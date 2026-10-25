from core.database import SessionLocal
from sqlalchemy.orm import Session
from users.models import UserModel
from Books.models import BookModel
from faker import Faker

fake = Faker()

def seed_users(db):
    user = UserModel(user_name = fake.user_name().lower())
    user.set_password('123456')
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def seed_books(db, user, count=10): 
    book_list = []
    for _ in range(count):
        user_id = user.id
        title_of_the_book=fake.sentence().lower()
        author=fake.name().lower()
        if db.query(BookModel).filter_by(title_of_the_book=title_of_the_book, author=author, user_id=user_id).first():
            continue  # Skip if the book already exists for the user
        result = db.query(BookModel).filter_by(title_of_the_book=title_of_the_book, author=author).all()
        # get the last book with the same title and author
        if result:
            new_result = result[-1].number_of_readers + 1
        # Generate a random number of reads for the book
        number_of_reads = fake.random_int(min=0, max=20)
        book_list.append(BookModel(user_id = user_id,
                                   title_of_the_book=title_of_the_book,
                                   author=author,
                                   number_of_readers=new_result if result else 1,
                                   description=fake.text(),
                                   number_of_reads=number_of_reads,
                                   is_completed=False if number_of_reads == 0 else True))
    db.add_all(book_list)
    db.commit()
    return book_list

def main():
    db = SessionLocal()
    try:
        user = seed_users(db)
        seed_books(db, user, count=10)
    finally:
        db.close()

if __name__ == "__main__":
    main()