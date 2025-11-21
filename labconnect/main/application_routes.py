import os

from flask import Response, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from labconnect import db
from labconnect.models import Applications, Opportunities, User

from . import main_blueprint


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "pdf",
        "doc",
        "docx",
    }


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

    resume_url = None
    if "resume" in request.files:
        file = request.files["resume"]
        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(
                    f"{user.id}_{opportunity.id}_{file.filename}"
                )

                upload_folder = os.path.join(
                    current_app.root_path, "static", "uploads", "resumes"
                )
                os.makedirs(upload_folder, exist_ok=True)

                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                resume_url = f"/static/uploads/resumes/{filename}"
            else:
                return {"msg": "Invalid file type. Allowed: PDF, DOC, DOCX"}, 400

    new_application = Applications(
        user_id=user.id, opportunity_id=opportunity.id, resume_url=resume_url
    )

    try:
        db.session.add(new_application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"msg": "Already Applied."}, 409

    return {"msg": "Application Submitted."}, 201


@main_blueprint.route("/profile/applications", methods=["GET"])
@jwt_required()
def get_my_applications() -> Response:
    # Get list of all applications by User
    user_email = get_jwt_identity()
    user = db.session.execute(
        db.select(User).where(User.email == user_email)
    ).scalar_one_or_none()

    if not user:
        return {"msg": "User not found"}, 404

    applications = (
        db.session.execute(
            db.select(Applications)
            .where(Applications.user_id == user.id)
            .order_by(Applications.applied_on.desc())
        )
        .scalars()
        .all()
    )

    results = []
    for app in applications:
        results.append(
            {
                "application_id": app.id,
                "opportunity_id": app.opportunity_id,
                "opportunity_name": app.opportunity.name,
                "status": app.status.value,
                "applied_on": app.applied_on.isoformat(),
                "resume_url": app.resume_url,
            }
        )

    return jsonify(results)
