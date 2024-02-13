Department
----------

Current code:
```
@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")
```
Possibly:
What school professor is under:
- ITWS
- Lally 
- School of Architecture
- School of Engineering
- HASS
- School of Science

Professors could post to whole school to widen the range of students that can find the project 

Specific departments/ majors within a school 
- Computer Science
- Ect...

Profesors could post to one or maybe more than one major to find specific students within a major

Students would be able to look under schools and under majors

Department:
    Variables:
        School:
            Department:

|Department
----------
|ITWS
|Lally 
|School of Architecture
|School of Engineering
|HASS
|School of Science 

Therorticly what needs to be done to actually implement this
- Query for schools/departments
- to get past projects for each profesors
- Return to json    

List of current profs
List of currrent projects 

Data being returned 
{
  "professors": [],
  "projects": []
}
