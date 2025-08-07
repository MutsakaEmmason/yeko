from app.utils.db import SessionLocal
from app.models.models import BorrowedRecord


def get_all_borrowed_records():
    with SessionLocal() as session:
        records = session.query(BorrowedRecord).all()
        return [{
            "ID": r.borrow_id,
            "User": r.user.name,
            "Book": r.book.title,
            "Borrow Date": r.borrow_date,
            "Due Date": r.due_date,
            "Return Date": r.return_date or "Not Returned",
            "Status": r.status
        } for r in records]
