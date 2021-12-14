from sqlalchemy.orm.exc import NoResultFound
from models import CourseModel, GroupModel, StudentModel
from flask_restful import Resource
from app import db
from flask import request


class Students(Resource):
    def get(self):
        data = request.get_json(force=True)
        student_id = data.get('student_id')
        student_info = {}
        for student in db.session.query(StudentModel).filter(StudentModel.id ==
                                                             student_id):
            student_info[student.id] = dict(
                id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                group_id=student.group_id,
                courses=[course.name for course in student.courses],
            )
            return student_info

    # Add new student
    def post(self):
        data = request.get_json(force=True)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        db.session.add(
            StudentModel(
                group_id=None,
                first_name=first_name,
                last_name=last_name,
            )
        )
        db.session.commit()
        return {'code': 201, 'message': f'{first_name} {last_name} added'}, 201

    # Delete student by STUDENT_ID
    def delete(self):
        data = request.get_json(force=True)
        student_id = data.get('student_id')
        try:
            db.session.delete(db.session.query(StudentModel).filter(
                StudentModel.id == student_id).one())
            db.session.commit()
            return {
                'code': 200,
                'message': f'Student with the ID = {student_id} deleted.',
            }, 200
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404


class Groups(Resource):
    # Receives groups and students.
    def get(self):
        groups = {}
        for group in db.session.query(GroupModel).all():
            students = {}
            for student in db.session.query(
                    StudentModel).filter(StudentModel.group_id == group.name):
                students[student.id] = dict(
                    id=student.id,
                    name=f'{student.first_name} {student.last_name}',
                )
            groups[group.name] = dict(
                id=group.id,
                name=group.name,
                volume=len(students),
                students=students,
            )
        return groups

    # Adds a new group.
    def post(self):
        data = request.get_json(force=True)
        group_name = data.get('group_name')
        db.session.add(GroupModel(name=group_name))
        db.session.commit()
        return {'code': 201, 'message': f'{group_name} has been added!'}, 201

    # Deletes a group.
    def delete(self):
        data = request.get_json(force=True)
        group_name = data.get('group_name')
        try:
            db.session.delete(db.session.query(GroupModel).filter(
                GroupModel.name == group_name).one())
            db.session.commit()
            return {
                       'code': 200,
                       'message': f'Group with the ID = {group_name} deleted.',
                   }, 200
        except NoResultFound:
            return {'code': 404, 'message': 'Group not found'}, 404


class StudentsOnCourse(Resource):
    # Adds a new group.
    def get(self):
        data = request.get_json(force=True)
        course_name = data.get('course_name')
        courses_list = [crse.name for crse in db.session.query(
            CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
        students = {}
        for student in db.session.query(StudentModel).\
            select_from(CourseModel).\
                join(StudentModel.courses).\
                    filter(CourseModel.name == course_name):
            students[student.id] = dict(
                id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                group_id=student.group_id,
            )
        return students

    # Add a student to the course (from a list)
    def put(self):
        data = request.get_json(force=True)
        course_name = data.get('course_name')
        student_id = data.get("student_id")
        courses_list = [crse.name for crse in db.session.query(
            CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
        course = db.session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        try:
            student = db.session.query(
                 StudentModel).filter(StudentModel.id == student_id).one()
            student.courses.append(course)
            db.session.commit()
            return {
                'code': 401,
                'mesage': f'Student with the ID = {student_id} added to the {course_name} course.',
                }, 401
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404

    # Remove the student from one of his or her courses
    def delete(self):
        data = request.get_json(force=True)
        course_name = data.get('course_name')
        student_id = data.get("student_id")
        courses_list = [crse.name for crse in db.session.query(
            CourseModel).all()]
        if course_name not in courses_list:
            return {'code': 404, 'message': 'Course not found'}, 404
        course = db.session.query(
            CourseModel).filter(CourseModel.name == course_name).one()
        try:
            student = db.session.query(
                StudentModel).filter(StudentModel.id == student_id).one()
            student.courses.remove(course)
            db.session.commit()
            return {
                'code': 404,
                'message': f'Student with the ID = {student_id} '
                           f'removed from the {course_name} course.',
                }, 404
        except NoResultFound:
            return {'code': 404, 'message': 'Student not found'}, 404
