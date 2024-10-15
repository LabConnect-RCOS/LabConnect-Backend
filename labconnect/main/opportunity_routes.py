import datetime

from flask import abort, request

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from labconnect import db
from labconnect.models import (
    LabManager,
    Leads,
    Opportunities,
    RecommendsClassYears,
    RecommendsMajors,
    RecommendsCourses,
    User,
)

from labconnect.helpers import LocationEnum

from . import main_blueprint


@main_blueprint.get("/searchOpportunity/<string:query>")
def searchOpportunity(query: str):
    # Perform a search
    stmt = (
        db.select(Opportunities)
        .where(
            (
                Opportunities.search_vector.match(query)
            )  # Full-text search using pre-generated tsvector
            | (
                db.func.similarity(Opportunities.name, query) >= 0.1
            )  # Fuzzy search on the 'name' field
            | (
                db.func.similarity(Opportunities.description, query) >= 0.1
            )  # Fuzzy search on the 'description' field
        )
        .order_by(
            db.func.similarity(
                Opportunities.name, query
            ).desc()  # Order by similarity for fuzzy search results
        )
    )

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
        return LocationEnum[location_string]  # Use upper() for case-insensitivity
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
    print(queryInfo)

    if len(queryInfo) == 0:
        return data

    data["department"] = queryInfo[0][1].department_id

    for i, item in enumerate(queryInfo):
        data["author"] += item[1].getName()
        # data["author"] += "look at def packageIndividualOpportunity(opportunityInfo):"
        if i != len(queryInfo) - 1:
            data["author"] += ", "

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
        db.select(Leads, LabManager)
        .where(Leads.opportunity_id == opportunity.id)
        .join(LabManager, Leads.lab_manager_id == LabManager.id)
    )

    data = query.all()

    professorInfo = ""

    for i, item in enumerate(data):
        professorInfo += item[1].getName()
        if i != len(data) - 1:
            professorInfo += ", "

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


#
@main_blueprint.route("/opportunity/filter", methods=["POST"])
def filterOpportunities():
    # Handle POST requests for filtering opportunities
    json_request_data = request.get_json()


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


# # Jobs page
# @main_blueprint.get("/getOpportunityCards")
# def getOpportunityCards():
# #     # query database for opportunity
#     query = db.session.execute(
#         db.select(Opportunities).where(Opportunities.active == True)
#     )

#     data = query.fetchall()

#         # return data in the below format if opportunity is found
#         cards = {
#             "data": [packageOpportunityCard(opportunity[0]) for opportunity in data]
#         }

#     return cards

#     abort(500)

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

# @main_blueprint.get("/getOpportunityByProfessor/<string:rcs_id>")
# def getOpportunityByProfessor(rcs_id: str):
# #     # query database for opportunity
#     query = db.session.execute(
#         db.select(Opportunities, Leads)
#         .where(Leads.lab_manager_id == rcs_id)
#         .join(Opportunities, Leads.opportunity_id == Opportunities.id)
#     )

#         data = query.all()
#         print(data)

#         # return data in the below format if opportunity is found
#         return {"data": [opportunity[0].to_dict() for opportunity in data]}

#     abort(500)

# @main_blueprint.get("/getProfessorOpportunityCards/<string:rcs_id>")
# def getProfessorOpportunityCards(rcs_id: str):
#
#     # query database for opportunity
#     user = db.first_or_404(db.select(User).where(User.email == rcs_id))

#     query = db.session.execute(
#         db.select(Opportunities, Leads)
#         .where(Leads.lab_manager_id == user.lab_manager_id)
#         .join(Opportunities, Leads.opportunity_id == Opportunities.id)
#     )

#     data = query.all()

#     cards = {"data": []}

#     for row in data:
#         opportunity = row[0]

#         if not opportunity.active:
#             continue

#         oppData = {
#             "id": opportunity.id,
#             "title": opportunity.name,
#             "body": "Due " + str(opportunity.application_due),
#             "attributes": [],
#         }

#         if opportunity.pay is not None and opportunity.pay > 0:
#             oppData["attributes"].append("Paid")

#         if (
#             opportunity.one_credit
#             or opportunity.two_credits
#             or opportunity.three_credits
#             or opportunity.four_credits
#         ):
#             oppData["attributes"].append("Credit Available")

#         cards["data"].append(oppData)

#     # return data in the below format if opportunity is found
#     return cards

#     abort(500)

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

#     abort(500)


# functions to create/edit/delete opportunities
# @main_blueprint.post("/createOpportunity")
# def createOpportunity():
#     # if request.method == "POST":
#     data = request.get_json()
#     authorID = data["authorID"]
#     newPostData = data

#         # query database to see if the credentials above match
#         query = db.session.execute(
#             db.select(LabManager).where(LabManager.id == authorID)
#         )

#     data = query.all()[0][0]

#     # TODO: how do we get the opportunity id?
#     # if match is found, create a new opportunity with the new data provided

#     one = False
#     two = False
#     three = False
#     four = False

#     if "1" in newPostData["credits"]:
#         one = True
#     if "2" in newPostData["credits"]:
#         two = True
#     if "3" in newPostData["credits"]:
#         three = True
#     if "4" in newPostData["credits"]:
#         four = True

#     lenum = convert_to_enum(newPostData["location"])

#     if lenum is None:
#         lenum = LocationEnum.TBD

