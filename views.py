from datetime import datetime

from flask import current_app, render_template, request, redirect, url_for, session, flash

from tables import database as d

from flask_session import Session


import functools
import operator

"""Log In Page"""

from passlib.hash import pbkdf2_sha256
from forms import LoginForm
from user import get_user

from flask_login import LoginManager, login_user, logout_user

def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def create_contact_page():
    if request.method == "GET":
        return render_template("create_contact.html")
    else:
        contact_name = request.form["contact_name"]
        contact_surname = request.form["contact_surname"]
        contact_email = request.form["contact_email"]
        contact_number = request.form["contact_number"]
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.crete_contact(contact_name, contact_surname, contact_email, contact_number, user_id[0][0])
        flash("Contact is created successfully")
        return redirect(url_for("create_contact_page"))

def contacts_page():
    db = current_app.config["db"]
    if request.method == "GET":
        contacts = db.get_contacts()
        i = 0
        for contact in contacts:
            contacts[i] = list(contacts[i])
            contacts[i][0] = db.get_human(contact[0])[0][0]
            i = i + 1
        return render_template("contact.html", contacts= contacts)
    else:
        form_contact_keys = request.form.getlist("deletes")
        for form_contact_key in form_contact_keys:
            db.delete_contacts(db.get_contact_id(form_contact_key)[0][0],1)
        flash("You deleted some of the contacts")
        return redirect(url_for("contacts_page"))
##############################################################
def create_interview_page():
    if request.method == "GET":
        return render_template("create_interview.html")
    else:
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        comment = request.form["comment"]
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.crete_interview(date_from, date_to, user_id[0][0])
        flash("Interview is created successfully")
        return redirect(url_for("create_interview_page"))

def interviews_page():
    db = current_app.config["db"]
    if request.method == "GET":
        interviews = db.get_interviews()
        i = 0
        for interview in interviews:
            interviews[i] = list(interviews[i])
            interviews[i][0] = db.get_human(interview[0])[0][0]
            print(interviews[i][0])
            i = i + 1
        return render_template("interview.html", interviews= interviews)
    else:
        form_interview_keys = request.form.getlist("deletes")
        for form_interview_key in form_interview_keys:
            db.delete_interviews(db.get_interview_id(form_interview_key)[0][0],1)
        flash("You deleted some of your interviews")
        return redirect(url_for("interviews_page"))


def create_event_page():
    if request.method == "GET":
        return render_template("create_event.html")
    else:
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        comment = request.form["comment"]
        status = request.form["status"]
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_event(date_from, date_to, comment, status, user_id[0][0])
        flash("Event is created successfully")
        return redirect(url_for("create_event_page"))

def events_page():
    db = current_app.config["db"]
    if request.method == "GET":
        events = db.get_events()
        i = 0
        for event in events:
            events[i] = list(events[i])
            events[i][0] = db.get_human(event[0])[0][0]
            i = i + 1
        return render_template("event.html", events= events)

    else:
        form_event_keys = request.form.getlist("deletes")
        for form_event_key in form_event_keys:
            db.delete_events(db.get_event_id(form_event_key)[0][0],1)
        flash("You deleted some of your events")
        return redirect(url_for("events_page"))

def create_role_page():
    if request.method == "GET":
        return render_template("create_role.html")
    else:
        surname = request.form["surname"]
        email = request.form["email"]
        number = request.form["number"]
        event_quota = request.form["event_quota"]
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_role(surname,email,number, event_quota, user_id[0][0])
        flash("System Role is created")
        return redirect(url_for("create_role_page"))

def roles_page():
    db = current_app.config["db"]
    if request.method == "GET":
        roles = db.get_roles()
        i = 0
        for role in roles:
            roles[i] = list(roles[i])
            roles[i][0] = db.get_human(role[0])[0][0]
            i = i+1
        return render_template("role.html", roles = roles)
    else:
        form_role_keys = request.form.getlist("deletes")
        for form_role_key in form_role_keys:
            db.delete_roles(db.get_role_id(form_role_key)[0][0],1)
        flash("You deleted some of your roles")
        return redirect(url_for("roles_page"))

def signup_page():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.data["name"]
        password = form.data["password"]
        next_page = request.args.get("next", url_for("login_page"))
        db = current_app.config["db"]
        db.create_human(name,pbkdf2_sha256.hash(password))
        flash("You signed up into our website")
        return redirect(next_page)
    flash("Invalid credentials.")
    return render_template("signup.html", form=form)

def signout_page():
    db = current_app.config["db"]
    name = session.get('user_id', 'not set')
    user_id = db.get_user_id(name)
    db.delete_human(user_id[0][0])
    flash("You are no longer a user of this site :(")
    return redirect(url_for("home_page"))

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.data["name"]
        user = get_user(name)
        if user is not None:
            password = form.data["password"]
            if pbkdf2_sha256.verify(password, user.password[0][0] ):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)

def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))