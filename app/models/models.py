from datetime import date
from sqlalchemy import (
    Column, Integer, String, Date, Text, Enum,
    ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'Role'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey('Role.role_id'))
    role = relationship("Role", back_populates="users")

    borrow_records = relationship("BorrowedRecord", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    reports = relationship("Report", back_populates="generated_by_user")


class Category(Base):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = 'Book'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100))
    category_id = Column(Integer, ForeignKey('Category.category_id'))

    total_copies = Column(Integer, default=0)
    available_copies = Column(Integer, default=0)

    category = relationship("Category", back_populates="books")
    inventory = relationship("Inventory", back_populates="book", uselist=False)
    borrow_records = relationship("BorrowedRecord", back_populates="book")


class Inventory(Base):
    __tablename__ = 'Inventory'

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('Book.book_id'))
    last_checked = Column(Date)
    current_stock = Column(Integer)

    book = relationship("Book", back_populates="inventory")


class BorrowedRecord(Base):
    __tablename__ = 'Borrowed_Record'

    borrow_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    book_id = Column(Integer, ForeignKey('Book.book_id'))

    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(Enum('borrowed', 'returned', 'overdue'), default='borrowed')

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")


class Payment(Base):
    __tablename__ = 'Payment'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_type = Column(String(50))  # e.g., fine, subscription
    payment_date = Column(Date, nullable=False)
    description = Column(Text)

    user = relationship("User", back_populates="payments")


class Report(Base):
    __tablename__ = 'Report'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    report_type = Column(String(100))
    generated_by = Column(Integer, ForeignKey('User.user_id'))
    generated_date = Column(Date)
    description = Column(Text)

    generated_by_user = relationship("User", back_populates="reports")