#     newOpportunity = Opportunities(
#         name=newPostData["name"],
#         description=newPostData["description"],
#         recommended_experience=newPostData["recommended_experience"],
#         pay=newPostData["pay"],
#         one_credit=one,
#         two_credits=two,
#         three_credits=three,
#         four_credits=four,
#         semester=newPostData["semester"],
#         year=newPostData["year"],
#         application_due=datetime.datetime.strptime(
#             newPostData["application_due"], "%Y-%m-%d"
#         ),
#         active=newPostData["active"],
#         location=lenum,
#     )
#     print("before comitting")
#     db.session.add(newOpportunity)
#     db.session.commit()

#     print("got here atleast")

#     newLead = Leads(lab_manager_id=authorID, opportunity_id=newOpportunity.id)

#     db.session.add(newLead)
#     db.session.commit()

#     for course in newPostData["courses"]:
#         newCourse = RecommendsCourses(
#             opportunity_id=newOpportunity.id, course_code=course
#         )
#         db.session.add(newCourse)
#         db.session.commit()

#         for major in newPostData["majors"]:
#             newMajor = RecommendsMajors(
#                 opportunity_id=newOpportunity.id, major_code=major
#             )
#             db.session.add(newMajor)
#             db.session.commit()

#     for year in newPostData["years"]:
#         newYear = RecommendsClassYears(
#             opportunity_id=newOpportunity.id, class_year=year
#         )
#         db.session.add(newYear)
#         db.session.commit()

#     # db.session.add(newOpportunity)

#     return {"data": "Opportunity Created"}

#
# abort(500)


# @main_blueprint.route("/editOpportunity", methods=["DELETE", "POST"])
# def editOpportunity():
#     if True:
#         data = request.get_json()
#         id = data["id"]
#         # authToken = data["authToken"]
#         # authorID = data["authorID"]
#         newPostData = data

#         # query database to see if the credentials above match
#         query = db.session.execute(
#             db.select(
#                 Opportunities, RecommendsMajors, RecommendsCourses, RecommendsClassYears
#             )
#             .where(Opportunities.id == id)
#             .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
#             .join(
#                 RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id
#             )
#             .join(
#                 RecommendsClassYears,
#                 RecommendsClassYears.opportunity_id == Opportunities.id,
#             )
#         )

#         data = query.all()

#         if not data or len(data) == 0:
#             abort(404)

#         opportunity = data[0][0]

#         one = False
#         two = False
#         three = False
#         four = False

#         if "1" in newPostData["credits"]:
#             one = True
#         if "2" in newPostData["credits"]:
#             two = True
#         if "3" in newPostData["credits"]:
#             three = True
#         if "4" in newPostData["credits"]:
#             four = True

#         lenum = convert_to_enum(newPostData["location"])
#         print(newPostData["location"])
#         print("printing lenum")
#         print(lenum)

#         # if match is found, edit the opportunity with the new data provided
#         opportunity.name = newPostData["name"]
#         opportunity.description = newPostData["description"]
#         opportunity.recommended_experience = newPostData["recommended_experience"]
#         opportunity.pay = newPostData["pay"]
#         opportunity.one_credit = one
#         opportunity.two_credits = two
#         opportunity.three_credits = three
#         opportunity.four_credits = four
#         opportunity.semester = newPostData["semester"]
#         opportunity.year = newPostData["year"]
#         opportunity.application_due = datetime.datetime.strptime(
#             newPostData["application_due"], "%Y-%m-%d"
#         )
#         opportunity.active = newPostData["active"]

#         if lenum is not None:
#             opportunity.location = lenum

#         db.session.add(opportunity)
#         db.session.commit()

#         # delete all the old data in the recommends tables

#         for row in data:
#             db.session.delete(row[1])
#             db.session.delete(row[2])
#             db.session.delete(row[3])

#         # create new data for allow the tables

#         for course in newPostData["courses"]:
#             newCourse = RecommendsCourses(
#                 opportunity_id=opportunity.id, course_code=course
#             )
#             db.session.add(newCourse)
#             db.session.commit()

#         for major in newPostData["majors"]:
#             newMajor = RecommendsMajors(opportunity_id=opportunity.id, major_code=major)
#             db.session.add(newMajor)
#             db.session.commit()

#         for year in newPostData["years"]:
#             newYear = RecommendsClassYears(
#                 opportunity_id=opportunity.id, class_year=year
#             )
#             db.session.add(newYear)
#             db.session.commit()

#         return "Successful"

#     abort(500)


# @main_blueprint.route("/deleteOpportunity", methods=["DELETE", "POST"])
# def deleteOpportunity():
#     if request.method in ["DELETE", "POST"]:
#         data = request.get_json()
#         id = data["id"]

#         query = db.session.execute(
#             db.select(
#                 Opportunities,
#                 RecommendsMajors,
#                 RecommendsCourses,
#                 RecommendsClassYears,
#                 Leads,
#             )
#             .where(Opportunities.id == id)
#             .join(RecommendsMajors, RecommendsMajors.opportunity_id == Opportunities.id)
#             .join(
#                 RecommendsCourses, RecommendsCourses.opportunity_id == Opportunities.id
#             )
#             .join(
#                 RecommendsClassYears,
#                 RecommendsClassYears.opportunity_id == Opportunities.id,
#             )
#             .join(Leads, Leads.opportunity_id == Opportunities.id)
#         )

#         data = query.all()
#         print(data)

#         if not data or len(data) == 0:
#             abort(404)

#         opportunity = data[0][0]

#         for row in data:
#             db.session.delete(row[1])
#             db.session.delete(row[2])
#             db.session.delete(row[3])
#             db.session.delete(row[4])

#         leads = data[0][4]

#         db.session.delete(opportunity)

#         db.session.commit()

#         return "Success"

#     abort(500)
