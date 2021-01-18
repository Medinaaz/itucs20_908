from flask import Flask, session ,current_app, render_template, request, redirect, url_for, flash
from datetime import datetime
from message import sendmessage, sendmessageicon, sendmessagetitle, msg
import views
from flask_session import Session
import time
from flask_login import LoginManager, login_user, logout_user
from user import get_user

from tables import database as d
from passlib.hash import pbkdf2_sha256
from forms import LoginForm, SignUpForm

lm = LoginManager()

app = Flask(__name__)

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

app.config.from_object("settings")

@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

# SIGN UP PAGE

@app.route("/signup",methods=["GET", "POST"])
def signup_page():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.data["name"]
        password = form.data["password"]
        next_page = request.args.get("next", url_for("login_page"))
        db = current_app.config["db"]
        db.create_human(name, pbkdf2_sha256.hash(password))
        flash("You signed up")
        return redirect(next_page)
    flash("Invalid credentials.")
    return render_template("signup.html", form=form)

# LOGIN PAGE
@app.route("/login",methods=["GET", "POST"])
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

# CREATE A CONTACT
@app.route("/createcontact", methods=["GET","POST"])
def create_contact_page():
    if request.method == "GET":
        return render_template("create_contact.html")
    else:
        contact_name = request.form['contact_name']
        contact_surname = request.form['contact_surname']
        contact_email = request.form['contact_email']
        contact_number = request.form['contact_number']
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_contact(contact_name, contact_surname, contact_email, contact_number, user_id[0][0])
        flash("Contact is created successfully")
        return redirect(url_for("create_contact_page"))

# LIST CONTACTS, DELETE CONTACT
@app.route("/contacts", methods =["GET", "POST"])
def contacts_page():
    db = current_app.config["db"]
    if request.method == "GET":
        contacts = db.get_contact()
        i = 0
        for contact in contacts:
            contacts[i] = list(contacts[i])
            contacts[i][0] = db.get_human(contact[0])[0][0]
            i = i+1
        return render_template("contact.html", contacts = contacts)
    else:
        form_contact_keys = request.form.getlist("deletes")
        for form_contact_key in form_contact_keys:
            db.delete_contacts(db.get_contact_id(form_contact_key)[0][0],1)
        flash("You deleted some of your contacts")
        return redirect(url_for("contacts_page"))

# CREATE AN INTERVIEW
@app.route("/createinterview", methods=["GET","POST"])
def create_interview_page():
    if request.method == "GET":
        return render_template("create_interview.html")
    else:
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        comment = request.form['comment']
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_interview(date_from, date_to, comment, user_id[0][0])
        flash("Interview is created successfully")
        return redirect(url_for("create_interview_page"))

# LIST INTERVIEWS AND SHOW UP NOTIFICATIONS FOR THE INTERVIEWS THAT ARE IN THE CURRENT MONTH
# DELETE INTERVIEWS
@app.route("/interviews", methods =["GET", "POST"])
def interviews_page():
    db = current_app.config["db"]
    notif_list = []

    today = datetime.today()
    today_month = today.month
    print("Today's month",today_month)

    if request.method == "GET":
        interviews = db.get_interview()
        i = 0
        j = 0
        number_of_interviews = len(interviews)
        while j<number_of_interviews:
              print("Months",interviews[j][1].month)
              if(today_month==interviews[j][1].month):
                sendmessage("You have new notifications!!")
                icons = ['face-glasses']
                sendmessageicon(interviews[j][3], icons[0])
                time.sleep(0.3)
                notif_list.append(interviews[j][3])
              j=j+1
        print("To print", notif_list[0])
       # print("To print", notif_list[1])
        print(len(interviews))

        for interview in interviews:
            interviews[i] = list(interviews[i])
            interviews[i][0] = db.get_human(interview[0])[0][0]
            i = i+1
        return render_template("interview.html", interviews = interviews)
    else:
        form_interview_keys = request.form.getlist("deletes")
        for form_interview_key in form_interview_keys:
            db.delete_interviews(db.get_interview_id(form_interview_key)[0][0],1)
        flash("You deleted some of your interviews")
        return redirect(url_for("interviews_page"))

