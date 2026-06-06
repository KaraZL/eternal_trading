from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.book import Book
    from app.models.collateral import Collateral

'''
Type checking avoid copilot to ask for import of Client, Book, Collateral in the top of the file, which would create circular imports.
'''

class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    client_id: Mapped[str] = mapped_column(String, ForeignKey("clients.id"), nullable=False)
    book_id: Mapped[str] = mapped_column(String, ForeignKey("books.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="loan")
    book: Mapped["Book"] = relationship("Book", back_populates="loan")
    collateral_items: Mapped[list["Collateral"]] = relationship("Collateral", back_populates="loan", cascade="all, delete-orphan")

    '''
    ForeignKey(...) creates the database relationship between the Loan table and the Client and Book tables.
    client_id VARCHAR NOT NULL REFERENCES clients(id)

    The relationship(...) function is used to define the ORM-level relationship between the Loan model and the Client and Book models.
        -> This allows you to easily access the related Client and Book objects from a Loan instance, and vice versa.
        The back_populates parameter is used to specify the name of the attribute on the related model that will be used to access the relationship in the opposite direction.
    
    Exp: SQLAlchemy loads rows where Collateral.loan_id == Loan.id. (since it is specified as a ForeignKey in the Collateral model)
    '''

