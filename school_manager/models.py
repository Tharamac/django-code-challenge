from django.db import models
import uuid

class School(models.Model):
    name = models.CharField(max_length = 20)
    max_students = models.IntegerField()
    
    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    student_id = models.UUIDField(max_length = 20,default = uuid.uuid4, editable= False)
    school = models.ForeignKey(School, on_delete = models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name
    