# CREATE EVENTS
@app.route("/createevent", methods=["GET","POST"])
def create_event_page():
    if request.method == "GET":
        return render_template("create_event.html")
    else:
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        comment = request.form['comment']
        status = request.form['status']
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_event(date_from, date_to, comment, status,user_id[0][0])
        flash("Event is created successfully")
        return redirect(url_for("create_event_page"))

# LIST EVENTS, DELETE EVENTS
@app.route("/events", methods =["GET", "POST"])
def events_page():
    db = current_app.config["db"]
    if request.method == "GET":
        events = db.get_event()
        i = 0
        for event in events:
            events[i] = list(events[i])
            events[i][0] = db.get_human(event[0])[0][0]
            i = i+1
        return render_template("event.html", events = events)
    else:
        form_event_keys = request.form.getlist("deletes")
        for form_event_key in form_event_keys:
            db.delete_events(db.get_event_id(form_event_key)[0][0],1)
        flash("You deleted some of your events")
        return redirect(url_for("events_page"))

# CREATE A USER ROLE
@app.route("/createrole", methods=["GET","POST"])
def create_role_page():
    if request.method == "GET":
        return render_template("create_role.html")
    else:
        surname = request.form['surname']
        email = request.form['email']
        number = request.form['number']
        event_quota = request.form['event_quota']
        name = session.get('user_id','not set')
        db = current_app.config["db"]
        user_id = db.get_user_id(name)
        db.create_role(surname, email, number,event_quota,user_id[0][0])
        flash("Role is created successfully")
        return redirect(url_for("create_role_page"))

# LIST USER ROLES, DELETE
@app.route("/roles", methods =["GET", "POST"])
def roles_page():
    db = current_app.config["db"]
    if request.method == "GET":
        roles = db.get_role_()
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

# UPDATE A CONTACT
def update_contact_profile(contact_id, contact_name, contact_surname, contact_email, contact_number):
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement =  """UPDATE CONTACTS SET
                    CONTACT_NAME = (%(id)s),
                    CONTACT_SURNAME = (%(id)s),
                    CONTACT_EMAIL = (%(id)s),
                    CONTACT_NUMBER = (%(id)s),
                    WHERE CONTACT_ID = (%(id)s)
                    """
    cursor.execute(statement, [contact_name, contact_surname, contact_email, contact_number])
    connection.commit()
    cursor.close()
    connection.close()
    return

# UPDATE AN EVENT
def update_event_profile(event_id, date_from, date_to, comment, status):
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement =  """UPDATE EVENTS SET
                    DATE_FROM = (%(id)s),
                    DATE_TO = (%(id)s),
                    COMMENT = (%(id)s),
                    STATUS = (%(id)s),
                    WHERE EVENT_ID = (%(id)s)
                    """
    cursor.execute(statement, [date_from, date_to, comment, status])
    connection.commit()
    cursor.close()
    connection.close()
    return

# UPDATE AN INTERVIEW
def update_interview_profile(interview_id, date_from, date_to, comment):
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement =  """UPDATE INTERVIEWS SET
                    DATE_FROM = (%(id)s),
                    DATE_TO = (%(id)s),
                    COMMENT = (%(id)s),
                    WHERE INTERVIEW_ID = (%(id)s)
                    """
    cursor.execute(statement, [date_from, date_to, comment])
    connection.commit()
    cursor.close()
    connection.close()
    return

# UPDATE ROLE
def update_role_profile(role_id, surname, email, number, event_quota):
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement =  """UPDATE ROLES SET
                    SURNAME = (%(id)s),
                    EMAIL = (%(id)s),
                    NUMBER = (%(id)s),
                    EVENT_QUOTA = (%(id)s),
                    WHERE ROLE_ID = (%(id)s)
                    """
    cursor.execute(statement, [surname, email, number, event_quota])
    connection.commit()
    cursor.close()
    connection.close()
    return

# logout page
@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

 # signout page
@app.route("/signout")
def signout_page():
    db = current_app.config["db"]
    name = session.get('user_id', 'not set')
    user_id = db.get_user_id(name)
    db.delete_human(user_id[0][0])
    logout_user()
    flash("User account deleted")
    return redirect(url_for("home_page"))

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

app.config["DEBUG"] = True
lm.init_app(app)
lm.login_view = "login_page"

db = d()
app.config["db"] = db
#Session(app)

if __name__ == "__main__":
   # app = create_app()
    app.run()