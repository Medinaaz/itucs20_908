Developer Guide
===============

Database Design
---------------

There are in total 5 tables where main table can be considered as HUMANS table where user creates/access his/her credentials and can create a contact list, set up events, interviews and system roles.

   .. figure:: erdesign.png
      :scale: 50 %
      :alt: map to buried treasure

      Database erdesign.



Code
----
SQL queries have been used under tables.py . The operations are implemented in server.py


   .. figure:: elephantsql.png
      :scale: 50 %
      :alt: map to buried treasure

      As an example, here is the code for login page and signup page.
      
Like it is mentioned, tables.py has functions that makes necessary changes in database. We used dbapi2(library: pscycopg2) for these functions
   
   .. figure:: login.png
      :scale: 50 %
      :alt: map to buried treasure

      As an example, here is the code for deleting comments from database.
      
      
   .. figure:: signup.png
      :scale: 50 %
      :alt: map to buried treasure
      
      Users data's can be observed in elephantsql server more clearly.
          
        

.. toctree::

 
