from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import LessonURLValidator
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [LessonURLValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner']

    def get_lesson_count(self, instance):
        return instance.lessons.count()
