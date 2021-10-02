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

This is now fully working!  I need to do some additional testing and cleanup, but I will be able to begin using this to program out digital display boards next week.  To get the 2FA to work, you will need to first browse through the db to the secret for admin, use that to setup the Google Authenticator app for time based OTP.  From that point you will be able to log in as admin (I wouldn't recommend setting up your own admin and user accounts, remove the test entry from the db for security purposes).  More updates to come as I perform further testing and revise functionality.