from datetime import datetime

from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from labconnect import db
from labconnect.helpers import LocationEnum, SemesterEnum, format_credits
from labconnect.models import (
    LabManager,
    Leads,
    Opportunities,
    RecommendsClassYears,
    User,
    Courses,
)

from . import main_blueprint


@main_blueprint.get("/searchOpportunity/<string:query>")
def searchOpportunity(query: str):
    # Perform a search
    stmt = (
        db.select(Opportunities)
        .where(
            # Made query input
            (
                Opportunities.search_vector.match(input)
            )  # Full-text search using pre-generated tsvector
            | (
                db.func.similarity(Opportunities.name, input) >= 0.1
            )  # Fuzzy search on the 'name' field
            | (
                db.func.similarity(Opportunities.description, input) >= 0.1
            )  # Fuzzy search on the 'description' field
        )
        .order_by(
            db.func.similarity(
                Opportunities.name, input
            ).desc()  # Order by similarity for fuzzy search results
        )
    )
    # Perform a search
    # stmt = (
    #     db.select(Opportunities)
    #     .where(
    #         (
    #             Opportunities.search_vector.match(input)
    #         )  # Full-text search using pre-generated tsvector
    #         | (
    #             db.func.similarity(Opportunities.name, input) >= 0.1
    #         )  # Fuzzy search on the 'name' field
    #         | (
    #             db.func.similarity(Opportunities.description, input) >= 0.1
    #         )  # Fuzzy search on the 'description' field
    #     )
    #  .order_by(
    #         db.func.similarity(
    #             Opportunities.name, input
    #         ).desc()  # Order by similarity for fuzzy search results
    #     )
    # )

    data = db.session.execute(stmt).scalars().all()

    results = []

    for opportunity in data:
        results.append(opportunity.to_dict())

    return results


# @main_blueprint.get("/opportunity")
# def getOpportunity2():
#     if not request.data:
#         abort(400)
#     json_request_data = request.get_json()
#     if not json_request_data:
#         abort(400)
#     id = json_request_data.get("id", None)
#     if not id:
#         abort(400)
#     data = db.first_or_404(db.select(Opportunities).where(Opportunities.id == id))
#     result = data.to_dict()
#     return result


def convert_to_enum(location_string):
    try:
        return LocationEnum[
            location_string.upper()
        ]  # Use upper() for case-insensitivity
    except KeyError:
        return None  # Or raise an exception if you prefer


def packageOpportunity(opportunityInfo, professorInfo):
    data = opportunityInfo.to_dict()
    data["professor"] = professorInfo.name
    data["department"] = professorInfo.department_id
    return data


def packageIndividualOpportunity(opportunityInfo):
    data = {
        "id": opportunityInfo.id,
        "name": opportunityInfo.name,
        "description": opportunityInfo.description,
        "recommended_experience": opportunityInfo.recommended_experience,
        "author": "",
        "department": "",
    }
    data = {
        "id": opportunityInfo.id,
        "name": opportunityInfo.name,
        "description": opportunityInfo.description,
        "recommended_experience": opportunityInfo.recommended_experience,
        "author": "",
        "department": "",
    }

    opportunity_credits = ""
    if opportunityInfo.one_credit:
        opportunity_credits += "1, "
    if opportunityInfo.two_credits:
        opportunity_credits += "2, "
    if opportunityInfo.three_credits:
        opportunity_credits += "3, "
    if opportunityInfo.four_credits:
        opportunity_credits += "4"

    if opportunity_credits != "":
        opportunity_credits += " credits"

    data["aboutSection"] = [
        {
            "title": "Pay",
            "description": f"${opportunityInfo.pay} per hour",
        },
        {
            "title": "Semester",
            "description": f"{opportunityInfo.semester} {opportunityInfo.year}",
        },
        {
            "title": "Application Due",
            "description": opportunityInfo.application_due,
        },
    ]

    if opportunity_credits != "":
        data["aboutSection"].append(
            {
                "title": "Credits",
                "description": opportunity_credits,
            }
        )

    # get professor and department by getting Leads and LabManager

    query = db.session.execute(
        db.select(Leads, LabManager)
        .where(Leads.opportunity_id == opportunityInfo.id)
        .join(LabManager, Leads.lab_manager_id == LabManager.id)
    )

    queryInfo = query.all()

    if len(queryInfo) == 0:
        return data

    data["department"] = queryInfo[0][1].department_id

    # for i, item in enumerate(queryInfo):
    # data["author"] += item[1].getName()
    # data["author"] += "look at def packageIndividualOpportunity(opportunityInfo):"
    # if i != len(queryInfo) - 1:
    # data["author"] += ", "

    author_names = [item[1].getName() for item in queryInfo]
    data["author"] = ", ".join(author_names)

    if len(queryInfo) > 1:
        data["authorProfile"] = (
            "https://t4.ftcdn.net/jpg/03/78/40/51/360_F_378405187_PyVLw51NVo3KltNlhUOpKfULdkUOUn7j.jpg"
        )
    elif len(queryInfo) == 1:
        data["authorProfile"] = (
            "https://cdn-icons-png.flaticon.com/512/1077/1077114.png"
        )

    return data


