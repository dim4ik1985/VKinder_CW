import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BotUsers(Base):
    __tablename__ = 'bot_users'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Integer, nullable=False)
    age = sq.Column(sq.String(length=20))
    sex = sq.Column(sq.String(length=2), nullable=False)
    hometown = sq.Column(sq.String(length=50))



class UserSearch(Base):
    __tablename__ = "user_search"

    id = sq.Column(sq.Integer, primary_key=True)
    f_name = sq.Column(sq.String(length=50), nullable=False)
    l_name = sq.Column(sq.String(length=50), nullable=False)
    url_profile = sq.Column(sq.String(length=50), nullable=False)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_users.id"), nullable=False)

    relations_user = relationship(BotUsers, backref="user_search")


class PhotoUsers(Base):
    __tablename__ = "photo_users"

    id = sq.Column(sq.Integer, primary_key=True)
    url_photo = sq.Column(sq.String(length=500), nullable=False)
    users_search_id = sq.Column(sq.Integer, sq.ForeignKey("user_search.id"), nullable=False)

    relations_user_search = relationship(UserSearch, backref="photo_users")


class FavoritesUsers(Base):
    __tablename__ = "favorites_users"
    id = sq.Column(sq.Integer, primary_key=True)
    # url_profile = sq.Column(sq.String(length=50), nullable=False)
    users_relat_id = sq.Column(sq.Integer, sq.ForeignKey("user_search.id"), nullable=False)

    relations_favorites = relationship(UserSearch, backref="favorites_users")


def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
