import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from students.models import Course, Student
from django_testing import settings


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def students_factory():
    def students(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return students


@pytest.fixture()
def courses_factory():
    def courses(*args, **kwargs):
        students = baker.prepare(Student, *args, **kwargs)
        return baker.make(Course, students=students, *args, **kwargs)

    return courses


@pytest.mark.django_db
def test_get_courses(client, courses_factory):
    courses_count = Course.objects.count()
    courses_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10 + courses_count


@pytest.mark.django_db
def test_get_course(client, courses_factory):
    courses_factory(_quantity=1)
    course_id = Course.objects.all()[0].pk
    response = client.get(f'/api/v1/courses/{course_id}/')
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == course_id


@pytest.mark.django_db
def test_create_course(client, students_factory):
    courses_count = Course.objects.count()
    students_factory(_quantity=1)
    student_id = Student.objects.all()[0].pk
    response = client.post('/api/v1/courses/', data={'name': 'course', 'student': student_id})

    assert response.status_code == 201
    assert Course.objects.count() == courses_count + 1


@pytest.mark.django_db
def test_filter_courses_by_id(client, courses_factory):
    courses_factory(_quantity=10)
    course_id = Course.objects.all()[0].pk
    response = client.get(f'/api/v1/courses/?id={course_id}')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_courses_by_name(client, courses_factory):
    courses_factory(_quantity=10)
    course_name = Course.objects.all()[0].name
    response = client.get(f'/api/v1/courses/?name={course_name}')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == course_name


settings.MAX_STUDENTS_PER_COURSE = 5


@pytest.mark.parametrize(('quantity', 'status', 'created'), ((1, 200, 1), (6, 400, 0)))
@pytest.mark.django_db
def test_update_course(client, courses_factory, quantity, status, created):
    courses_factory(_quantity=quantity)
    student_id = Student.objects.all()[0].pk
    course_id = Course.objects.all()[0].pk

    response = client.put(f'/api/v1/courses/{course_id}/', data={'name': 'new_name', 'student': student_id})

    assert response.status_code == status
    assert Course.objects.filter(pk=course_id, name='new_name', students=student_id).count() == created


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    courses_factory(_quantity=10)
    courses_count = Course.objects.count()
    course_id = Course.objects.all()[0].pk

    response = client.delete(f'/api/v1/courses/{course_id}/')
    assert response.status_code == 204
    assert Course.objects.count() == courses_count - 1
