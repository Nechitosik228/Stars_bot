from .config import Config
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Member(Config.BASE):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]

    
    


# + name: str
# + telegram_id: int
# + role_id: int
# + group_id: int
