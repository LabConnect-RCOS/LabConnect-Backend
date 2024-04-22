# Profile
    The profile page will display the User's name, major/department, class and 
    their past opportunities. 

## Current code:  
``` Python
@main_blueprint.route("/profile/<string:rcs_id>")  
def profile(rcs_id: str):  
    return render_template("profile.html")
```

## Data needed:
Profile:
- Variables  
    - Username - string  
    - Title/Level - string  
    - Department - string  
    - Projects 
        - Current:  
            - professor - string  
            - credits - int  
            - description - string  
        - Past:  
            - professor - string  
            - credits - int  
            - description - string  

## Objectives
Query the Users database to access the user and get the needed  
data from the User object. In order to access the User's current  
and previous projects, query the opportunities database.

## Output Json data
{
"Profile":{
    "rcs_id": "str",
    "name": "str",
    "email": "str",
    "phone_number": "123-456-7890",
    "website": "str",
    "title": "str",
    "departments": "str",
    "past_opportunities": [
        "professor": "str",
        "credits": int,
        "description": "str",
    ],
    "current_opportunities": [
        "professor": "str",
        "credits": int,
        "description": "str",
    ],
    }
}
