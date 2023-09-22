**PHASE I: collecting information for database**

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

**Entities**
Database stores "opportunity" entities. 
* Name
* Type
* Department (what if more than 1 department?) ***GET BACK TO THIS LATER***
* Student Major Requirements
* Required Skills
* Student Year Requirements (Fr, So, Jr, Sr)
* Estimated Time Requirements
Each row represents one of these instances, or an individual opportunity.
All entities contain simple attributes and each column can only contain a single piece of data and each attribute must characterize the entity it belongs to. 

**Relationships**
Relationships then can be drawn in between the different entities.
