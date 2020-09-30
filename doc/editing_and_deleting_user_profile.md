## Editing and deleting user profile

### Table of Contents

* [Interface for editing user profile](#interface-for-editing-user-profile)
* [Interface for editing user password](#interface-for-editing-user-password)
* [Interface for deleting user profile](#interface-for-deleting-user-profile)

### Interface for editing login

Edit login (either username or email).

* **URI:** `/users/login_update/`
* **Method:** `POST`
* **Params**
  * `username=[string]`
  * `email=[string]`
* **Success Response**
  * **Code:** 200
  * **Content:** None
* **Error Response**
  * **Code:** 400
  * **Content:**
    * `{"username": "This field may not be blank."}`
    * `{"username": "Username is already in use."}`
    * `{"email": "This field may not be blank."}`
    * `{"email": "Enter a valid email address."}`
    * `{"email": "Email is already in use."}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/users/login_update/ -d "username=some.user&email=some.user@example.com"`

### Interface for editing user password

Edit user password.

* **URI:** `/users/password_update/`
* **Method:** `POST`
* **Params**
  * `old_password=[string]`
  * `password=[string]`
  * `retype_password=[string]`
* **Success Response**
  * **Code:** 200
  * **Content:** None
* **Error Response**
  * **Code:** 400
  * **Content:**
    * `{"old_password": "This field may not be blank."}`
    * `{"old_password": "Incorrect old password."}`
    * `{"password": "This field may not be blank."}`
    * `{"password": "Passwords mismatch."}`
    * `{"password": [
          "This password is too short. It must contain at least 8 characters.",
          "This password is too common.",
          "This password is entirely numeric."
        ]
      }`
    * `{"retype_password": "This field may not be blank."}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/users/password_update/ -d "old_password=somepass&password=newpass&retype_password=newpass"`

### Interface for deleting user profile

Delete user profile.

* **URI:** `/users/profile_delete/`
* **Method:** `POST`
* **Params**
  * `username=[string]`
  * `password=[string]`
* **Success Response**
  * **Code:** 200
  * **Content:** None
* **Error Response**
  * **Code:** 400
  * **Content:**
    * `{"username": "This field may not be blank."}`
    * `{"username": "Username mismatch."}`
    * `{"password": "This field may not be blank."}`
    * `{"password": "Incorrect password."}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/users/profile_delete/ -d "username=some.user&password=somepass"`
