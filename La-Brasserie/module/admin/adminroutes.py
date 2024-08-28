from flask import render_template, url_for, redirect, flash, abort, session
from module.admin import admin1
from module.models import Item, User, Reservation, Facilities, Offers, Admin
from module.forms import ItemForm, OffersForm, FacilitiesForm, LoginForm
from module import db
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


def cost(start, end, room):
    room = Item.query.filter_by(name=room).first()
    if room is None:
        return "Not Available"

    # Step 3: Calculate the difference
    difference = (end - start).days
    return room.price * difference

@admin1.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Admin.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            session.permanent = True
            session["user"] = attempted_user.username
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('admin.user'))
        else:
            if "user" in session:
                return redirect(url_for('user'))
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('adminlogin.html', form=form)

@admin1.route("/dashboard")
def dashboard():
    if "user" in session:
        reservations = Reservation.query.filter_by(confirmed='N').all()
        return render_template("adminhome.html", reservations=reservations, cost=cost)
    return redirect(url_for('admin.login_page'))

@admin1.route("/users")
def user():
    if "user" in session:
        profile = User.query.all()
        return render_template("adminusers.html", profile=profile)
    return redirect(url_for('admin.login_page'))

@admin1.route("/roomsandfacilities")
def facilities():
    if "user" in session:
        items = Item.query.all()
        facilities = Facilities.query.all()
        offers = Offers.query.all()
        return render_template("adminfacilities.html", items=items, Facilities=facilities, offers=offers)
    return redirect(url_for('admin.login_page'))

@admin1.route("/bookings")
def bookings():
    if "user" in session:
        reservations = Reservation.query.filter_by(confirmed='Y').all()
        return render_template("adminbookings.html", reservations=reservations, cost=cost)
    return redirect(url_for(login_page))

@admin1.route("/add", methods=['GET', 'POST'])
def add():
        if "user" in session:
            print ("here")
            offers = OffersForm()
            item = ItemForm()
            facilities = FacilitiesForm()
            reservations = Reservation.query.filter_by(confirmed='Y').all()

            if offers.validate_on_submit():
                print('here 1')
                create = Offers(name=offers.name.data,
                                description=offers.description.data,
                                code=offers.code.data,
                                end_date=offers.end_date.data,
                                price=offers.price.data)
                db.session.add(create)
                db.session.commit()
                flash(f"Added successfully!", category='success')
                return redirect(url_for('admin.user'))

            elif facilities.validate_on_submit():
                create1 = Facilities(name=facilities.name.data,
                                    description=facilities.description.data,
                                    code=facilities.code.data,
                                    end_date=facilities.end_date.data,
                                    price=facilities.price.data)
                db.session.add(create1)
                db.session.commit()
                flash(f"Added successfully!", category='success')
                return redirect(url_for('admin.user'))

            elif item.validate_on_submit():
                create2 = Item(name=item.name.data,
                            description=item.description.data,
                            code=item.code.data,
                            end_date=item.end_date.data,
                            price=item.price.data)
                db.session.add(create2)
                db.session.commit()
                flash(f"Added successfully!", category='success')
                return redirect(url_for('admin.user'))

            if offers.errors != {} or item.errors != {} or facilities.errors != {}:
                print("!!here")
                for err_msg in offers.errors.values():
                    flash(f'There was an error with creating an offer: {err_msg}', category='danger')
                for err_msg in item.errors.values():
                    flash(f'There was an error with creating an item: {err_msg}', category='danger')
                for err_msg in facilities.errors.values():
                    flash(f'There was an error with creating a facility: {err_msg}', category='danger')

            return render_template("adminadd.html", reservations=reservations, offer=offers, item=item, facilities=facilities)
        return redirect(url_for('admin.login_page'))
        

@admin1.route('/confirm_reservation/<int:reservation_id>', methods=['POST'])
def confirm_reservation(reservation_id):
    if "user" in session:
        # Query the specific reservation by ID
        reservation = Reservation.query.get(reservation_id)
        if reservation is None:
            flash('Reservation was not confirmed!', 'warning')
            abort(404)
        
        # Update the 'confirmed' column to 'Y'
        reservation.confirmed = 'Y'
        point = cost(reservation.start_date, reservation.end_date, reservation.room_type)/100
        person = User.query.filter_by(phone_number=reservation.phone_number).first()
        person.points += point
        db.session.commit()

        # Flash a success message (optional)
        flash('Reservation confirmed successfully!', 'success')

        # Redirect back to the original page (or any other page)
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for(login_page))

@admin1.route('/delete_facility/<int:reservation_id>', methods=['POST'])
def delete_facility(reservation_id):
    if "user" in session:
        # Query the specific reservation by ID
        reservation = Facilities.query.get(reservation_id)
        if reservation is None:
            flash('Facility was not deleted!', 'warning')
            abort(404)
        
        to_delete = reservation
        db.session.delete(to_delete)
        db.session.commit()

        # Flash a success message (optional)
        flash('Deleted successfully!', 'success')

        # Redirect back to the original page (or any other page)
        return redirect(url_for('admin.facilities'))

@admin1.route('/delete_offers/<int:reservation_id>', methods=['POST'])
def delete_offers(reservation_id):
    if "user" in session:
        # Query the specific reservation by ID
        reservation = Offers.query.get(reservation_id)
        if reservation is None:
            flash('Facility was not deleted!', 'warning')
            abort(404)
        
        to_delete = reservation
        db.session.delete(to_delete)
        db.session.commit()

        # Flash a success message (optional)
        flash('Deleted successfully!', 'success')

        # Redirect back to the original page (or any other page)
        return redirect(url_for('admin.facilities'))
    return redirect(url_for(login_page))

@admin1.route('/delete_item/<int:reservation_id>', methods=['POST'])
def delete_item(reservation_id):
    if "user" in session:
        # Query the specific reservation by ID
        reservation = Item.query.get(reservation_id)
        if reservation is None:
            flash('Facility was not deleted!', 'warning')
            abort(404)
        
        to_delete = reservation
        db.session.delete(to_delete)
        db.session.commit()

        # Flash a success message (optional)
        flash('Deleted successfully!', 'success')

        # Redirect back to the original page (or any other page)
        return redirect(url_for('admin.facilities'))
    return redirect(url_for(login_page))


@admin1.route('/logout')
def logout():
    if "user" in session:
        logout_user()
        flash("You have been logged out!", category='info')
        session.pop("user", None)
        return redirect(url_for("admin.login_page"))
    return redirect(url_for(login_page))