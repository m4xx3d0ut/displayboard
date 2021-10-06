# DisplayBoard

## Local content updater for digital signage

~~Some tools for updating Fully Video Kiosk app (https://www.fully-kiosk.com/) on local LAN.~~
Initially this project was intended to update Android eSigns running the fully-kiosk app over their REST API, for... reasons... this ended up being a bad approach.  I've found it to be a much simpler approach to instead have the Flask app simply display the content to a player URL which the eSigns can then play from using their built in browser.  As a result this project is now suitable for any kiosk software capable of opening a URL (which broadens it's usability substantially).  As such I have changed the name of the project to simply "DisplayBoard", which I think says it all.  Functionally, it is a rudimentary CMS for digital signage.  More details to come as the project continues.

### Current State
- [x] Basic app framework
- [x] Content upload system
- [x] User login system
- [x] User management with Admin panel
- [X] Content settings configuration utility
- [X] Content player
- [X] 2FA via Google Authenticator
- [ ] Testing and code cleanup

### Where this project is at

This is now fully working!  I need to do some additional testing and cleanup, but I will be able to begin using this to program our digital display boards next week.  To get the 2FA to work, you will need to first browse through the db to the secret for admin, use that to setup the Google Authenticator app for time based OTP.  From that point you will be able to log in as admin (I would recommend setting up your own admin and user accounts, remove the test entry from the db for security purposes).  More updates to come as I perform further testing and revise functionality.

There is a env_vars.sh script included that will run the flask development server.  If you want to run it with Gunicorn you'll need to set these environmental variables:

export SESSION_TYPE=redis<br />
export SESSION_REDIS=redis://127.0.0.1:6379<br />

There are default credentials in the SQLite DB, you can log in with:

Email: admin@admin.com<br />
Password: admin<br />
OTP: (You will need to get the 'secret' from the DB and use the "Enter a setup key" option in Google Authenticator.  You can browse the DB to find this.)<br />

The admin page is pretty spartan at this point.  You can add a user, it will show you their info, including the secret for the OTP setup, but there is no way to remove a user from the panel at this time.  I recommend you use a DB browser, after creating a new admin account, to remove the default credentials.

I'm serving this with Nginx and Gunicorn.  The dispalyboard.service unit file will help you get that working with Systemd if you're into that sort of thing.