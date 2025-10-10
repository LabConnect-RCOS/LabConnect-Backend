from datetime import datetime

from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import case, func

from labconnect import db
from labconnect.helpers import (
    LocationEnum,
    SemesterEnum,
    convert_to_enum,
    format_credits,
)
from labconnect.models import (
    Courses,
    LabManager,
    Leads,
    Opportunities,
    Participates,
    RecommendsClassYears,
    RecommendsMajors,
    User,
    UserSavedOpportunities,
)
from labconnect.serializers import serialize_opportunity

from . import main_blueprint


def opportunity_to_dict(opportunity: Opportunities) -> dict:
    """Return a plain dict representation of an Opportunities model instance."""
    if opportunity is None:
        return {}

    return {
        "id": opportunity.id,
        "name": opportunity.name,
        "description": opportunity.description,
        "recommended_experience": opportunity.recommended_experience,
        "pay": opportunity.pay,
        "one_credit": bool(opportunity.one_credit),
        "two_credits": bool(opportunity.two_credits),
        "three_credits": bool(opportunity.three_credits),
        "four_credits": bool(opportunity.four_credits),
        "semester": str(opportunity.semester) if opportunity.semester is not None else None,
        "year": opportunity.year,
        "active": bool(opportunity.active),
    }

# Single opportunity endpoints used by the frontend/tests
@main_blueprint.get("/opportunity/<int:opportunity_id>")
def get_single_opportunity(opportunity_id: int):
    """Return a single opportunity by id. Returns 404 if not found
    """
    opp = db.session.get(Opportunities, opportunity_id)
    if not opp:
        abort(404)

    return opportunity_to_dict(opp)


@main_blueprint.get("/opportunity")
def get_opportunity_via_json():
    """GET /opportunity expects a JSON payload with {"id": <int>}."""
    data = request.get_json()
    if not data:
        abort(400)

    if "id" not in data:
        abort(400)

    try:
        opp_id = int(data["id"])
    except ValueError:
        abort(400)

    opp = db.session.get(Opportunities, opp_id)
    if not opp:
        abort(404)

    return opportunity_to_dict(opp)


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

    results = [serialize_opportunity(opportunity) for opportunity in data]

    return results


