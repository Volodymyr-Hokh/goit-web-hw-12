from datetime import date, timedelta
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactRequest


async def get_contacts(offset: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(offset).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactRequest, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactRequest, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, offset: int, limit: int, db: Session) -> List[Contact] | None:
    contacts = db.query(Contact).filter(Contact.first_name.ilike(query) | Contact.last_name.ilike(
        query) | Contact.email.ilike(query)).offset(offset).limit(limit).all()
    return contacts


async def find_contacts_by_birthday(offset: int, limit: int, db: Session) -> List[Contact] | None:
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(text("TO_CHAR(birthday, 'MM-DD') BETWEEN :start_date AND :end_date")
                                        ).params(start_date=today.strftime('%m-%d'),
                                                 end_date=next_week.strftime('%m-%d')).all()

    return contacts
