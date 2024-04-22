from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {
            'id': self.course.pk,
            'lesson_count': 0,
            'lessons': [],
            'is_subscribed': False,
            'title': 'Test Course',
            'preview': None,
            'description': None,
            'owner': self.user.pk
        }
                         )

    def test_course_list(self):
        url = reverse('lms:course-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    'id': self.course.pk,
                    'lesson_count': 0,
                    'lessons': [],
                    'is_subscribed': False,
                    'title': 'Test Course',
                    'preview': None,
                    'description': None,
                    'owner': self.user.pk
                }
            ]
        }
                         )

    def test_course_create(self):
        url = reverse('lms:course-list')
        data = {'title': 'Test 2'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {'title': 'Test fixed'}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Test fixed')

    def test_course_delete(self):
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.lesson = Lesson.objects.create(title='Test lesson',
                                            owner=self.user,
                                            video_url='https://www.youtube.com/watch?v=FyTL1bnUx5I&')
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data,
                         {
                             "id": self.lesson.pk,
                             "title": "Test lesson",
                             "preview": None,
                             "description": None,
                             "video_url": "https://www.youtube.com/watch?v=FyTL1bnUx5I&",
                             "course": None,
                             "owner": self.user.pk
                         }
                         )

    def test_lesson_list(self):
        url = reverse('lms:lessons')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": "Test lesson",
                    "preview": None,
                    "description": None,
                    "video_url": "https://www.youtube.com/watch?v=FyTL1bnUx5I&",
                    "course": None,
                    "owner": self.user.pk
                }
            ]
        }
                         )

    def test_lesson_create(self):
        url = reverse('lms:lesson-create')
        data = {
            'title': 'Test 2',
            'video_url': 'https://www.youtube.com/watch?v=FyTL1bnUx5I&'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:lesson-update', args=(self.lesson.pk,))
        data = {'title': 'Lesson fixed', 'video_url': 'https://www.youtube.com/watch?v=FyTL1bnUx5I&'}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'Lesson fixed')

    def test_lesson_delete(self):
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse('lms:subscription')
        data = {'course_id': self.course.pk}
        response1 = self.client.post(url, data)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json(), {"message": "подписка добавлена"})
        self.assertEqual(Subscription.objects.all().count(), 1)

        response2 = self.client.post(url, data)

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json(), {"message": "подписка удалена"})
        self.assertEqual(Subscription.objects.all().count(), 0)
