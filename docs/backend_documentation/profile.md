# Profile

## Current code:  
@main_blueprint.route("/profile/<string:rcs_id>")  
def profile(rcs_id: str):  
    return render_template("profile.html")

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

## Objectives-
Query the Users database to access the user and get the needed  
data from the User object. In order to access the User's current  
and previous projects, query the opportunities database.