def packageOpportunityCard(opportunity):

    # get professor and department by getting Leads and LabManager
    query = db.session.execute(
        db.select(Leads, LabManager, User.first_name, User.last_name)
        .where(Leads.opportunity_id == opportunity.id)
        .join(LabManager, Leads.lab_manager_id == LabManager.id)
        .join(User, LabManager.id == User.lab_manager_id)
    )

    data = query.all()

    professorInfo = ", ".join(item[1].getName() for item in data)

    card = {
        "id": opportunity.id,
        "title": opportunity.name,
        "professor": professorInfo,
        "season": opportunity.semester,
        "location": "TBA",
        "year": opportunity.year,
    }

    return card


# @main_blueprint.get("/getOpportunity/<int:opp_id>")
# def getOpportunity(opp_id: int):
#     # query database for opportunity
#     query = db.session.execute(
#         db.select(Opportunities).where(Opportunities.id == opp_id)
#     )

#     data = query.all()

#     # check if opportunity exists
#     if not data or len(data) == 0:
#         abort(404)

#     data = data[0]
#     oppData = packageIndividualOpportunity(data[0])

#     # return data in the below format if opportunity is found
#     return {"data": oppData}


# @main_blueprint.get("/opportunity/filter")
# @main_blueprint.route("/opportunity/filter", methods=["GET"])
# def getOpportunities():
#     # Handle GET requests for fetching default active opportunities
#     data = db.session.execute(
#         db.select(Opportunities)
#         .where(Opportunities.active == True)
#         .limit(20)
#         .order_by(Opportunities.last_updated.desc())
#         .distinct()
#     ).scalars()
#     result = [opportunity.to_dict() for opportunity in data]
#     return result


##@main_blueprint.route("/opportunity/filter", methods=["POST"])
##def filterOpportunities():
# Handle POST requests for filtering opportunities
##json_request_data = request.get_json()


#     if not json_request_data:
#         abort(400)

#     filters = json_request_data.get("filters", None)

#     data = None

#     if filters is None:
#         data = db.session.execute(db.select(Opportunities).limit(20)).scalars()

#     elif not isinstance(filters, list):
#         abort(400)

#     else:

#         where_conditions = []
#         query = (
#             db.select(Opportunities)
#             .where(Opportunities.active == True)
#             .limit(20)
#             .order_by(Opportunities.last_updated)
#             .distinct()
#         )
#         for given_filter in filters:
#             field = given_filter.get("field", None)
#             value = given_filter.get("value", None)

#             if field and value:
#                 field = field.lower()

#                 # Location filter
# if field == "location":
# if value.lower() == "remote":
#                         where_conditions.append(Opportunities.location == "REMOTE")
#                 else:
#                         where_conditions.append(Opportunities.location != "REMOTE")

#                 # Class year filter
#                 elif field == "class_year":
# #                     if not isinstance(value, list):
# #                         abort(400)
# #                     query = query.join(
# #                         RecommendsClassYears,
# #                         Opportunities.id == RecommendsClassYears.opportunity_id,
# #                     ).where(RecommendsClassYears.class_year.in_(value))

# #                 # Credits filter
#                 elif field == "credits":
#                     if not isinstance(value, list):
#                         abort(400)
# #                     credit_conditions = []
# #                     for credit in value:
# #                         if credit == 1:
# #                             credit_conditions.append(Opportunities.one_credit.is_(True))
# #                         elif credit == 2:
# #                             credit_conditions.append(
#                                 Opportunities.two_credits.is_(True)
# #                             )
#                         elif credit == 3:
# #                             credit_conditions.append(
# #                                 Opportunities.three_credits.is_(True)
# #                             )
# #                         elif credit == 4:
# #                             credit_conditions.append(
#                                 Opportunities.four_credits.is_(True)
# #                             )
#                         else:
# #                             abort(400)
#                     where_conditions.append(db.or_(*credit_conditions))

