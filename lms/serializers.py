from rest_framework import serializers

from lms.models import Course, Lesson
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'first_name', 'last_name')
