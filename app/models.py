# Import SQLAlchemy column types and ORM helpers.
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

# Import the shared declarative base.
from .database import Base


# Store administrator login credentials.
class AdminUser(Base):
    # Map this model to the administrator table.
    __tablename__ = "admin_users"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the administrator username.
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # Store only a secure password hash.
    password_hash: Mapped[str] = mapped_column(String(255))
    # Store whether this administrator can still sign in.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Store when the administrator was created.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# Store church announcements and notices entered by administrators.
class Notice(Base):
    # Map this model to the notices table.
    __tablename__ = "notices"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the notice title.
    title: Mapped[str] = mapped_column(String(200))
    # Store the full notice content.
    content: Mapped[str] = mapped_column(Text)
    # Store an optional call-to-action URL.
    link_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Store an optional call-to-action label.
    link_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Store whether the notice is visible publicly.
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    # Store the date/time the notice was created.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# Store Sunday and other worship services.
class Service(Base):
    # Map this model to the services table.
    __tablename__ = "services"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the service name.
    name: Mapped[str] = mapped_column(String(150))
    # Store the service day.
    day: Mapped[str] = mapped_column(String(50))
    # Store the service time.
    time: Mapped[str] = mapped_column(String(50))
    # Store the weekly service topic when applicable.
    topic: Mapped[str | None] = mapped_column(String(250), nullable=True)
    # Store the Bible reference when applicable.
    bible_reference: Mapped[str | None] = mapped_column(String(250), nullable=True)
    # Store additional service details.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Store whether the service is visible on the public website.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# Store the annual church theme.
class ChurchTheme(Base):
    # Map this model to the theme table.
    __tablename__ = "church_themes"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the theme year.
    year: Mapped[int] = mapped_column(Integer, unique=True)
    # Store the theme title or keyword.
    title: Mapped[str] = mapped_column(String(200))
    # Store the theme subtitle.
    subtitle: Mapped[str] = mapped_column(String(300))
    # Store the theme Bible reference.
    bible_reference: Mapped[str] = mapped_column(String(200))
    # Store optional explanatory text.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Store whether this is the current theme.
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)


# Store priest and leadership information without requiring photographs.
class Leader(Base):
    # Map this model to the leaders table.
    __tablename__ = "leaders"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the person's display name when the church chooses to publish it.
    name: Mapped[str] = mapped_column(String(200))
    # Store the person's title.
    title: Mapped[str] = mapped_column(String(200))
    # Store optional biography text.
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Store optional image path.
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Store whether this leader is publicly visible.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# Store the fourteen family groups and their leaders.
class FamilyGroup(Base):
    # Map this model to the family groups table.
    __tablename__ = "family_groups"

    # Store the primary key.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Store the family group name.
    name: Mapped[str] = mapped_column(String(200))
    # Store the family group leader's name.
    leader_name: Mapped[str] = mapped_column(String(200))
    # Store optional family group description.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Store whether the family group is publicly visible.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
