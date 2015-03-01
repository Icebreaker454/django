"""Ehis module is for testing purposes"""

from django.test import TestCase
from students.models.student import Student
from students.models.group import Group

class StudentTestCase(TestCase):
    def student_str_representation(self):
        student = Student.objects.create(first_name="Alex", 
                                         last_name="Messer", 
                                         student_group = Group.objects.first(),
                                         ticket = "SD2334")
        self.assertEqual(student.__unicode__(), "%s %s" %(student.first_name ,student.last_name))


