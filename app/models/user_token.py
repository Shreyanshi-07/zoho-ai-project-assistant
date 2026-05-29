from datetime import datetime
from sqlmodel import SQLModel, Field

class UserToken(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    access_token: str
    refresh_token: str
    expires_at: datetime
    portal_id: str
