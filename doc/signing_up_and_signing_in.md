## Signing up and signing in

### Table of Contents

* [Introduction](#introduction)
* [Interface for signing up](#interface-for-signing-up)
* [Interface for signing in](#interface-for-signing-in)
* [Interface for refreshing an access token](#interface-for-refreshing-an-access-token)

### Introduction

One must have an account to customize OS images and get access to other CusDeb features (not less interesting than that). To create a new account (to sign up), provide the username, password and email. The username and password are used for signing in the system and the email is used:
* for account activation;
* for password recovery;
* (optionally) instead of username when signing in.

When a user is signed up, they can get a token pair to start working with CusDeb. The pair consists of an access token and a refresh token. By default, access tokens are expired in 5 minutes and refresh tokens are expired in 48 hours.

The access and refresh tokens are the [JSON Web Tokens](https://jwt.io) (JWT). Both access and refresh token contain the following encoded JSON payload.

```
{'token_type': '<token type>', 'exp': <exp>, 'jti': '<jti>', 'user_id': <user id>}
```

* `token_type` is a token type as it's seen from the name of the field. It accepts one of the following values: `'access'` or `'refresh'`.
* `exp` is an expiration date. It accepts integer numbers known as Unix timestamps.
* `jti` is a JWT ID (see [Section 4.1.7](https://tools.ietf.org/html/rfc7519#page-10) of RFC 7519).
* `user_id` is a user id. It accepts integer numbers.

The secret key stored in `SECRET_KEY` (located in the `docker.py`) module is used to implement encoding and decoding the payload.

It might be asked why there are two tokens instead of the only one. Let's look at the following two cases (borrowed from [this article](https://habr.com/ru/company/Voximplant/blog/323160/)).

* **Case 1: Eve knows both Alice's tokens and has never used the refresh token**

  In this case Eve will get access to the service until the access token is expired. When it expires and the application used by Alice uses the refresh token, the server will return a new pair of tokens and the previous one Eve has got will turn into a pumpkin.

* **Case 2: Eve knows both Alice's tokens and has used both of them**

  In this case both Alice's tokens turn into a pumpkin and the application used by Alice suggests that she authenticate providing her username and password. After that the token pair Eve has got will turn into a pumpkin again.

Thus, the combination of the access and refresh tokens limits the time of access to the system by a malicious user. In case of the only token, it can be used by the malicious user for weeks and nobody will ever know about it.

### Interface for signing up

Creates a new user account.

* **URI:** `/auth/signup/`
* **Method:** `POST`
* **Params**
  * `username=[string]`
  * `email=[string]`
  * `password=[string]`
* **Success Response**
  * **Code:** 201
  * **Content:** None
* **Error Response**
  * **Code:** 400
  * **Content:**
    * `{"11": "Username cannot be empty"}`
    * `{"12": "Password cannot be empty"}`
    * `{"13": "Email cannot be empty"}`
    * `{"21": "Username is already in use"}`
    * `{"22": "Email is already in use"}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/auth/signup/ -d "username=some.user&password=secret&email=some.user@example.com"`

### Interface for signing in

Obtains a pair of tokens.

* **URI:** `/auth/token/`
* **Method:** `POST`
* **Params:**
  * `username=[string]`
  * `password=[string]`
* **Success Response:**
  * **Code:** 200
  * **Content:** `{"refresh": "<refresh token>", "access": "<access token>"}`, where `<refresh token>` and `<access token>` are the JWT tokens.
* **Error Response:**
  * **Code:** 400
  * **Content:** `{"non_field_errors": ["No active account found with the given credentials"]}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/auth/token/ -d "username=some-user&password=secret"`

### Interface for refreshing an access token

* **URI:** `/auth/token/refresh/`
* **Method:** `POST`
* **Param:** `refresh=[string]` where `refresh` is the refresh token.
* **Success Response:**
  * **Code:** 200
  * **Content:** `{"access": "<access>"}`, where `<access>` is a new access token which replaces the previous one.
* **Error Response:**
  * **Code:** 401
  * **Content:** `{"detail": "Token is invalid or expired", "code": "token_not_valid"}`
* **Sample Call:**

  `$ curl -L -X POST http://127.0.0.1:8001/api/v1/auth/token/refresh/ -d "refresh=<refresh tocken>"`
