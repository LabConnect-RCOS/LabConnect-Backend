Phase 3: Devise database schema from ER Diagram

Steps to convert ER Diagram to relational model

1. Convert entities to relational model
   - Effectively, there's at least 4 in this case: rpi_departments, contact_links, lab_runner, opportunities
   - The other entities related to opportunities are: courses, majors, class_years, application_due_dates, semesters, salary_comp_info, upfront_pay_comp_info, credit_comp_info

2. Convert weak entities to relational model
   - There are no weak entities in the diagram
    
3. Convert relationships based on cardinality
   - The relationships are: isPartOf, hasLink, promotes, recommends_courses, recommends_majors, recommends_c_years, application_due, active_semesters, has_salary_comp, has_upfront_pay_comp, has_credit_comp

4. Convert entity hierarchies to relational model
   - The diagram has no entity hierarchies

## RELATIONS ##

Note: I usually include functional dependencies (fd) but this time it's implied that key -> all attributes, so I won't list them.

Template: name( set of attributes ),  key: (set of prime attributes)

The relations:

rpi_departments( name, description ), key: name

contact_links( contact_link, contact_type ), key: contact_link

lab_runner( rcs_id, name ), key: rcs_id

opportunities( id, name, description, active_status, recommended_experience ), key: id

courses( course_code, course_name ), key: course_code

majors( major_code, major_name ), key: major_code

class_years( class_year, class_name ), key: class_year

application_due_dates( date ), key: date

semesters( year, season ), key: (year, season)

salary_comp_info( usd_per_hour ), key: usd_per_hour 

upfront_pay_comp_info( usd ), key: usd 

credit_comp_info( number_of_credits, course_code ), key: (number_of_credits, course_code)


isPartOf(dep_name, lab_runner_rcs_id), key: (dep_name, lab_runner_rcs_id)
hasLink()
promotes()
recommends_courses()
recommends_majors()
recommends_c_years()
application_due()
active_semesters()
has_salary_comp()
has_upfront_pay_comp()
has_credit_comp()

