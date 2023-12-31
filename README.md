# BanPay Challenge

## Description

This code was developed in order to solve a Challenge given by BanPay.

The solution was built using Django as framework.

the routes created was:

| Route      | Method       |
|------------|--------------|
| /register  | POST         |
| /login  | POST         |
| /users  | GET          |
| /users/{id}  | GET / DELETE |
| /users/{id}/change_group | POST         |
| /users/{id}/change_password  | POST         |
| /ghibli  | GET          |


Every public user can register themselves, login, list and retrieve users.

Only Admins can delete users.

Only Admins and Oneself can change group. (only one group by user is functional)

Groups are a predefined list (FILMS, PEOPLE, LOCATIONS, SPECIES, VEHICLES).

Only Oneself can change password.

And Ghibli endpoint requires be authenticated.


## Run Local

In order to run project local with docker, it is required to have docker installed and create a ***'.env'*** file like:

```
SECRET_KEY=AlEhusyffxbtgfXeVmbTbiahiGwMxfnZWDjnhWsgWqUUBspMzd
DEBUG=True
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=banpay_db
```

and execute:

```
docker compose up -d
```