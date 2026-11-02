from fastapi.testclient import TestClient
from main import app
from core.database import Base, create_engine, sessionmaker, get_db
from sqlalchemy import StaticPool
import pytest
from faker import Faker
from users.models import UserModel
from Books.models import BookModel

fake = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope = 'package')
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope = 'module', autouse = True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)

@pytest.fixture(scope = 'session', autouse = True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind = engine)
    yield
    Base.metadata.drop_all(bind = engine)

@pytest.fixture(scope = 'function')
def anon_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope = 'package', autouse = True)
def generate_mock_data(db_session):
    user = UserModel(user_name = "usertest")
    user.set_password("12345678910")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    print(f"user created, username: {user.user_name}, ID: {user.id}")

    book_list = []
    for _ in range (12):
        user_id = user.id
        title_of_the_book=fake.sentence().lower()
        author=fake.name().lower()
        number_of_reads = fake.random_int(min=0, max=20)
        book_list.append(BookModel(user_id = user_id,
                                   title_of_the_book=title_of_the_book,
                                   author=author,
                                   number_of_readers= 1,
                                   description=fake.text(),
                                   number_of_reads=number_of_reads,
                                   is_completed=False if number_of_reads == 0 else True))
    db_session.add_all(book_list)
    db_session.commit()
    print(f'added 12 books for user with ID: {user.id}')