from sqlmodel import SQLModel, Session, create_engine
import os


def build_database_url():
    """Build database URL from individual components or use DATABASE_URL if provided."""
    # If DATABASE_URL is provided, use it directly
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")

    # Otherwise, build from individual components
    db_host = os.getenv("DB_HOST", "postgres")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "example")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = build_database_url()
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
