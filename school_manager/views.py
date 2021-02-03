from django.shortcuts import render
from school_manager.serializers import SchoolSerializer, StudentSerializer
from school_manager.models import Student, School
from rest_framework import permissions
from rest_framework import viewsets
# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentsListViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    def get_queryset(self):
        return Student.objects.filter(school = self.kwargs['school_pk'])
    def perform_create(self, serializer):
        serializer.save(school= self.kwargs['school_pk'])