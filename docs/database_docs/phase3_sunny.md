Phase 3: Devise database schema from ER Diagram

Steps to convert ER Diagram to relational model

1. Convert entities to relational model
   - Effectively, there's at least 4 in this case: rpi_departments, contact_links, lab_runner, opportunities
   - The other entities related to opportunities are: courses, majors, experiences, class_years, application_due_dates, semesters, pay_compensation_info, credit_compensation_info

2. Convert weak entities to relational model
   - There are no weak entities in the diagram
    
3. Convert relationships based on cardinality
   - The relationships are: isPartOf, hasLink, promotes, recommends_courses, recommends_majors, recommends_experiences, recommends_c_years, application_due, active_semesters, has_pay_comp, has_credit_comp

4. Convert entity hierarchies to relational model
   - The diagram has no entity hierarchies

## RELATIONS ##

Note: I usually include functional dependencies (fd) but this time it's implied that key -> all attributes, so I won't list them.

Template: name( set of attributes ),  key: (set of prime attributes)

rpi_departments( name, description ), key: name

contact_links( contact_link, contact_type ), key: contact_link

lab_runner( rcs_id, name ), key: rcs_id

opportunities( name, description, active_status ), key: name

isPartOf, hasLink, promotes, recommends_courses, recommends_majors, recommends_experiences, recommends_c_years, application_due, active_semesters, has_pay_comp, has_credit_comp