# #                 # Majors filter
# #                 elif field == "majors":
# #                     if not isinstance(value, list):
# #                         abort(400)
# #                     query = query.join(
# #                         RecommendsMajors,
# #                         Opportunities.id == RecommendsMajors.opportunity_id,
# #                     ).where(RecommendsMajors.major_code.in_(value))

# #                 # Departments filter
#                 elif field == "departments":
# #                     if not isinstance(value, list):
# #                         abort(400)
# #                     query = (
# #                         query.join(Leads, Opportunities.id == Leads.opportunity_id)
# #                         .join(LabManager, Leads.lab_manager_id == LabManager.id)
# #                         .where(LabManager.department_id.in_(value))
# #                     )

# #                 # Pay filter
#                 elif field == "pay":
# #                     if not isinstance(value, dict):
# #                         abort(400)
# #                     min_pay = value.get("min")
# #                     max_pay = value.get("max")
# #                     if min_pay is None or max_pay is None:
# #                         abort(400)
# #                     where_conditions.append(Opportunities.pay.between(min_pay, max_pay))

# #                 # Other fields
#                 else:
# #                     try:
# #                         where_conditions.append(
# #                             getattr(Opportunities, field).ilike(f"%{value}%")
# #                         )
# #                     except AttributeError:
# #                         abort(400)

# #         query = query.where(*where_conditions)
# #         data = db.session.execute(query).scalars()

# #     if not data:
# #         abort(404)

# #     result = [opportunity.to_dict() for opportunity in data]

# #     return result


# @main_blueprint.put("/opportunity")
# def changeActiveStatus2():

#     if not request.data:
#         abort(400)

#     json_request_data = request.get_json()

#     if not json_request_data:
#         abort(400)

#     postID = json_request_data.get("id", None)
#     status = json_request_data.get("status", None)

#     if (
#         postID is None
#         or status is None
#         or not isinstance(postID, int)
#         or not isinstance(status, bool)
#     ):
#         abort(400)

#     opportunity = db.first_or_404(
#         db.select(Opportunities).where(Opportunities.id == postID)
#     )
#     opportunity.active = status
#     db.session.commit()
#     return {"msg": "Opportunity updated successfully"}, 200


# @main_blueprint.get("/getOpportunityMeta/<int:id>")
# def getOpportunityMeta(id: int):
#     query = db.session.execute(
#         db.select(
#             Opportunities, RecommendsMajors, RecommendsCourses, RecommendsClassYears
#         )
#         .where(Opportunities.id == id)
#         .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
#         .join(RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id)
#         .join(
#             RecommendsClassYears,
#             RecommendsClassYears.opportunity_id == Opportunities.id,
#         )
#     )
#     data = query.all()
#     print(data)


#     if not data or len(data) == 0:
#         abort(404)

#     dictionary = data[0][0].to_dict()
#     dictionary["semester"] = dictionary["semester"].upper()
#     dictionary["courses"] = set()
#     dictionary["majors"] = set()
#     dictionary["years"] = set()

#     for row in data:
#         dictionary["courses"].add(row[2].course_code)
#         dictionary["majors"].add(row[1].major_code)
#         dictionary["years"].add(row[3].class_year)

#     dictionary["courses"] = list(dictionary["courses"])
#     dictionary["majors"] = list(dictionary["majors"])
#     dictionary["years"] = list(dictionary["years"])

#     for i in range(len(dictionary["years"])):
#         dictionary["years"][i] = str(dictionary["years"][i])

#     dictionary["credits"] = []
#     if dictionary["one_credit"]:
#         dictionary["credits"].append("1")

#     if dictionary["two_credits"]:
#         dictionary["credits"].append("2")

#     if dictionary["three_credits"]:
#         dictionary["credits"].append("3")

#     if dictionary["four_credits"]:
#         dictionary["credits"].append("4")

#     dictionary.pop("one_credit")
#     dictionary.pop("two_credits")
#     dictionary.pop("three_credits")
#     dictionary.pop("four_credits")

#     return {"data": dictionary}

#     abort(500)


