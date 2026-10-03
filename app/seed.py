# Import SQLAlchemy select for checking existing rows.
from sqlalchemy import select

# Import configured settings.
from .config import settings
# Import the database engine and session factory.
from .database import Base, SessionLocal, engine
# Import all editable content models.
from .models import AdminUser, ChurchTheme, FamilyGroup, Leader, Notice, Service
# Import the secure password hasher.
from .security import hash_password


# Create the database tables when the application starts for the first time.
def create_tables():
    # Create every registered model table if it does not exist.
    Base.metadata.create_all(bind=engine)


# Seed useful initial church content without overwriting administrator changes.
def seed_initial_data():
    # Open a database session for the seed operation.
    db = SessionLocal()
    # Guard the seed operation so the session closes correctly.
    try:
        # Create the initial admin account if it does not exist.
        admin = db.scalar(select(AdminUser).where(AdminUser.username == settings.admin_username))
        # Add the configured initial administrator only once.
        if not admin:
            # Create the initial administrator record.
            db.add(
                AdminUser(
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                    is_active=True,
                )
            )

        # Create the current annual theme if no theme exists yet.
        theme = db.scalar(select(ChurchTheme).where(ChurchTheme.is_current.is_(True)))
        # Seed the theme supplied for the current church website.
        if not theme:
            # Add the 2026 church theme requested for the website.
            db.add(
                ChurchTheme(
                    year=2026,
                    title="MEGALEIOS",
                    subtitle="OUR YEAR OF GREAT THINGS",
                    bible_reference="Luke 1:49",
                    description="A year of celebrating God's great works and His faithfulness to His people.",
                    is_current=True,
                )
            )

        # Add representative Sunday service records when the database is empty.
        if not db.scalar(select(Service.id).limit(1)):
            # Add the main Sunday Eucharistic service.
            db.add(
                Service(
                    name="Sunday Divine Service",
                    day="Sunday",
                    time="8:00 AM",
                    topic="Sunday Worship & Holy Communion",
                    bible_reference="See weekly bulletin",
                    description="A reverent Anglican worship service with hymns, Scripture, sermon and Holy Communion.",
                    is_active=True,
                )
            )
            # Add an additional Sunday worship service slot that can be edited from admin.
            db.add(
                Service(
                    name="Sunday Family Service",
                    day="Sunday",
                    time="10:00 AM",
                    topic="Weekly Sunday Topic",
                    bible_reference="See weekly bulletin",
                    description="A family-focused worship gathering. Update the weekly topic and reference from the admin dashboard.",
                    is_active=True,
                )
            )

        # Add a short welcome notice when no notice exists.
        if not db.scalar(select(Notice.id).limit(1)):
            # Create the initial welcome notice.
            db.add(
                Notice(
                    title="Welcome to AAMAC",
                    content="Welcome to Adeyinka Adegbite Memorial Anglican Church. Please check this notice board regularly for current church announcements, events and service updates.",
                    is_published=True,
                )
            )

        # Add leadership placeholders so names remain optional.
        if not db.scalar(select(Leader.id).limit(1)):
            # Add a senior priest placeholder without inventing a personal name.
            db.add(
                Leader(
                    name="Name to be added",
                    title="Vicar / Priest",
                    bio="Church leadership profile can be completed by the administrator.",
                    is_active=True,
                )
            )
            # Add a second priest placeholder.
            db.add(
                Leader(
                    name="Name to be added",
                    title="Assistant Priest",
                    bio="Church leadership profile can be completed by the administrator.",
                    is_active=True,
                )
            )
            # Add a bishop placeholder.
            db.add(
                Leader(
                    name="Name to be added",
                    title="Bishop, Diocese of Ibadan South",
                    bio="The diocesan leadership profile can be completed by the administrator.",
                    is_active=True,
                )
            )

        # Add family-group placeholders without inventing group names or leaders.
        if not db.scalar(select(FamilyGroup.id).limit(1)):
            # Create fourteen editable family group records.
            for number in range(1, 15):
                # Add one family group placeholder for each requested group.
                db.add(
                    FamilyGroup(
                        name=f"Family Group {number}",
                        leader_name="Leader to be added",
                        description="Update this family group from the administrator dashboard.",
                        is_active=True,
                    )
                )

        # Persist all initial records.
        db.commit()
    # Always close the database session.
    finally:
        # Release the database connection.
        db.close()


# Run database setup and initial content seeding when this module is executed directly.
if __name__ == "__main__":
    # Create all database tables defined by the application's models.
    create_tables()

    # Insert the initial administrator and AAMAC website content.
    seed_initial_data()

    # Confirm that the database initialization completed successfully.
    print("AAMAC database initialized and initial data seeded successfully.")
