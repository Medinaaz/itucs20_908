import psycopg2 as dbapi2
from datetime import datetime

url = "postgres://dkzczqkr:A9DqgGng3sZrPhRCTldrz1LVx9ADuvBr@dumbo.db.elephantsql.com:5432/dkzczqkr"

class database:
	def __init__(self):
		self.is_a_try = 1

	def delete_all(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """
					DROP TABLE HUMANS;
					DROP TABLE EVENTS;
					DROP TABLE ROLES;
					DROP TABLE INTERVIEWS;
					DROP TABLE CONTACTS;
					"""
		cursor.execute(statement)
		connection.commit()
		cursor.close()
		connection.close()
		return

	def create_tables(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """CREATE TABLE IF NOT EXISTS HUMANS(
							HUMAN_ID SERIAL PRIMARY KEY,
							NAME VARCHAR(30),
							PASSWORD VARCHAR(1000) NOT NULL,
							ROLE VARCHAR(6),
							DATE DATE
						);
					CREATE TABLE IF NOT EXISTS ROLES(
							ROLE_ID SERIAL PRIMARY KEY,
							SURNAME VARCHAR(30),
							EMAIL VARCHAR(50),
							NUMBER VARCHAR(30),
							EVENT_QUOTA INTEGER,
							UNIQUE(EMAIL),
							ROLE_WHICH INTEGER REFERENCES HUMANS(HUMAN_ID)
						);
						CREATE TABLE IF NOT EXISTS CONTACTS(
							CONTACT_ID SERIAL PRIMARY KEY,
							CONTACT_NAME VARCHAR(30) NOT NULL,
							CONTACT_SURNAME VARCHAR(30) NOT NULL,
							CONTACT_EMAIL VARCHAR(20),
							CONTACT_NUMBER VARCHAR(20),
							CONTACT_ID_WHICH INTEGER REFERENCES HUMANS(HUMAN_ID)
						);
						CREATE TABLE IF NOT EXISTS INTERVIEWS(
							INTERVIEW_ID SERIAL PRIMARY KEY,
							DATE_FROM DATE,
							DATE_TO DATE,
							COMMENT TEXT,
							INTERVIEW_ID_WHICH INTEGER REFERENCES HUMANS(HUMAN_ID)
						);
						CREATE TABLE IF NOT EXISTS EVENTS(
							EVENT_ID SERIAL PRIMARY KEY,
							DATE_FROM DATE,
							DATE_TO DATE,
							COMMENT TEXT,
							STATUS VARCHAR(20),
							EVENT_ID_WHICH INTEGER REFERENCES HUMANS(HUMAN_ID)
						);
							"""
		cursor.execute(statement)
		connection.commit()
		cursor.close()
		connection.close()
		return

	def create_human(self, name, password):
		
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		today = datetime.today()

		statement = """INSERT INTO HUMANS (NAME, PASSWORD,ROLE, DATE)
						VALUES (%s, %s, %s, %s)
							"""
		cursor.execute(statement, [name, password, "user", today])
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_password(self, name):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT PASSWORD FROM HUMANS
					WHERE(NAME=(%(id)s))
						   """
		cursor.execute(statement, {'id': name})
		password = cursor.fetchall()
		cursor.close()
		connection.close()
		return password

	def get_role(self, name):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT ROLE FROM HUMANS
					WHERE (NAME = (%(id)s))
							"""

		cursor.execute(statement, {'id': name})
		role = cursor.fetchall()
		if(role == "admin"):
			bool_admin = True
		bool_admin = False
		cursor.close()
		connection.close()
		return bool_admin

	def get_user_id(self, name):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT HUMAN_ID FROM HUMANS
					WHERE (NAME=(%(id)s))
					        """
		cursor.execute(statement, {'id':name})
		user_id = cursor.fetchall()
		cursor.close()
		connection.close()
		return user_id

	def get_human(self, id):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT NAME FROM HUMANS
					WHERE (HUMAN_ID = (%(id)s))
							"""
		cursor.execute(statement, {'id':id})
		person = cursor.fetchall()
		cursor.close()
		connection.close()
		return person

	def get_humans(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT PASSWORD, NAME, DATE FROM HUMANS
							"""

		cursor.execute(statement)
		humans = cursor.fetchall()
		cursor.close()
		connection.close()
		return humans

	def delete_human(self, id):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		database.delete_roles(self, id, 0)
		database.delete_contacts(self, id, 0)
		database.delete_interviews(self, id, 0)
		database.delete_events(self, id, 0)

		statement = """DELETE FROM HUMANS
						WHERE (HUMAN_ID = (%(id)s))
							"""
		cursor.execute(statement, {'id':id})
		connection.commit()
		cursor.close()
		connection.close()
		return

	############ CONTACT

	def create_contact(self, contact_name, contact_surname, contact_email, contact_number, which):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		today = datetime.today()

		statement = """INSERT INTO CONTACTS (CONTACT_NAME, CONTACT_SURNAME, CONTACT_EMAIL, CONTACT_NUMBER, CONTACT_ID_WHICH)
						VALUES (%s, %s, %s, %s, %s)
							"""
		cursor.execute(statement, [contact_name, contact_surname, contact_email,contact_number, which])
		connection.commit()
		cursor.close()
		connection.close()
		return


	def get_contact(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT CONTACT_ID_WHICH, CONTACT_NAME, CONTACT_SURNAME, CONTACT_EMAIL, CONTACT_NUMBER FROM CONTACTS
							"""
		cursor.execute(statement)
		contacts = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return contacts

	def delete_contacts(self, id, check):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		if(check == 0):
			statement = """DELETE FROM CONTACTS
						WHERE (CONTACT_ID_WHICH = (%(id)s))
							"""
		else:
			statement = """DELETE FROM CONTACTS
						WHERE (CONTACT_ID = (%(id)s))
							"""
		cursor.execute(statement, {'id': id})
		connection.commit()
		cursor.close()
		connection.close()
		return

#
#
# 	def get_contacts(self):
# 		connection = dbapi2.connect(url)
# 		cursor = connection.cursor()
#
# 		statement = """SELECT CONTACT_NAME, CONTACT_SURNAME, CONTACT_EMAIL, CONTACT_NUMBER, CONTACT_ID_WHICH FROM CONTACTS
# 							"""
# 		cursor.execute(statement)
# 		contacts = cursor.fetchall()
# 		connection.commit()
# 		cursor.close()
# 		connection.close()
# 		return contacts

	def get_contact_id(self, contact):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT CONTACT_ID FROM CONTACTS
						WHERE (CONTACT_NAME = (%(id)s))
							"""

		cursor.execute(statement, {'id': contact})
		contact_id = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return contact_id

####### INTERVIEWS
	def create_interview(self, date_from, date_to, comment,which):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """INSERT INTO INTERVIEWS (DATE_FROM, DATE_TO, COMMENT, INTERVIEW_ID_WHICH)
							VALUES (%s, %s, %s, %s)

								"""

		cursor.execute(statement ,[date_from, date_to, comment, which])
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_interview(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT INTERVIEW_ID_WHICH, DATE_FROM, DATE_TO, COMMENT FROM INTERVIEWS
							"""

		cursor.execute(statement)
		interviews = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return interviews

	def delete_interviews(self, id, check):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		if(check == 0):
			statement = """DELETE FROM INTERVIEWS
						WHERE (INTERVIEW_ID_WHICH = (%(id)s))
							"""

		else:
			statement = """DELETE FROM INTERVIEWS
						WHERE (INTERVIEW_ID = (%(id)s))
							"""

		cursor.execute(statement, {'id':id})
		connection.commit()
		cursor.close()
		connection.close()
		return 

	def get_interview_id(self, interview):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT INTERVIEW_ID FROM INTERVIEWS
						WHERE (COMMENT = (%(id)s))
							"""
		cursor.execute(statement, {'id' : interview})
		interview_id = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return interview_id

	######## EVENTS

	def create_event(self, date_from, date_to, comment, status, which):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		today = datetime.today()

		statement = """INSERT INTO EVENTS (DATE_FROM, DATE_TO, COMMENT, STATUS, EVENT_ID_WHICH)
						VALUES (%s, %s, %s, %s, %s)
							"""
		cursor.execute(statement, [date_from, date_to, comment, status,which])
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_event(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT EVENT_ID_WHICH, DATE_FROM, DATE_TO, COMMENT, STATUS FROM EVENTS
							"""
		cursor.execute(statement)
		events = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return events

	def delete_events(self, id, check):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		if(check == 0):
			statement = """DELETE FROM EVENTS
						WHERE (EVENT_ID_WHICH = (%(id)s))
							"""

		else:
			statement = """DELETE FROM EVENTS
						WHERE (EVENT_ID = (%(id)s))
							"""

		cursor.execute(statement, {'id':id})
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_event_id(self, event):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT EVENT_ID FROM EVENTS
						WHERE (COMMENT = (%(id)s))
							"""

		cursor.execute(statement, {'id':event})
		event_id = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return event_id

	def create_role(self, surname, email, number, event_quota, which):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		today = datetime.today()

		statement = """INSERT INTO ROLES (SURNAME, EMAIL, NUMBER, EVENT_QUOTA, ROLE_WHICH)
						VALUES (%s, %s, %s, %s, %s)
							"""
		cursor.execute(statement, [surname, email, number, event_quota,which])
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_role_(self):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT ROLE_WHICH, SURNAME, EMAIL, NUMBER, EVENT_QUOTA FROM ROLES
							"""
		cursor.execute(statement)
		events = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return events

	def delete_roles(self, id, check):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		if(check == 0):
			statement = """DELETE FROM ROLES
						WHERE (ROLE_WHICH = (%(id)s))
							"""
		else:
			statement = """DELETE FROM ROLES
						WHERE (ROLE_ID = (%(id)s))
							"""

		cursor.execute(statement, {'id':id})
		connection.commit()
		cursor.close()
		connection.close()
		return

	def get_role_id(self, role):
		connection = dbapi2.connect(url)
		cursor = connection.cursor()

		statement = """SELECT ROLE_ID FROM ROLES
						WHERE (SURNAME = (%(id)s))
							"""

		cursor.execute(statement, {'id':role})
		role_id = cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return role_id

	def delete_interview(self, id):
	    connection = dbapi2.connect(url)
	    cursor = connection.cursor()

	    statement = """DELETE FROM INTERVIEWS
	                    WHERE (INTERVIEW_ID = (%(id)s))
	                    """
	    cursor.execute(statement, {'id':id})
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return

	def delete_event(self, id):
	    connection = dbapi2.connect(url)
	    cursor = connection.cursor()

	    statement = """DELETE FROM EVENTS
	                    WHERE (EVENT_ID = (%(id)s))
	                    """
	    cursor.execute(statement, {'id':id})
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return

	def delete_contact(self, id):
	    connection = dbapi2.connect(url)
	    cursor = connection.cursor()

	    statement = """DELETE FROM CONTACTS
	                    WHERE (CONTACT_ID = (%(id)s))
	                    """
	    cursor.execute(statement, {'id':id})
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return

	def delete_role(self, id):
	    connection = dbapi2.connect(url)
	    cursor = connection.cursor()

	    statement = """DELETE FROM ROLES
	                    WHERE (ROLE_ID = (%(id)s))
	                    """
	    cursor.execute(statement, {'id':id})
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return

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
