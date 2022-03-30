from app import app, api
from resourses import *


api.add_resource(Students, '/students/', methods=['GET', 'POST', 'DELETE'])

api.add_resource(Groups, '/groups/', methods=['GET', 'POST', 'DELETE'])

api.add_resource(StudentsOnCourse, '/course/', methods=['GET', 'POST', 'PUT',
                                                        'DELETE'])


if __name__ == '__main__':
    app.run()
