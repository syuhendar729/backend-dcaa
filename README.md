# Entity Database

| field | type | additional |
| --- | --- | --- |
| id | Integer | primary_key |
| username | String | unique |
| email | String | unique |
| password | String |  |
| profile_picture | String |  |
| created_at | Datetime |  |
| updated_at | Datetime |  |

# API Docs

## 1. Register User API

Endpoint :  `POST /user`

Request Body `form-data` :

| key | type | value |
| --- | --- | --- |
| username | text | oda |
| email | text | oda@mail.com |
| password | text | oda123 |

Response Body Success :

```json
{
    "data": {
        "oda2": "oda2",
        "oda2@mail.com": "oda2@mail.com"
    },
    "message": "Success create user data."
}
```

Response Body Error :

```json
// username already exists
{
    "data": [],
    "message": "Failed create user. Username already exists."
}
// email already exists
{
    "data": [],
    "message": "Failed create user. Email already exists."
}
```

## 2. Login User API

Endpoint :  `POST /user`

Request Body `form-data` :

| key | type | value |
| --- | --- | --- |
| email | text | oda@mail.com |
| password | text | oda123 |

Response Body Success :

```json
{
    "data": {
        "access_token": "<access_token>",
        "data": {
            "email": "oda@mail.com",
            "id": 1,
            "profile_picture": null,
            "username": "oda"
        },
        "refresh_token": "<refresh_token>"
    },
    "message": "Success login!"
}
```

Response Body Error :

```json
// user not registered
{
    "data": [],
    "message": "Failed login. User not registered."
}
// if wrong password
{
    "data": [],
    "message": "Failed login. Wrong password."
}
```

## 3. Update User Data API

Endpoint :  `PATCH /user`

Authorization: `Bearer Token`

Request Body `form-data`:

| key | type | value |
| --- | --- | --- |
| username | text | oda |
| email | text | oda@mail.com |
| profile_picture | file | <file_image> |

Response Body Success :

```json
{
    "data": {
        "email": "oda@mail.com",
        "profile_picture": "/static/namafile.png",
        "username": "oda"
    },
    "message": "Success update user data."
}

// if only update email

{
    "data": {
        "email": "oda@mail.com",
        "profile_picture": null,
        "username": null
    },
    "message": "Success update user data."
}
```

Response Body Error :

```json
// if not valid email

{
    "data": {
        "email": [
            "Not a valid email address."        
         ]
    },
    "message": "Validation failed."
}
// username already exist
{
    "data": [],
    "message": "Failed update user. Username already exists."
}
// email already exist
{
    "data": [],
    "message": "Failed update user. Email already exists."
}
// not valid image extension
{
    "data": [],
    "message": "Invalid file type. Only PNG, JPG, or JPEG files are allowed."
}
```

## 4. Get Detail User Data API

Endpoint :  `GET /users`

Authorization: `Bearer Token`

Request Body `form-data`:

| key | type | value |
| --- | --- | --- |
| old_password | text | oda123 |
| new_password | text | 123oda |

Response Body Success :

```json
{
    "data": {
        "email": "oda@mail.com",
        "id": 16,
        "profile_picture": null,
        "username": "oda2"
    },
    "message": "Success get detail user."
}

```

## 5. Reset Password User Data API

Endpoint :  `PATCH /users`

Authorization: `Bearer Token`

Request Body `form-data`:

| key | type | value |
| --- | --- | --- |
| old_password | text | oda123 |
| new_password | text | 123oda |

Response Body Success :

```json
{
    "data": [],
    "message": "Success update password."
}
```

## 6. Logout User API

Endpoint :  `PATCH /logout`

Authorization: `Bearer Token`

Request Body `form-data`:

| key | type | value |
| --- | --- | --- |
| old_password | text | oda123 |
| new_password | text | 123oda |

Response Body Success :

```json
{
    "data": [],
    "message": "Success logout user."
}
```

Error Response Umum:

```json
// token in blacklist
{
    "msg": "Token has been revoked"
}
{
    "msg": "Invalid header padding"
}
```

## 6. Delete User API

Endpoint :  `DELETE /users`

Authorization: `Bearer Token`

Response Body Success :

```json
{
    "data": 1,
    "message": "Success delete user."
}
```

Error Response Umum:

```json
{
    "data": [],
    "message": "Failed delete user. User not found."
}
```
