# LabConnect Data Documentation

## Authentication

### User Authentication State

- **No User Logged In:**
  - **Cookies:** 
    ```
    User: {}
    ```
  - **Procedure for Retrieving Data:**
    - Upon authentication or application startup, check for the presence of cookies.
    - If cookies are available, transfer the cookie to the global context (using React context API) and initiate background authentication using the cookie data.
    - Once authenticated, adjust application settings accordingly.

### Necessary Functions

- **logOut()**
  - Removes all cookies.
  - Clears user information from the global context.

- **logIn()**
  - Retrieves user data from the server.
  - Stores user data in the global context API.
  - Stores user data in cookies for future authentication.

## User Authentication Details

### User Logged In Details

- **Complete Cookies:**
  ```
  User: {
    id: u1,
    role: admin,
    email: johnj@rpi.edu,
    name: Jon John,
    department: “Computer Science”,
    researchCenter: “CBIS”,
  }
  ```

### Usage of Cookies and Authentication

- **User Navigation:**
  - **Logged In Users:**
    - Access to all tabs.
    - Log out option available.
  
  - **Not Logged In Users:**
    - Restricted access:
      - No profile view.
      - No option to create.