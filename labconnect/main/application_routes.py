from flask import Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from labconnect import db
from labconnect.models import Applications, Opportunities, User

from . import main_blueprint


@main_blueprint.route("/opportunity/<int:opportunity_id>/apply", methods=["POST"])
@jwt_required()
def apply_to_opportunity(opportunity_id: int) -> Response:
    # User applies to opportunity
    user_email = get_jwt_identity()
    user = db.session.execute(
        db.select(User).where(User.email == user_email)
    ).scalar_one_or_none()

    if not user:
        return {"msg": "User not found"}, 404

    opportunity = db.session.get(Opportunities, opportunity_id)
    if not opportunity:
        return {"msg": "Opportunity not found"}, 404

    new_application = Applications(
        user_id=user.id,
        opportunity_id=opportunity.id,
    )

    try:
        db.session.add(new_application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"msg": "Already Applied."}, 409

    return {"msg": "Application Submitted."}, 201
