from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import MyPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import update_course
from users.permissions import ManagerPermission, OwnerPermission


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_permissions(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            self.permission_classes = [ManagerPermission | OwnerPermission]
        elif self.action == 'destroy':
            self.permission_classes = [OwnerPermission & IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated | ManagerPermission]
        elif self.action == 'create':
            self.permission_classes = [~ManagerPermission]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            if ManagerPermission().has_permission(self.request, self):
                return Course.objects.all().order_by('id')
            else:
                return Course.objects.filter(owner=user).order_by('id')
        else:
            return Course.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        recipients = instance.subscriptions.values_list('user__email', flat=True)
        update_course.delay(list(recipients), instance.title)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~ManagerPermission & IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | ManagerPermission]
    pagination_class = MyPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            if ManagerPermission().has_permission(self.request, self):
                return Lesson.objects.all().order_by('id')
            else:
                return Lesson.objects.filter(owner=user).order_by('id')
        else:
            return Lesson.objects.none()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ManagerPermission | OwnerPermission]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ManagerPermission | OwnerPermission]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [OwnerPermission]


class SubscriptionAPIView(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(course=course_item, user=user)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
