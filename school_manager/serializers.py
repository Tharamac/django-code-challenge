from rest_framework import serializers
from school_manager.models import School,Student 

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
       model = Student
       fields = '__all__'
    
    def validate_school(self, selected_school):
        # selected_school = attr['school']
        max_number = School.objects.filter(name = selected_school)[0].max_students
        current_num_of_students = len(Student.objects.filter(school = selected_school))
        if(current_num_of_students >= max_number):
            raise serializers.ValidationError("This school is already full")
        else:
            return selected_school
        
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


