from module import db
from module import db, login_manager
from module import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    phone_number = db.Column(db.String(length=12), nullable=False, unique=True)
    points = db.Column(db.Integer(), nullable=False, default=254)


    @property
    def prettier_budget(self):
        if len(str(self.points)) >= 4:
            return f'{str(self.points)[:-3]},{str(self.points)[-3:]} points'
        else:
            return f"{self.points} points"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    code = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    quantity = db.Column(db.Integer())
    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(length=12), nullable=False)
    confirmed = db.Column(db.String(length=1), nullable=False, default='N')
    room_type = db.Column(db.String(length=30), nullable=False)

    def __repr__(self):
        return f'<DateRange {self.start_date} to {self.end_date} for User ID {self.first_name} {self.last_name}>'
    
class Facilities(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    code = db.Column(db.String(length=12), nullable=False, unique=True)
    end_date = db.Column(db.Date, nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    def __repr__(self):
        return f'Facilities {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.String(), default='Anonymous')
    def __repr__(self):
        return f'Comment {self.owner}'

class Dish(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    dishtype = db.Column(db.String(length=30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    def __repr__(self):
        return f'Dishes {self.name}'
    
class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.String(), default='Anonymous')
    def __repr__(self):
        return f'Comment {self.owner}'
    
class Offers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    code = db.Column(db.String(length=12), nullable=False, unique=True)
    end_date = db.Column(db.Date, nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    def __repr__(self):
        return f'Facilities {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    phone_number = db.Column(db.String(length=12), nullable=False, unique=True)

    @property
    def prettier_budget(self):
        if len(str(self.points)) >= 4:
            return f'{str(self.points)[:-3]},{str(self.points)[-3:]} points'
        else:
            return f"{self.points} points"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price