def packageIndividualOpportunity(opportunityInfo):
    data = {
        "id": opportunityInfo.id,
        "name": opportunityInfo.name,
        "description": opportunityInfo.description,
        "recommended_experience": opportunityInfo.recommended_experience,
        "authors": "",
        "department": "",
        "pay": opportunityInfo.pay,
        "credits": None,
        "semester": f"{opportunityInfo.semester} {opportunityInfo.year}",
        "application_due": opportunityInfo.application_due,
        "recommended_class_years": "",
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

    if opportunity_credits != "":
        data["credits"] = opportunity_credits

    # get professor and department by getting Leads and LabManager

    query = db.session.execute(
        db.select(Leads, LabManager, User)
        .where(Leads.opportunity_id == opportunityInfo.id)
        .join(LabManager, Leads.lab_manager_id == LabManager.id)
        .join(User, LabManager.id == User.lab_manager_id)
    )

    queryInfo = query.all()

    if len(queryInfo) == 0:
        return data

    data["department"] = queryInfo[0][1].department_id

    author_info = [
        [item[2].first_name + " " + item[2].last_name, item[2].id] for item in queryInfo
    ]

    data["authors"] = author_info

    if len(queryInfo) > 1:
        data["authorProfile"] = (
            "https://t4.ftcdn.net/jpg/03/78/40/51/360_F_378405187_PyVLw51NVo3KltNlhUOpKfULdkUOUn7j.jpg"
        )
    elif len(queryInfo) == 1:
        data["authorProfile"] = (
            "https://cdn-icons-png.flaticon.com/512/1077/1077114.png"
        )

    return data


@main_blueprint.get("/getOpportunity/<int:opp_id>")
def getOpportunity(opp_id: int):
    # query database for opportunity and recommended class years
    query = db.session.execute(
        db.select(
            Opportunities,
            # Creates an array for all of the recommended class years for the
            # opportunity labeled recommended_years
            func.array_agg(RecommendsClassYears.class_year).label("recommended_years"),
        )
        .join(
            RecommendsClassYears,
            Opportunities.id == RecommendsClassYears.opportunity_id,
        )
        .where(Opportunities.id == opp_id)
        .group_by(Opportunities.id)
    )

    data = query.all()

    # check if opportunity exists
    if not data or len(data) == 0:
        abort(404)

    data = data[0]
    oppData = packageIndividualOpportunity(data[0])
    oppData["recommended_class_years"] = data[1]

    # return data in the below format if opportunity is found
    return {"data": oppData}


@main_blueprint.get("/opportunity/filter")
@jwt_required()
def filterOpportunities():
    # Handle GET requests for filtering opportunities using query parameters
    filters = request.args.to_dict(flat=False)
    user_id = get_jwt_identity()
    data = None

    query = (
        db.select(
            Opportunities,
            func.json_agg(
                func.json_build_object(
                    "first_name",
                    User.first_name,
                    "last_name",
                    User.last_name,
                    "preferred_name",
                    User.preferred_name,
                )
            ).label("lab_managers"),
            case((UserSavedOpportunities.user_id.isnot(None), True), else_=False).label(
                "is_saved"
            ),
        )
        .join(Leads, Opportunities.id == Leads.opportunity_id)
        .join(LabManager, Leads.lab_manager_id == LabManager.id)
        .join(User, LabManager.id == User.lab_manager_id)
        .outerjoin(
            RecommendsMajors, Opportunities.id == RecommendsMajors.opportunity_id
        )
        .outerjoin(
            UserSavedOpportunities,
            db.and_(
                Opportunities.id == UserSavedOpportunities.opportunity_id,
                UserSavedOpportunities.user_id == user_id,  # filter for current user
            ),
        )
        .where(Opportunities.active)
        .group_by(Opportunities.id, UserSavedOpportunities.user_id)
        .order_by(Opportunities.last_updated)
        .limit(20)
    )

    if filters is not None or filters != {}:
        where_conditions = []
        for field, value in filters.items():
            if field and value:
                field = field.lower()
                value = value[0].split(",")

                # Location filter
                # not in use yet
                if field == "location":
                    for location in value:
                        if location.lower() == "remote":
                            where_conditions.append(Opportunities.location == "REMOTE")
                        else:
                            where_conditions.append(Opportunities.location != "REMOTE")

                # Class year filter
                elif field == "years":
                    if not isinstance(value, list):
                        abort(400)
                    years = list(map(int, filter(str.isdigit, value)))
                    if len(years) == 0:
                        abort(400)
                    query = query.join(
                        RecommendsClassYears,
                        Opportunities.id == RecommendsClassYears.opportunity_id,
                    ).where(RecommendsClassYears.class_year.in_(years))

                # Credits filter
                elif field == "credits":
                    if not isinstance(value, list):
                        abort(400)
                    credit_conditions = []
                    for credit in value:
                        if credit == "1":
                            credit_conditions.append(Opportunities.one_credit.is_(True))
                        elif credit == "2":
                            credit_conditions.append(
                                Opportunities.two_credits.is_(True)
                            )
                        elif credit == "3":
                            credit_conditions.append(
                                Opportunities.three_credits.is_(True)
                            )
                        elif credit == "4":
                            credit_conditions.append(
                                Opportunities.four_credits.is_(True)
                            )
                        else:
                            abort(400)
                    where_conditions.append(db.or_(*credit_conditions))

                # Majors filter
                elif field == "majors":
                    if not isinstance(value, list):
                        abort(400)
                    where_conditions.append(RecommendsMajors.major_code.in_(value))

                # Departments filter
                # not currently in use
                elif field == "departments":
                    if not isinstance(value, list):
                        abort(400)
                    query = (
                        query.join(Leads, Opportunities.id == Leads.opportunity_id)
                        .join(LabManager, Leads.lab_manager_id == LabManager.id)
                        .where(LabManager.department_id.in_(value))
                    )

                # Pay filter
                elif field == "hourlypay":
                    pay = value[0]
                    try:
                        pay = float(pay)
                    except ValueError:
                        abort(400)
                    where_conditions.append(Opportunities.pay >= float(pay))

                # Other fields
                else:
                    try:
                        where_conditions.append(
                            getattr(Opportunities, field).ilike(f"%{value}%")
                        )
                    except AttributeError:
                        abort(400)

        query = query.where(*where_conditions)

    data = db.session.execute(query).all()

    if not data:
        abort(404)

    result = [
        serialize_opportunity(
            opportunity[0],
            lab_managers=", ".join(
                [
                    f"{name.get('preferred_name', None) or name.get('first_name')} "
                    f"{name.get('last_name')}"
                    for name in opportunity[1]
                ]
            ),
            saved=opportunity[2],
        )
        for opportunity in data
    ]

    return result


@main_blueprint.get("/staff/opportunities/<string:rcs_id>")
def getLabManagerOpportunityCards(rcs_id: str) -> list[dict[str, str]]:
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

    cards = [
        {
            "id": row[0],
            "title": row[1],
            "due": row[2].strftime("%-m/%-d/%y"),
            "pay": row[3],
            "credits": format_credits(row[4], row[5], row[6], row[7]),
        }
        for row in data
    ]

    return cards


@main_blueprint.get("/profile/opportunities/<string:rcs_id>")
@jwt_required()
def getProfileOpportunities(rcs_id: str) -> list[dict[str, str]]:
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
        .join(Participates, Participates.user_id == rcs_id)
        .join(Opportunities, Participates.opportunity_id == Opportunities.id)
        .where(User.id == rcs_id)
        .select_from(User)
    )

    data = db.session.execute(query).all()

    cards = [
        {
            "id": row[0],
            "title": row[1],
            "due": row[2].strftime("%-m/%-d/%y"),
            "pay": row[3],
            "credits": format_credits(row[4], row[5], row[6], row[7]),
        }
        for row in data
    ]

    return cards