# Jobs page
@main_blueprint.get("/getOpportunityCards")
def getOpportunityCards():
    # query database for opportunity
    query = db.session.execute(
        db.select(Opportunities).where(Opportunities.active == True)
    )

    data = query.fetchall()
    # return data in the below format if opportunity is found
    cards = {"data": [packageOpportunityCard(opportunity[0]) for opportunity in data]}

    return cards


# @main_blueprint.get("/getOpportunities")
# def getOpportunities():
# #     # query database for opportunity
#     query = db.session.execute(
#         db.select(Opportunities, Leads, LabManager)
#         .join(Leads, Leads.opportunity_id == Opportunities.id)
#         .join(LabManager, Leads.lab_manager_id == LabManager.id)
#     )
#     data = query.all()
#     print(data[0])

#         # return data in the below format if opportunity is found
#         return {
#             "data": [
#                 packageOpportunity(opportunity[0], opportunity[2])
#                 for opportunity in data
#             ]
#         }

#     abort(500)


@main_blueprint.get("/staff/opportunities/<string:rcs_id>")
def getLabManagerOpportunityCards(rcs_id: str):

    query = (
        db.select(
            Opportunities.id,
            Opportunities.name,
            Opportunities.application_due,
            Opportunities.pay,
            Opportunities.one_credit,
            Opportunities.two_credits,
            Opportunities.three_credits,
            Opportunities.four_credits,
        )
        .join(LabManager, User.lab_manager_id == LabManager.id)
        .join(Leads, Leads.lab_manager_id == LabManager.id)
        .join(Opportunities, Leads.opportunity_id == Opportunities.id)
        .where(User.id == rcs_id)
        .select_from(User)
    )

    data = db.session.execute(query).all()

    cards = {
        "data": [
            {
                "id": row[0],
                "title": row[1],
                "due": row[2].strftime("%-m/%-d/%y"),
                "pay": row[3],
                "credits": format_credits(row[4], row[5], row[6], row[7]),
            }
            for row in data
        ]
    }

    return cards


# @main_blueprint.get("/getProfileOpportunities/<string:rcs_id>")
# def getProfileOpportunities(rcs_id: str):
# #     # query database for opportunity

#     query = db.session.execute(
#         db.select(Opportunities, Leads)
#         .where(Leads.lab_manager_id == rcs_id)
#         .join(Opportunities, Leads.opportunity_id == Opportunities.id)
#     )

#     data = query.all()

#     cards = {"data": []}

#     for row in data:
#         opportunity = row[0]

#         oppData = {
#             "id": opportunity.id,
#             "title": opportunity.name,
#             "body": "Due " + str(opportunity.application_due),
#             "attributes": [],
#             "activeStatus": opportunity.active,
#         }

#         if opportunity.pay is not None and opportunity.pay > 0:
#             oppData["attributes"].append("Paid")
#         if (
#             opportunity.one_credit
#             or opportunity.two_credits
#             or opportunity.three_credits
#             or opportunity.four_credits
#         ):
#             oppData["attributes"].append("Credits")

#         cards["data"].append(oppData)

#     # return data in the below format if opportunity is found
#     return cards


