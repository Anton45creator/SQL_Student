#**SQL Student**
__________________________________________________________
##Description

The SQL Student program automatically fills the database with test data. Allows you to view and manage students, groups, courses.
To create tables in the database, type the following commands in the terminal:
>> set DATABASE="your database"
> 
>> python fake_data.py

To start the program, type the following commands:
>> DATABASE="your database"
> 
>> python main.py

_*To run the tests, do all the above operations and create a test database and
run the tests.*_
_________________________________________________________________________

After launching the program, using Curl or Postman, you can make http requests; request, add, delete students and groups.
Example of a http request:

>>curl -i -x POST -H "Content-Type: application/json" -d {"first_name": 
"Egor", "last_name": "Koshin"} http://127.0.0.1:5000/api/v1.0/students/

>>curl -i -x GET -H "Content-Type: application/json" -d {"student_id":"89"} 
> http://127.0.0.1:5000/api/v1.0/students/