lanciesite
==========

Setup
=====
Email
-----
To enable the contact form on the public website a few steps need to be taken.
The contact form sends an email to the administrator (or any address you want).
Because of this you have to set up django to the appropriate mail provider.
This can either be done in the global django settings or by a small file in the
lanciesite sub-folder. In case the email settings are in the global django
settings then line 13 needs to be removed from `lanciesite/settings.py`, this
line imports the local configuration. If you want to use this local
configuration instead then you should rename
`lanciesite/email_settings.py-example` to `lanciesite/email_settings.py` and
fill  in the details. Most of these are explained at
http://docs.djangoproject.com/en/1.6/ref/settings/ with the exception of the
`EMAIL_CONTACT_DESTINATION` setting, you should set this to the email address
where you want to receive the contact messages.
