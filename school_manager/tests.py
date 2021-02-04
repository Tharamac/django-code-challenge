from django.test import TestCase
from django.urls import reverse
from school_manager.views import School, Student 
from rest_framework import status
from rest_framework.test import APITestCase

class SchoolTest(APITestCase):
    school_url = '/schools/'

    def test_POST_response(self):
        # name input has 20 characters
        data = {
            "name" : "Test High School DxD",
            "max_students" : 1
        }
        # Test POST request on school data.
        post_response = self.client.post(self.school_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        
        # Check data integrity
        school_id = post_response.data['id']
        check_data = School.objects.filter(id = school_id)[0]
        
        self.assertEqual(check_data.name, data['name'])
        self.assertEqual(check_data.max_students, data['max_students'])

    def test_POST_response_but_input_over_20_characters(self):
        data = {
            "name" : "Tester Senior High School ",
            "max_students" : 1
        }
        # Test POST request on school data.
        post_response = self.client.post(self.school_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
       

    def test_POST_blank_name(self):
        data = {
            "name" : "",
            "max_students" : 1
        }
        post_response = self.client.post(self.school_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POST_zero_max_students(self):
        data = {
            "name" : "Empty School",
            "max_students" : 0
        }
        post_response = self.client.post(self.school_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_GET_response(self):
        data = {
            "name" : "Test School",
            "max_students" : 1
        }      
        post_response = self.client.post(self.school_url, data, format='json')
        school_id = post_response.data['id']
    
        # Test GET request on school data
        get_response = self.client.get(self.school_url + str(school_id) +'/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        # Test response data integrity
        get_response_data = get_response.data
        self.assertEqual(get_response_data['name'], data['name'])
        self.assertEqual(get_response_data['max_students'], data['max_students'])
  
    def test_PUT_response(self): 
        data = {
            "name" : "Test School",
            "max_students" : 1
        }      
        post_response = self.client.post(self.school_url, data, format='json')
        post_response_data = post_response.data

        # Test PUT request on school data
        data['name'] = "Testing School"
        data['max_students'] = 5
        put_response = self.client.put(self.school_url + str(post_response_data['id']) + '/', data)
        put_response_data = put_response.data
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response_data['id'], post_response_data['id'])
        self.assertEqual(put_response_data['name'], data['name'])
        self.assertEqual(put_response_data['max_students'], data['max_students'])

    def test_PUT_response_but_input_over_20_characters(self):  
        data = {
            "name" : "Test School",
            "max_students" : 1
        }      
        post_response = self.client.post(self.school_url, data, format='json')
        post_response_data = post_response.data
       
        data['name'] = "123456789012345678901"
        put_response = self.client.put(self.school_url + str(post_response_data['id']) +'/', data)
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_DELETE_response(self):  
        data = {
            "name" : "Test School",
            "max_students" : 1
        }      
        post_response = self.client.post(self.school_url, data, format='json')
        post_response_data = post_response.data
       
        delete_response = self.client.delete(self.school_url +  str(post_response_data['id']) +'/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # check data is really deleted
        get_response = self.client.get(self.school_url +  str(post_response_data['id']) +'/')
        self.assertEqual(get_response.status_code,status.HTTP_404_NOT_FOUND)      
    
class StudentTest(APITestCase):
    student_url = '/students/'
    school_url = '/schools/'
    school_id:int = None
    school_max_students:int = None
    def setUp(self):
        data = {
            "name" : "Test High School DxD",
            "max_students" : 1
        }
        # Test POST request on school data.
        post_response = self.client.post(self.school_url, data, format='json')
        self.school_id = post_response.data['id']
        self.school_max_students = post_response.data['max_students']
        return super().setUp()
    
    def test_POST_response(self):
        # name input has 20 characters
        data = {
            "first_name" : "Tharasumaichikosorai",
            "last_name" :  "Takahashimakotomikan",
            "school" : self.school_id
        }
        # Test POST request on school data.
        post_response = self.client.post(self.student_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
    
        # Check data integrity
        student_id = post_response.data['id']
        check_data = Student.objects.filter(id = student_id)[0]
        
        self.assertEqual(check_data.first_name, data['first_name'])
        self.assertEqual(check_data.last_name, data['last_name'])
        self.assertEqual(check_data.school.id, data['school'])

    def test_POST_response_on_nested_route(self):
        # name input has 20 characters
        data = {
            "first_name" : "Tharasumaichikosorai",
            "last_name" :  "Takahashimakotomikan",
            "school" : self.school_id
        }
        # Test POST request on school data.
        url = self.school_url + str(self.school_id) + self.student_url
        post_response = self.client.post(url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
    
        # Check data integrity
        student_id = post_response.data['id']
        check_data = Student.objects.filter(id = student_id)[0]
        
        self.assertEqual(check_data.first_name, data['first_name'])
        self.assertEqual(check_data.last_name, data['last_name'])
        self.assertEqual(check_data.school.id, data['school'])

    def test_POST_in_full_school(self):
        data = {
            "first_name" : "Tharasumaichikosorai",
            "last_name" :  "Takahashimakotomikan",
            "school" : self.school_id
        }
        # Test POST request 
        post_response = self.client.post(self.student_url, data, format='json')
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        post_response = self.client.post(self.student_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post_response.data['school'][0].__str__(), "This school is already full.")

    def test_POST_in_full_school_on_nested_route(self):
        data = {
            "first_name" : "Tharasumaichikosorai",
            "last_name" :  "Takahashimakotomikan",
            "school" : self.school_id
        }
        url = self.school_url + str(self.school_id) + self.student_url
        # Test POST request 
        post_response = self.client.post(url, data, format='json')
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        post_response = self.client.post(url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post_response.data['school'][0].__str__(), "This school is already full.")

    def test_POST_response_but_input_over_20_characters(self):
        data = {
            "first_name" : "Tharasumaichikosoraima",
            "last_name" :  "Takahashimakotoshinpei",
            "school" : self.school_id
        }
        # Test POST request 
        post_response = self.client.post(self.student_url, data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_GET_response(self):
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        post_response = self.client.post(self.student_url, data, format='json')
        student_id = post_response.data['id']
    
        # Test GET request 
        get_response = self.client.get(self.student_url + str(student_id) +'/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        # Test response data integrity
        get_response_data = get_response.data
        self.assertEqual(get_response_data['first_name'], data['first_name'])
        self.assertEqual(get_response_data['last_name'], data['last_name'])
        self.assertEqual(get_response_data['school'], data['school'])

    def test_GET_response_on_nested_route(self):
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        url = self.school_url + str(self.school_id) + self.student_url
        post_response = self.client.post(url, data, format='json')
        student_id = post_response.data['id']
    
        # Test GET request 
        get_response = self.client.get(url + str(student_id) +'/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        # Test response data integrity
        get_response_data = get_response.data
        self.assertEqual(get_response_data['first_name'], data['first_name'])
        self.assertEqual(get_response_data['last_name'], data['last_name'])
        self.assertEqual(get_response_data['school'], data['school'])
  
    def test_PUT_response(self): 
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        post_response = self.client.post(self.student_url, data, format='json')    
        post_response_data = post_response.data
    
        # Test PUT request 
        data['first_name'] = "Testing School"
        put_response = self.client.put(self.student_url + str(post_response_data['id']) + '/', data)
        # print(put_response.data)
        put_response_data = put_response.data
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response_data['id'], post_response_data['id'])
        self.assertEqual(put_response_data['first_name'], data['first_name'])

    def test_PUT_response_on_nested_route(self): 
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        url = self.school_url + str(self.school_id) + self.student_url
        post_response = self.client.post(url, data, format='json')    
        post_response_data = post_response.data
        
    
        # Test PUT request 
        data['first_name'] = "Testing School"
        put_response = self.client.put(url + str(post_response_data['id']) + '/', data)
        # print(put_response.data)
        put_response_data = put_response.data
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response_data['id'], post_response_data['id'])
        self.assertEqual(put_response_data['first_name'], data['first_name'])


    def test_DELETE_response(self):  
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        post_response = self.client.post(self.student_url, data, format='json')    
        post_response_data = post_response.data
       
       
        delete_response = self.client.delete(self.student_url +  str(post_response_data['id']) +'/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # check data is really deleted
        get_response = self.client.get(self.student_url +  str(post_response_data['id']) +'/')
        self.assertEqual(get_response.status_code,status.HTTP_404_NOT_FOUND)

    def test_DELETE_response_on_nested_route(self):  
        data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : self.school_id
        }
        url = self.school_url + str(self.school_id) + self.student_url
        post_response = self.client.post(url, data, format='json')    
        post_response_data = post_response.data
    
        delete_response = self.client.delete(url +  str(post_response_data['id']) +'/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # check data is really deleted
        get_response = self.client.get(self.student_url +  str(post_response_data['id']) +'/')
        self.assertEqual(get_response.status_code,status.HTTP_404_NOT_FOUND)      

class NestedRouteTest(APITestCase):
    student_url = '/students/'
    school_url = '/schools/'
    
    def test_GET_all_students(self):
        school_data = {
            "name" : "Nested",
            "max_students" : 15
        }
        # Test POST request on school data.
        school_post_response = self.client.post(self.school_url, school_data, format='json')
        school_id = school_post_response.data['id']
        student1_data = {
            "first_name" : "Tharasumaichikosorai",
            "last_name" :  "Takahashimakotomikan",
            "school" : school_id
        }
        # Test POST request 
        student1_post_response = self.client.post(self.student_url,student1_data, format='json')
        student2_data = {
            "first_name" : "Childe",
            "last_name" :  "Tartaglia",
            "school" : school_id
        }
        student2_post_response = self.client.post(self.student_url, student2_data, format='json')
        self.school_id = school_post_response.data['id']
        url = self.school_url + str(school_id) + self.student_url
        get_response = self.client.get(url)
        self.assertEqual(len(get_response.data), 2)