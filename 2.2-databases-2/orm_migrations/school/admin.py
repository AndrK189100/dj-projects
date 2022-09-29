from django.contrib import admin
from .models import Student, Teacher


class TeachersStudentsInline(admin.TabularInline):
    model = Student.teachers.through
    extra = 3

    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [TeachersStudentsInline]
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [TeachersStudentsInline]
    pass
