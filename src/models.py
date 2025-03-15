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
    nickname: Optional[str] = None


    class Config:
        from_attributes = True


class Transaction(BaseModel):
    id: Optional[int] = None
    account_id: int
    date: date
    description: Optional[str] = None
    amount: float
    currency: str
    category: Optional[str] = None
    transaction_type: TransactionType
    transfer_reference_id: Optional[int] = None
    balance_id: Optional[int] = None # applies only to accounts not credit cards

    class Config:
        from_attributes = True


class Balance(BaseModel):
    id: Optional[int] = None
    account_id: int
    date: date
    amount: float

    class Config:
        from_attributes = True
