from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import ManagerPermission, OwnerPermission


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            self.permission_classes = [ManagerPermission | OwnerPermission]
        elif self.action == 'destroy':
            self.permission_classes = [OwnerPermission]
        elif self.action == 'list':
            self.permission_classes = [ManagerPermission | IsAuthenticated]
        elif self.action == 'create':
            self.permission_classes = [~ManagerPermission]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        if ManagerPermission().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~ManagerPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [ManagerPermission | IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if ManagerPermission().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


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
