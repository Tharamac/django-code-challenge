from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *

class StudentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Student
       fields = ["first_name", "last_name", "student_id"]
