from django.test import TestCase
from django.urls import reverse
from school_manager import views
from rest_framework import status
from rest_framework.test import APIRequestFactory

class StudentsTest(APITestCase):
    student_url = reverse(views.StudentViewSet)
    school_url = reverse(views.SchoolViewSet)
    # Test Post request on school data
    def test_post_and_get_school(self):
        data = {
            "name" : "Test School",
            "max_students" : 1
        }
        response = self.client.post(school_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_data = School.objects.filter(name = data["name"])[0]
        self.assertDictEqual(check_data , data )
        school_id = check_data.id
        response = self.client.get(schools_url + str(school_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_school(self):

