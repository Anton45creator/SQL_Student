from main import app

client = app.test_client()


def test_student(db_session):
    response = client.get("/api/v1/student")
    assert response.status_code, 200


def test_course(db_session):
    response = client.get("/api/v1/course")
    assert response.status_code, 200


def test_group(db_session):
    response = client.get("/api/v1/group")
    assert response.status_code, 200


def test_add_new_student(db_session):
    response = client.post(
        '/api/v1.0/students/',
        data=dict(first_name='Andrew', last_name='Martic'),
    ).get_data(as_text=True)
    assert {"mesage": "Andrew Martic added."}, response
    students_after = client.get('/api/v1.0/students/').get_data(as_text=True)
    assert{'Martic', students_after}
    assert{'Andrew', students_after}


def test_delete_student_by_id(db_session):
    students_before = client.get('/api/v1.0/students/').get_data(as_text=True)
    assert {'Martic', students_before}
    response = client.delete('/api/v1.0/students/201/',).get_data(as_text=True)
    assert {"mesage": "Student with the ID = 201 deleted."}, response
    students_after = client.get('/api/v1.0/students/').get_data(as_text=True)
    assert {None, students_after}


def test_add_student_to_course(db_session):
    course_before = client.post(
        '/api/v1/students/',
        data=dict(course_name='biology')
    ).get_data(as_text=True)
    response = client.delete(
        '/api/v1/students/201/course/',
        data=dict(course_name='biology'),
    ).get_data(as_text=True)
    assert {"mesage": "Student with the ID = 201 removed from the biology "
                      "course."}, response

    course_after = client.post(
        '/api/v1/students/',
        data=dict(course_name='biology'),
    ).get_data(as_text=True)
    assert{'Martic', course_before}
    assert{None, course_after}


def test_remove_student_from_course(db_session):
    course_before = client.post(
        '/api/v1.0/students/',
        data=dict(course_name='biology')
    ).get_data(as_text=True)
    response = client.delete(
        '/api/v1/students/201/course/',
        data=dict(course_name='biology'),
    ).get_data(as_text=True)
    assert {"mesage": "Student with the ID = 201 removed from the biology "
            "course."}, response
    course_after = client.post(
        '/api/v1.0/students/',
        data=dict(course_name='biology'),
    ).get_data(as_text=True)
    assert {'Martic', course_before}
    assert {None, course_after}


