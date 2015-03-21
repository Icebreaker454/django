# -*- coding: utf-8 -*-

"""
    This module is for testing purposes
"""


from django.test import TestCase
from students.models.student import Student
from students.models.group import Group


class StudentTest(TestCase):
    """
        Student test block
    """
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Alex",
            last_name="Messer",
            student_group=Group.objects.first(),
            ticket="SD2334"
        )

    def test_student_str_representation(self):
        return self.assertEqual(
            self.student.__unicode__(),
            "%s %s" % (
                self.student.first_name,
                self.student.last_name
            )
        )

    def test_student_verbose_name_plural(self):
        return self.assertEqual(Student._meta.verbose_name_plural, u"Студенти")

    def test_students_index(self):
        response = self.client.get('/')
        return self.assertEqual(response.status_code, 200)

    def test_entry(self):
        response = self.client.get('/')
        return self.assertContains(response, u"%s %s" % (self.student.first_name, self.student.last_name))
