from module import app
from flask import url_for, redirect, render_template, request, session, flash
from datetime import datetime
from module.models import Item, User, Reservation, Offers
from module.forms import RegisterForm, LoginForm, BookForm
from module import db
from flask_login import login_user, logout_user, login_required, current_user
from module.admin import admin1 as admin

app.register_blueprint(admin, url_prefix="/admin")


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html', items=Item)

@app.route("/dining")
def dining():
    return render_template('dining.html')

@app.route("/offers")
def offer():
    offer = Offers.query.all()
    return render_template('offer.html', offer=offer)

@app.route("/accomodation")
def accomodation():
    items = Item.query.all()
    return render_template('accomodation.html', items=Item)

@app.route('/book', methods=["POST", "GET"])
def book():
    # Fetch room types from the database
    room_types = Item.query.all()
    
    # Prepare choices for SelectField where value and label are both room_type.name
    choices = [(room_type.name) for room_type in room_types]

    # Instantiate the form
    form = BookForm()
    # Set choices dynamically
    form.room_type.choices = choices
    items = Item.query.all()
    selected_item = request.form.get('roomtype')
    print (selected_item)
    if form.validate_on_submit():
        reservation_to_create = Reservation(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                room_type=form.room_type.data,
                              start_date=form.start_date.data,
                              end_date=form.end_date.data,
                              phone_number=form.phone_number.data)
        db.session.add(reservation_to_create)
        db.session.commit()
        flash(f"Booking Queue created successfully! You will be contacted to confirm your booking.", category='success')
        return redirect(url_for('user'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while booking: {err_msg}', category='danger')

    return render_template('book.html', form=form, items=items)

@app.route("/wellness")
def wellness():
    return render_template('wellness.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/eventsandcorporate")
def corporate():
    return render_template('corporate.html')

@app.route("/user")
def user():
    if "user" in session:
        user_name = session["user"]
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            flash('User not found', category='danger')
            return redirect(url_for('login'))
        phone = user.phone_number
        reservation = Reservation.query.filter_by(phone_number=phone).all()
        return render_template('user.html', user_name=user, reservation=reservation, Item=Item)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            session.permanent = True
            session["user"] = attempted_user.username
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('user'))
        else:
            if "user" in session:
                return redirect(url_for('user'))
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              phone_number=form.phone_number.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('user'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route("/my_reservations")
def my_reservation():
    return render_template('blank.html')