from app.utils.db import SessionLocal
from app.models.models import Book, Category
from models import Book  




        
        

def get_all_books():
    with SessionLocal() as session:
        books = session.query(Book).join(Category).all()
        return [{
            "ID": b.book_id,
            "Title": b.title,
            "Author": b.author,
            "Category": b.category.name if b.category else "None",
            "Available": b.available_copies,
            "Total": b.total_copies
        } for b in books]
    return Book.query.all()


def add_book(title, author, category_id, total, available):
    with SessionLocal() as session:
        book = Book(
            title=title,
            author=author,
            category_id=category_id,
            total_copies=total,
            available_copies=available
        )
        session.add(book)
        session.commit()
