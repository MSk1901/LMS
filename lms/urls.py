from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, SubscriptionAPIView, LessonListCreateAPIView, \
    LessonRetrieveUpdateDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lessons'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson'),

    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription'),
] + router.urls
