# DisplayBoard

## Local content updater for digital signage

~~Some tools for updating Fully Video Kiosk app (https://www.fully-kiosk.com/) on local LAN.~~
Initially this project was intended to update Android eSigns running the fully-kiosk app over their REST API, for... reasons... this ended up being a bad approach.  I've found it to be a much simpler approach to instead have the Flask app simply display the content to a player URL which the eSigns can then play from using their built in browser.  As a result this project is now suitable for any kiosk software capable of opening a URL (which broadens it's usability substantially).  As such I have changed the name of the project to simply "DisplayBoard", which I think says it all.  Functionally, it is a rudimentary CMS for digital signage.  More details to come as the project continues.

### Current State
- [x] Basic app framework
- [x] Content upload system
- [x] User login system
- [x] User management with Admin panel
- [ ] Content settings configuration utility
- [ ] Content player