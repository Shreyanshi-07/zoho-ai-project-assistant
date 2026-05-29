from sqlmodel import Session, select

from app.models.user_token import UserToken
from app.services.database import engine


def get_current_user():

    with Session(engine) as session:

        statement = select(UserToken).where(
            UserToken.user_id == "shreyanshi"
        )

        return session.exec(statement).first()