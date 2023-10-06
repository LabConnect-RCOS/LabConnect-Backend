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
* id: the id is used to uniquely identify an opportunity in the database.
* name: opportunities have a name.
* description: some text describing the opportunity
* active_status: boolean describing whether the opportunity is active
* recommended_experience: a long string describing recommended experience (VARCHAR: 65535 characters maximum)

Database stores rpi_departments:
* name: each department at RPI has a unique name
* description: some text describing the department at RPI

Database stores lab_runner: 
* rcs_id: a string to uniquely identify a lab_runner
* name: their name.

Database stores contact_links:
* contact link: the particular link used to contact someone, or group of people, or something.
* contact type: the type of contact information: email, phone number, website
* key: contact link

*Entities about opportunities*

Database stores courses:
* course_code: a code for the course. (i.e. CSCI-4380) This is the key.
* course_name: name of the course.

Database stores majors:
* major_code: a major code (for example: CSCI, BIOL, ESCE etc.) uniquely identifies a major in the database
* major_name: name of the major. 

Database stores class_years:
* class_years: a unique class year (i.e. freshmen, ...,senior, graduate)

Database stores pay_compensation_info:
* pay_usd_per_hour: the pay in US Dollars per hour of work in an opportunity

Database stores credit_compensation_info:
* number_of_credits: the number of credits awarded from an opportunity
* course_code: the course code that the credits go to.

Database stores application_due_date:
* date: the application due date to something (opportunity)

Database stores semesters:
* season: the season the semester is in (Spring, Summer, Fall, Winter)  
* year: the year the semester is in. 
---------

**Relationships**

A lab runner can promote many opportunities. An opportunity can be promoted by many lab runners.
A lab runner is part of many departments. A department has many lab runners.
A lab runner can have many contact links. A contact link can belong to many lab runners (group contacts).

An opportunity can recommend courses, majors, and class years.
Each of those entities can be recommended by many opportunities.

An opportunity can have: many pay compensation information and credit compensation information. 
Each pay or credit compensation information can be associated with many opportunities.

An opportunity can have applications due on many application_due_dates, while each due date may be shared 
by many opportunities.

An opportunity can be active in many semesters, while each semester can have many active opportunities.


## REFERENCES

https://www.w3schools.com/sql/sql_datatypes.asp





