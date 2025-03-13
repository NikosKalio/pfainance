from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class InstitutionType(str, Enum):
    BANK = "bank"
    CREDIT_UNION = "credit_union"
    INVESTMENT = "investment"
    INSURANCE = "insurance"
    OTHER = "other"


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"
    MORTGAGE = "mortgage"
    OTHER = "other"


class OwnershipType(str, Enum):
    PERSONAL = "personal"
    JOINT = "joint"
    BUSINESS = "business"


class TransactionType(str, Enum):
    PAYMENT = "payment"
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Institution(BaseModel):
    id: Optional[int] = None
    name: str
    type: InstitutionType

    class Config:
        from_attributes = True


class Account(BaseModel):
    id: Optional[int] = None
    institution_id: int
    account_number: str
    type: AccountType
    currency: str
    holder_name: str
    ownership: OwnershipType

    class Config:
        from_attributes = True


class Transaction(BaseModel):
    id: Optional[int] = None
    account_id: int
    date: date
    description: str
    amount: float
    currency: str
    balance_after: float
    category: str
    transaction_type: TransactionType
    transfer_reference_id: Optional[int] = None

    class Config:
        from_attributes = True


class Balance(BaseModel):
    id: Optional[int] = None
    account_id: int
    date: date
    amount: float

    class Config:
        from_attributes = True
