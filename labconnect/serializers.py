from labconnect.models import Courses, Opportunities
from labconnect.helpers import format_credits


def serialize_course(course: Courses) -> str:
    return f"{course.code} {course.name}"


def serialize_opportunity(
    opportunity: Opportunities, professor: str = "", saved: bool = False
) -> dict:
    return {
        "id": opportunity.id,
        "name": opportunity.name,
        "description": opportunity.description,
        "recommended_experience": opportunity.recommended_experience,
        "pay": opportunity.pay,
        "credits": format_credits(
            opportunity.one_credit,
            opportunity.two_credits,
            opportunity.three_credits,
            opportunity.four_credits,
        ),
        "semester": opportunity.semester,
        "year": opportunity.year,
        "application_due": opportunity.application_due,
        "active": opportunity.active,
        "last_updated": opportunity.last_updated,
        "location": opportunity.location,
        "professor": professor,
        "saved": saved,
    }
