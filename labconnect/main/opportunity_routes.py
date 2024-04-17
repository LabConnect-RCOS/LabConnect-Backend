from flask import abort, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)

from labconnect import db
from labconnect.models import (
    LabManager,
    Leads,
    Opportunities,
    RecommendsClassYears,
    RecommendsMajors,
)

from . import main_blueprint

# @main_blueprint.get("/opportunity")
# def getOpportunity():
#     if not request.data:
#         abort(400)

#     id = request.get_json().get("id", None)

#     if not id:
#         abort(400)

#     data = db.first_or_404(db.select(Opportunities).where(Opportunities.id == id))

#     result = data.to_dict()

#     return result


@main_blueprint.get("/opportunity/filter")
def filterOpportunities():

    if not request.data:
        abort(400)

    json_request_data = request.get_json()

    if not json_request_data:
        abort(400)

    filters = json_request_data.get("filters", None)

    data = None

    if filters is None:
        data = db.session.execute(db.select(Opportunities).limit(20)).scalars()

    elif not isinstance(filters, list):
        abort(400)

    else:

        where_conditions = []
        query = (
            db.select(Opportunities)
            .where(Opportunities.active == True)
            .limit(20)
            .order_by(Opportunities.last_updated)
            .distinct()
        )
        for filter in filters:
            field = filter.get("field", None)
            value = filter.get("value", None)

            if field and value:

                field = field.lower()

                if field == "location" and value.lower() == "remote":
                    where_conditions.append(Opportunities.location == "REMOTE")

                elif field == "location":
                    where_conditions.append(Opportunities.location != "REMOTE")

                elif field == "class_year":

                    if not isinstance(value, list):
                        abort(400)

                    query = query.join(
                        RecommendsClassYears,
                        Opportunities.id == RecommendsClassYears.opportunity_id,
                    ).where(RecommendsClassYears.class_year.in_(value))

                elif field == "credits":

                    if not isinstance(value, list):
                        abort(400)

                    credit_conditions = []

                    for credit in value:

                        if credit == 1:
                            credit_conditions.append(Opportunities.one_credit == True)
                        elif credit == 2:
                            credit_conditions.append(Opportunities.two_credits == True)
                        elif credit == 3:
                            credit_conditions.append(
                                Opportunities.three_credits == True
                            )
                        elif credit == 4:
                            credit_conditions.append(Opportunities.four_credits == True)
                        else:
                            abort(400)

                    query = query.where(db.or_(*credit_conditions))

                elif field == "majors":

                    if not isinstance(value, list):
                        abort(400)

                    query = query.join(
                        RecommendsMajors,
                        Opportunities.id == RecommendsMajors.opportunity_id,
                    ).where(RecommendsMajors.major_code.in_(value))

                elif field == "departments":

                    if not isinstance(value, list):
                        abort(400)

                    query = (
                        query.join(Leads, Opportunities.id == Leads.opportunity_id)
                        .join(LabManager, Leads.lab_manager_rcs_id == LabManager.rcs_id)
                        .where(LabManager.department_id.in_(value))
                    )

                elif field == "pay":

                    if not isinstance(value, dict):
                        abort(400)

                    min_pay = value.get("min", None)
                    max_pay = value.get("max", None)

                    if min_pay is None or max_pay is None:
                        abort(400)

                    where_conditions.append(Opportunities.pay.between(min_pay, max_pay))

                else:
                    try:
                        where_conditions.append(
                            getattr(Opportunities, field).ilike(f"%{value}%")
                        )
                    except AttributeError:
                        abort(400)

        query = query.where(*where_conditions)
        data = db.session.execute(query).scalars()

    if not data:
        abort(404)

    result = [opportunity.to_dict() for opportunity in data]

    return result


# @main_blueprint.delete("/opportunity")
# def deleteOpportunity():

#     id = request.get_json().get("id", None)

#     if not id:
#         abort(400)

#     db.session.execute(db.delete(Opportunities).where(Opportunities.id == id))

#     return 202


# @main_blueprint.put("/opportunity")
# def changeActiveStatus():
#     if request.method in ["DELETE", "POST"]:
#         data = request.get_json()
#         postID = data["postID"]
#         authToken = data["authToken"]
#         authorID = data["authToken"]
#         setStatus = data["setStatus"]

#         # query database to see if the credentials above match

#         # if match is found, change the opportunities active status to true or false based on setStatus

#         abort(200)

#     abort(500)
