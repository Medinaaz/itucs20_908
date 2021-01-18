SELECT * FROM "public"."humans" LIMIT 100

SELECT * FROM "public"."contacts" LIMIT 100

SELECT * FROM "public"."events" LIMIT 100

SELECT * FROM "public"."roles" LIMIT 100

SELECT * FROM "public"."interviews" LIMIT 100


DELETE FROM HUMANS;

INSERT INTO HUMANS(name, password, role, date) VALUES('Med', 'med12','admin','2021-01-17')

SELECT * FROM "public"."events" LIMIT 100

SELECT * FROM "public"."interviews" LIMIT 100

INSERT INTO INTERVIEWS(date_from, date_to, comment) VALUES('2021-01-10','2021-01-10','Siemens Interview')

INSERT INTO INTERVIEWS(date_from, date_to, comment) VALUES('2021-01-24','2021-01-24','Vodafone Interview')

INSERT INTO INTERVIEWS(date_from, date_to, comment) VALUES('2021-01-23','2021-01-23','Tesla Interview')

INSERT INTO CONTACTS(contact_name, contact_surname, contact_email, contact_number) VALUES('Zaurela','Dibra','z@gmail.com', '123')

INSERT INTO CONTACTS(contact_name, contact_surname, contact_email, contact_number) VALUES('Olsi','Zaganjori','olsi@gmail.com', '12367')

INSERT INTO CONTACTS(contact_name, contact_surname, contact_email, contact_number) VALUES('Ina','Dibra','ina@gmail.com', '1234')

INSERT INTO CONTACTS(contact_name, contact_surname, contact_email, contact_number) VALUES('Suzana','Zaganjori','s@gmail.com', '12343')

INSERT INTO EVENTS(date_from, date_to, comment, status) VALUES('2021-02-27','2021-03-02','Trip', 'Approved')

INSERT INTO EVENTS(date_from, date_to, comment, status) VALUES('2021-03-26','2021-03-27','Mountain Trip', 'Approved')

INSERT INTO ROLES(surname, email, number, event_quota) VALUES('Zaganjori','medinamedinazaganjori@gmail.com','+905059768593', '56')