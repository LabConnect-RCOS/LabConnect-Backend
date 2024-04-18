## Department Documentation

### Overview

The department functionality allows users to explore projects posted by professors based on their respective schools and departments or majors within a school. This documentation outlines the current implementation and proposed enhancements for this feature.

### Current Implementation

#### Code Snippet
```python
@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")
```

#### Functionality
- The current implementation renders a department-specific page based on the provided department parameter.

### Proposed Enhancements

#### Expansion of School and Major Options
- **School Options:**
  - ITWS
  - Lally
  - School of Architecture
  - School of Engineering
  - HASS
  - School of Science

- **Major Options:**
  - Specific departments/majors within each school

#### Project Posting Options
- Professors can post projects to the entire school, broadening the reach to students across various majors within the school.
- Professors can also target specific departments or majors within a school to find students with specialized skills or interests.

#### User Experience Improvement
- Students can navigate through schools and majors to explore available projects.
- Projects posted by professors will be categorized under schools and departments/majors for easy accessibility.

#### Implementation Steps

1. **Query for Schools/Departments:**
   - Retrieve a list of schools and their respective departments or majors.

2. **Retrieve Past Projects for Each Professor:**
   - Fetch past projects posted by professors, categorized under schools and departments/majors.

3. **Return Data in JSON Format:**
   - Provide a JSON response containing information about professors and their associated projects.

#### Data Structure

```json
{
  "professors": [],
  "projects": []
}
```

#### Current Data Returned
- Currently, the department endpoint returns data including school, description, and major information.