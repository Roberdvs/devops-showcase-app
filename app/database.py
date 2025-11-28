from sqlmodel import SQLModel, Session, create_engine
import os


def build_database_url_and_kwargs():
    """
    Build database URL and engine kwargs based on environment.
    - If USE_SQLITE=true, use SQLite (file or memory)
    - If DATABASE_URL is set, use it
    - Otherwise, build PostgreSQL URL from components
    Returns: (url, kwargs)
    """
    if os.getenv("USE_SQLITE", "false").lower() == "true":
        sqlite_path = os.getenv("SQLITE_PATH", ":memory:")
        if sqlite_path == ":memory:":
            url = "sqlite://"
        else:
            url = f"sqlite:///{sqlite_path}"
        kwargs = {"connect_args": {"check_same_thread": False}}
        return url, kwargs
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL"), {}
    db_host = os.getenv("DB_HOST", "postgres")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "example")
    url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return url, {}


DATABASE_URL, ENGINE_KWARGS = build_database_url_and_kwargs()
engine = create_engine(DATABASE_URL, echo=True, **ENGINE_KWARGS)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