# function to search for lab managers
@main_blueprint.get("/searchLabManagers/<string:query>")
def searchLabManagers(query: str):
    # Perform a search on User table by first name, last name, or email using ILIKE
    # for exact partial matches
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
            )
        )
    )

    results = db.session.execute(stmt).scalars().all()

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
    # Perform a search on Courses table by code and
    # name using ILIKE for exact partial matches
    # TODO: merge into filtering
    stmt = (
        db.select(Courses)
        .distinct()
        .where(
            (Courses.code.ilike(f"%{query}%"))
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
    except ValueError:
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

    years = [str(year.class_year) for year in years_data]
    # if years_data else []

    # Format opportunity data as JSON
    opportunity_data = {
        "id": opportunity.id,
        "title": opportunity.name,
        "application_due": opportunity.application_due.strftime("%Y-%m-%d"),
        "type": (
            "Any"
            if len(credits) > 0 and opportunity.pay and opportunity.pay > 0
            else "For Pay"
            if opportunity.pay and opportunity.pay > 0
            else "For Credit"
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
    except ValueError:
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

    # data is causing errors
    # Add the updated list of managers
    # if "lab_manager_ids" in data:
    #     for lab_manager_id in data["lab_manager_ids"]:
    #         new_lead = Leads(
    #             lab_manager_id=lab_manager_id, opportunity_id=opportunity_id
    #         )
    #         db.session.add(new_lead)

    # Atttempt to fix by replacing data with request_data
    # Add the updated list of managers
    if "lab_manager_ids" in request_data:
        for lab_manager_id in request_data["lab_manager_ids"]:
            new_lead = Leads()
            new_lead.lab_manager_id = lab_manager_id
            new_lead.opportunity_id = opportunity_id
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


# ////////////////////////////////////////////////
# Store opportunities saved by a user
# ***Specificaly storing a individual users saved opportunities***


# Save User Opportunity


@main_blueprint.post("/saveUserOpportunity/<int:opportunity_id>")
@jwt_required()
def saveUserOpportunity(opportunity_id):
    data = request.get_json()
    if not data:
        abort(400, "Missing JSON data")

    save_opp_opportunity_id = db.session.get(Opportunities, opportunity_id)
    if not save_opp_opportunity_id:
        return {"error": "Opportunity not found"}, 404

    save_opp_user_id = get_jwt_identity()

    # Check if the opportunity already exists in saved opportunities
    find_opp = db.session.execute(
        db.select(UserSavedOpportunities).where(
            (UserSavedOpportunities.user_id == save_opp_user_id)
            & (UserSavedOpportunities.opportunity_id == save_opp_opportunity_id)
        )
    ).scalar_one_or_none()

    if find_opp:
        return {"message": "Opportunity already saved"}, 200

    # Save the new opportunity
    new_opp = UserSavedOpportunities()
    new_opp.user_id = save_opp_user_id
    new_opp.opportunity_id = save_opp_opportunity_id

    db.session.add(new_opp)
    db.session.commit()

    return {"message": "Opportunity saved successfully"}, 201


# Delete an opportunitiy saved by a user
@main_blueprint.delete("/deleteUserOpportunity/<int:opportunity_id>")
@jwt_required()
def deleteUserOpportunity(opportunity_id):
    data = request.get_json()
    if not data:
        abort(400, "Missing JSON data")

    save_opp_user_id = get_jwt_identity()
    save_opp_opportunity_id = db.session.get(Opportunities, opportunity_id)
    if not save_opp_opportunity_id:
        return {"error": "Opportunity not found"}, 404

    # Find the saved opportunity
    get_saved_opp_info = db.session.execute(
        db.select(UserSavedOpportunities).where(
            (UserSavedOpportunities.user_id == save_opp_user_id)
            & (UserSavedOpportunities.opportunity_id == save_opp_opportunity_id)
        )
    ).scalar_one_or_none()

    if not get_saved_opp_info:
        return {"message": "Opportunity not found"}, 404

    # Delete the opportunity
    db.session.delete(get_saved_opp_info)
    db.session.commit()

    return {"message": "Opportunity deleted"}, 200


# Create route to return a list saved opportunities
@main_blueprint.get("/AllSavedUserOpportunities/")
@jwt_required()
def allSavedUserOportunities():
    # Get current users ID
    user_id = get_jwt_identity()

    # Get all saved opportunities for the user
    saved_opps = (
        db.session.execute(
            db.select(UserSavedOpportunities).where(
                UserSavedOpportunities.user_id == user_id
            )
        )
        .scalars()
        .all()
    )
    if not saved_opps:
        return {"message": "No saved opportunities found"}, 404

    # Put opportunities into a dictionary
    saved_opportunities_list = [opp.to_dict() for opp in saved_opps]

    return saved_opportunities_list, 200


# Create route to allow for multiple pages to be unsaved given a list of opp_ids
@main_blueprint.delete("/UnsaveMultiplePages/")
@jwt_required()
# Delete id that appear on delete_ids list
def UnsaveMultipleOpps():
    # Get a list of opportunity IDs
    data = request.get_json()
    delete_ids = data.get("delete_ids")
    if not delete_ids or not isinstance(delete_ids, list):
        return {"message": "Invalid or missing delete_ids"}, 400

    # Get opportunities to delete for current user
    user_id = get_jwt_identity()
    saved_opps = (
        db.session.execute(
            db.select(UserSavedOpportunities).where(
                UserSavedOpportunities.user_id == user_id,
                UserSavedOpportunities.opportunity_id.in_(delete_ids),
            )
        )
        .scalars()
        .all()
    )
    if not saved_opps:
        return {"message": "User has no saved opportunities"}, 404

    # Delete the opportinities
    for opp in saved_opps:
        db.session.delete(opp)

    db.session.commit()
    return {"message": f"Deleted {len(saved_opps)} saved opportunities"}, 200
