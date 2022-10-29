from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        pass
        if self.context['request'].method in ['PATCH', 'PUT']:
            course = Course.objects.filter(pk=self.context['request'].parser_context['kwargs']['pk'])
            count_students_on_course = course[0].students.count()
            if count_students_on_course > MAX_STUDENTS_PER_COURSE:
                raise ValidationError('To many students on the course')
        return data
