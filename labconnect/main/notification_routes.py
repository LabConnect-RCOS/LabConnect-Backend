from flask import Response, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from labconnect import db
from labconnect.models import Notifications, User

from . import main_blueprint


@main_blueprint.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications() -> Response:
    # Get all user notifications
    user_email = get_jwt_identity()
    user = db.session.execute(
        db.select(User).where(User.email == user_email)
    ).scalar_one_or_none()

    if not user:
        return {"msg": "User not found"}, 404

    notifications = (
        db.session.execute(
            db.select(Notifications)
            .where(Notifications.user_id == user.id)
            .order_by(Notifications.created_at.desc())
        )
        .scalars()
        .all()
    )

    results = []
    for notif in notifications:
        results.append(
            {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "type": notif.notification_type.value,
                "is_read": notif.is_read,
                "created_at": notif.created_at.isoformat(),
                "related_entity_id": notif.related_entity_id,
            }
        )

    return jsonify(results)
