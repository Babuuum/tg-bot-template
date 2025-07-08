from sqlmodel import SQLModel, Field
from datetime import datetime

class TgUser(SQLModel, table=True):
    id:          int         = Field(primary_key=True)
    username:    str | None  = Field(index=True, default=None)
    first_name:  str | None  = None
    joined_at:   datetime    = Field(default_factory=datetime.utcnow)