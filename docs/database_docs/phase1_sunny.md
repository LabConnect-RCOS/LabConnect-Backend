## PHASE I: collecting information for database

**Intro**

I need to know what people want in a database that stores research project information. 

There are 3 user groups: professors, graduate students and undergraduate students. Our product connects them to projects. Actually, I think we can group up undergraduate and graduate students into 1 student group.

So we should ask some questions to each group. 

The goal is to form a natural description of the database. Keep in mind 2 things: Entities and Relationships between them. For more details, see entities_and_relationships document

Questions we ask them
Professors:
* What research projects do they offer?
* Prerequisites for each project: sometimes coursework, sometimes experience -> hard to figure out database structure
* What are research projects about? How can we represent that in a database?
* Major? Available to graduate students only, undergraduates only, or both?
* Compensation?

Students
* What do they look for in a research project? 
* Major, matching prerequisites, compensation, availability, compensation?

Once these questions are answered, the entity relationship diagram can be drawn and the database can be designed in its entirety.

Opportunities require and/or recommend stuff:
- courses taken
- majors
- class year (i.e. sophomore)
- experience

## Entities and relationships

**Entities**

Database stores opportunities
* name: all opportunities are uniquely identified by name in the database
* description: some text describing the opportunity
* active_status: boolean describing whether the opportunity is active

Database stores rpi_departments:
* name: each department at RPI has a unique name
* description: some text describing the department at RPI

Database stores lab_runner: 
* rcs_id: a string to uniquely identify a lab_runner
* name: their name.

Database stores contact_links:
* contact link: the particular link used to contact someone, or group of people, or something.
* contact type: the type of contact information: email, phone number, website

--------
These 4 entities will likely not receive a table representation (due to being eliminated after normalization).

Database stores courses:
* course_code: a code for the course. (i.e. CSCI 4380) This is the key.
* course_name: name of the course.

Database stores majors:
* major_name: a unique major name

Database stores class_years:
* class_years: a unique class year (i.e. freshmen, sophomore, ...,senior, graduate)
  
Database stores experiences:
* description: a text describing a potential requirement/recommendation for experiences.
---------

**Relationships**

A lab runner can promote many opportunities. An opportunity can be promoted by many lab runners.



