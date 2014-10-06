lanciesite
==========

CSS
-----
The CSS for the new template is created with bootstrap and LESS.
This project can be found at: https://github.com/IcyPalm/LanCie-css-rebuild

Setup
=====

Email
-----
To enable the contact form on the public website a few steps need to be taken.
The contact form sends an email to the administrator (or any address you want).
Because of this you have to set up django to the appropriate mail provider.
This can either be done in the global django settings or by a small file in the
lanciesite sub-folder. In case the email settings are in the global django
settings then you don't need to do anything as it should work out of the box.
If you want to use the local configuration instead then you need to uncomment
line 13 in `lanciesite/settings.py` and rename
`lanciesite/email_settings.py-example` to `lanciesite/email_settings.py` and
fill  in the details. Most of these are explained at
http://docs.djangoproject.com/en/1.6/ref/settings/ with the exception of the
`EMAIL_CONTACT_DESTINATION` setting, you should set this to the email address
where you want to receive the contact messages.

Requirements
-----
To correctly format the forms in our bootstrap template an additional package is 
required:

django-bootstrap3 (https://github.com/dyve/django-bootstrap3)
