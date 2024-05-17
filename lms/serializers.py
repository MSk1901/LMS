from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import LessonURLValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [LessonURLValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course"""
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        """Метод для вложенного создания курса с уроками"""
        lessons_data = validated_data.pop('lessons', [])
        course = Course.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)
        return course

    def get_lesson_count(self, instance):
        """Метод для получения количества уроков в курсе"""
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        """Метод для проверки подписки текущего пользователя на курс"""
        return instance.subscriptions.exists()
