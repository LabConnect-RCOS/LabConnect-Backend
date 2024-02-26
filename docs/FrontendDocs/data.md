Labconnect Data Documentation:

Authentication:
No user logged in:
Cookies:
User : {}

How to retrieve data during authentication or app start up:
Check if cookie is available. If so, transfer cookie ⇒ globalContext (React context API) and authenticate with cookie in the background. When authenticated, change everything as necessary.

Necessary Functions:
logOut()
Removes all cookies
Removes information for global context
logIn()
Grabs data from server
Puts in global context api
Places in cookie


User Logged In:
Complete Cookies:
User: {
id: u1,
role:admin,
email: johnj@rpi.edu,
name: Jon John,
department: “Computer science”,
researchCenter: “CBIS”,
}

How Cookies And Authentication Are Used:
User Navigation:
Logged in users see:
All tabs
Log out tab

Not Logged In User:
Doesn’t see profile
Doesn’t see create




