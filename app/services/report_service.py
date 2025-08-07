from app.utils.db import SessionLocal
from app.models.models import Report


def get_all_reports():
    with SessionLocal() as session:
        reports = session.query(Report).all()
        return [{
            "ID": r.report_id,
            "Type": r.report_type,
            "By": r.generated_by_user.name if r.generated_by_user else "Unknown",
            "Date": r.generated_date,
            "Description": r.description
        } for r in reports]