# function to search for lab managers
@main_blueprint.get("/searchLabManagers/<string:query>")
def searchLabManagers(query: str):
    # Perform a search on User table by first name, last name, or email using ILIKE for exact partial matches
    stmt = (
        db.select(User)
        .join(LabManager, User.lab_manager_id == LabManager.id)
        .where(
            (
                User.first_name.ilike(
                    f"%{query}%"
                )  # Case-insensitive partial match on first_name
            )
            | (
                User.last_name.ilike(
                    f"%{query}%"
                )  # Case-insensitive partial match on last_name
            )
            | (
                User.email.ilike(
                    f"%{query}%"
                )  # Case-insensitive partial match on email
   lab_managers = [
        {
            "lab_manager_id": user.lab_manager_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        for user in results
    ]

    return {"lab_managers": lab_managers}, 200

@main_blueprint.get("/searchCourses/<string:query>")
def searchCourses(query: str):
    # Perform a search on Courses table by code and name using ILIKE for exact partial matches
    stmt = (
        db.select(Courses)
        .distinct()
        .where(
            (Courses.code.ilike(f"%{query}%"))
            | (
                User.last_name.ilike(
                    f"%{query}%"
                )  # Case-insensitive partial match on course code
            )
            | (
                Courses.name.ilike(
                    f"%{query}%"
                )  # Case-insensitive partial match on course name
            )
        )
    )

    results = db.session.execute(stmt).scalars().all()

    # Format results as JSON
    courses = [
        {
            "code": course.code,
            "name": course.name,
        }
        for course in results
    ]

    return {"courses": courses}, 200


# functions to create/edit/delete opportunities
@main_blueprint.post("/createOpportunity")
@jwt_required()
def createOpportunity():
    user_id = get_jwt_identity()
    if not request.data or not user_id:
        abort(400)

    request_data = request.get_json()

    if not request_data:
        abort(400)

    author = db.session.execute(
        db.select(User).where(User.email == user_id[0])
    ).scalar_one_or_none()

    if author is None or author.lab_manager_id is None:
        abort(400)

    try:
        pay = int(request_data["hourlyPay"])
    except:
        pay = None

    one = True if "1" in request_data["credits"] else False
    two = True if "2" in request_data["credits"] else False
    three = True if "3" in request_data["credits"] else False
    four = True if "4" in request_data["credits"] else False

    lenum = convert_to_enum(request_data["location"])

    if lenum is None:
        lenum = LocationEnum.TBD

    newOpportunity = Opportunities()
    newOpportunity.name = request_data["title"]
    newOpportunity.description = request_data["description"]
    newOpportunity.recommended_experience = request_data["recommended_experience"]
    newOpportunity.pay = pay
    newOpportunity.one_credit = one
    newOpportunity.two_credits = two
    newOpportunity.three_credits = three
    newOpportunity.four_credits = four
    newOpportunity.semester = SemesterEnum.FALL
    newOpportunity.year = datetime.now().year
    newOpportunity.application_due = datetime.strptime(
        request_data["application_due"], "%Y-%m-%d"
    )
    newOpportunity.active = True
    newOpportunity.location = lenum
    newOpportunity.last_updated = datetime.now()
    db.session.add(newOpportunity)
    db.session.commit()

    newLead = Leads()
    newLead.lab_manager_id = author.lab_manager_id
    newLead.opportunity_id = newOpportunity.id

    db.session.add(newLead)

    for year in request_data["years"]:
        if year.isdigit():
            recommended_year = int(year)
            newYear = RecommendsClassYears()
            newYear.opportunity_id = newOpportunity.id
            newYear.class_year = recommended_year
            db.session.add(newYear)

    db.session.commit()
              
    return {"data": "Opportunity Created", "id": newOpportunity.id}, 200


@main_blueprint.get("/editOpportunity/<int:opportunity_id>")
def editOpportunity_get(opportunity_id):
    opportunity = db.session.execute(
        db.select(Opportunities).where(Opportunities.id == opportunity_id)
    ).first()

    if not opportunity:
        return {"error": "Opportunity not found"}, 404

    opportunity = opportunity[0]

    # Query related courses
    # courses_data = db.session.execute(
    #     db.select(RecommendsCourses.course_code).where(
    #         RecommendsCourses.opportunity_id == opportunity_id
    #     )
    # ).all()

    # Query related majors
    # majors_data = db.session.execute(
    #     db.select(RecommendsMajors.major_code).where(
    #         RecommendsMajors.opportunity_id == opportunity_id
    #     )
    # ).all()

    # Query related class years
    years_data = db.session.execute(
        db.select(RecommendsClassYears.class_year).where(
            RecommendsClassYears.opportunity_id == opportunity_id
        )
    ).all()

    credits = [
        str(i)
        for i, credit in enumerate(
            [
                opportunity.one_credit,
                opportunity.two_credits,
                opportunity.three_credits,
                opportunity.four_credits,
            ],
            start=1,
        )
        if credit
    ]

    years = [str(year.class_year) for year in years_data] if years_data else []

    # Format opportunity data as JSON
    opportunity_data = {
        "id": opportunity.id,
        "title": opportunity.name,
        "application_due": opportunity.application_due.strftime("%Y-%m-%d"),
        "type": (
            "Any"
            if len(credits) > 0 and opportunity.pay and opportunity.pay > 0
            else "For Pay" if opportunity.pay and opportunity.pay > 0 else "For Credit"
        ),
        "hourlyPay": str(opportunity.pay),
        "credits": credits,
        "description": opportunity.description,
        "recommended_experience": opportunity.recommended_experience,
        # "semester": opportunity.semester,  # Convert enum to string
        # "year": opportunity.year,
        # "active": opportunity.active,
        "location": opportunity.location,  # Convert enum to string
        # "last_updated": opportunity.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        # "courses": [course.course_code for course in courses_data],
        # "majors": [major.major_code for major in majors_data],
        "years": years,
    }

    return opportunity_data


@main_blueprint.put("/editOpportunity/<int:opportunity_id>")
@jwt_required()
def editOpportunity(opportunity_id):

    user_id = get_jwt_identity()
    if not request.data or not user_id:
        abort(400)

    request_data = request.get_json()

    if not request_data:
        abort(400)

    # Check if the opportunity and author exist
    opportunity = db.session.execute(
        db.select(Opportunities).where(Opportunities.id == opportunity_id)
    ).scalar_one_or_none()

    if opportunity is None:
        abort(400)

    author = db.session.execute(
        db.select(User).where(User.email == user_id[0])
    ).scalar_one_or_none()

    if author is None or author.lab_manager_id is None:
        abort(400)

    leads = db.session.execute(
        db.select(Leads)
        .where(Leads.opportunity_id == opportunity_id)
        .where(Leads.lab_manager_id == author.lab_manager_id)
    ).scalar_one_or_none()

    if leads is None:
        abort(400)

    try:
        pay = int(request_data["hourlyPay"])
    except:
        pay = None

    one = True if "1" in request_data["credits"] else False
    two = True if "2" in request_data["credits"] else False
    three = True if "3" in request_data["credits"] else False
    four = True if "4" in request_data["credits"] else False

    lenum = convert_to_enum(request_data["location"])

    if lenum is None:
        lenum = LocationEnum.TBD

    # Update fields for opportunity based on the input data
    opportunity.name = request_data["title"]
    opportunity.description = request_data["description"]
    opportunity.recommended_experience = request_data["recommended_experience"]
    opportunity.pay = pay
    opportunity.one_credit = one
    opportunity.two_credits = two
    opportunity.three_credits = three
    opportunity.four_credits = four
    opportunity.application_due = datetime.strptime(
        request_data["application_due"], "%Y-%m-%d"
    )
    # opportunity.active = data["active"]
    opportunity.location = lenum
    opportunity.last_updated = datetime.now()

    existing_years = {
        str(year.class_year)
        for year in db.session.execute(
            db.select(RecommendsClassYears).where(
                RecommendsClassYears.opportunity_id == opportunity_id
            )
        ).scalars()
    }
    new_years = set(request_data["years"])

    # Years to add
    years_to_add = new_years - existing_years
    for year in years_to_add:
        newYear = RecommendsClassYears()
        newYear.opportunity_id = opportunity.id
        newYear.class_year = int(year)
        db.session.add(newYear)

    # Years to remove
    years_to_remove = existing_years - new_years
    if years_to_remove:
        db.session.execute(
            db.select(RecommendsClassYears)
            .where(
                RecommendsClassYears.opportunity_id == opportunity_id,
                RecommendsClassYears.class_year.in_(years_to_remove),
            )
            .delete(synchronize_session=False)
        )

    db.session.commit()

    # Add the updated list of managers
    if "lab_manager_ids" in data:
        for lab_manager_id in data["lab_manager_ids"]:
            new_lead = Leads(
                lab_manager_id=lab_manager_id, opportunity_id=opportunity_id
            )
            db.session.add(new_lead)

    db.session.commit()  # Commit all changes

    return {"data": "Opportunity Updated"}, 200


@main_blueprint.delete("/deleteOpportunity/<int:opportunity_id>")
@jwt_required()
def deleteOpportunity(opportunity_id):
    opportunity = db.session.get(Opportunities, opportunity_id)

    if not opportunity:
        return {"error": "Opportunity not found"}, 404

    # TODO: Add check to see if user has permission to delete opportunity
    user_id = get_jwt_identity()

    user = db.session.execute(
        db.select(User).where(User.email == user_id)
    ).scalar_one_or_none()

    if not user or not user.lab_manager_id:
        return {"error": "Don't have permission to delete!"}, 401

    leads = db.session.execute(
        db.select(Leads)
        .where(Leads.opportunity_id == opportunity_id)
        .where(Leads.lab_manager_id == user.lab_manager_id)
    ).scalar_one_or_none()

    if not leads:
        abort(400)

    # Delete the opportunity
    # cascading delete will handle all other tables
    db.session.delete(opportunity)
    db.session.commit()

    return {"data": "Opportunity Deleted"}
