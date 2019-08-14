# Interview management

    - Write a Python application which provides an API for an interview calendar.
    - There are interviewers and candidates. Each interview may consist of exactly one candidate and one or more interviewers.
    - If there are more interviewers available than candidates, the spare interviewers are distributed evenly across candidates.

    1. Interviewers can add slots when they have time independently from each other
    2. Candidates can add slots when they have time independently from each other
    3. Anyone can retrieve a collection of slots when interviews can take place. The API allows the caller to optionally define the candidate and optionally to define one or more interviewer. The API requires either the candidate or the interviewer(s) to be set

# Technology stack:

    - python 3.7,
    - Flask 1.0,
    - flake8 3.5.0,
    - docker 18.06.1-ce,
    - docker-compose 1.22.0,
    - swagger api documentation 2.0,
    - postgres 11.4,
    - Flask-Testing 2.1.1,
    - gunicorn 19.7.1,
    - Flask-SQLAlchemy 2.3.2,
    - coverage 4.4.2.

# To build and run the project:

    - docker-compose -f docker-compose-dev.yml build

# Run unit Test and code coverage:

    - docker-compose -f docker-compose-dev.yml run interview python manage.py cov

# Run code linting with flake8:

    - docker-compose -f docker-compose-dev.yml run interview flake8 project

# Run project:

    - docker-compose -f docker-compose-dev.yml up

# Test if service is up and runing:

    - http://localhost:5001/interview/ping

![TEST RUNING SERVICE](/images/ping.png)

# Api documentation:

    - http://localhost:8082/swagger

![Swagger API DOC](/images/Swagger_API.png)
