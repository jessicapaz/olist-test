# Call Records API
## Description

A REST API that receives call records and calculates monthly bills for a given telephone number.  

## Installation

`$ git clone https://github.com/jessicapaz/olist-test.git`

`$ cd olist-test`

`$ pipenv install`

`$ pipenv shell`

`$ python manage.py migrate`

## Run tests

`$ python manage.py test`

## Work environment 

`Notebook Asus Core i3-4005U 4GB 1TB`

`Ubuntu 16.04`

`Visual Studio Code`

# API Documentation

## Authentication
Receives a POST with a user's email and password and returns a JSON Web Token that can be used for authenticated requests.

### **Base URL:**
```
https://callrecords.herokuapp.com/v1/auth/
```

* **POST (Create)**
  * **Exemple:**
  ```bash
  $ curl -X POST -d "email=test&password=test" https://callrecords.herokuapp.com/v1/auth/
  ```

## Subscriber
Receives a subscriber.

### **Base URL**:
```
https://callrecords.herokuapp.com/v1/subscriber/
```

* **POST (Create)** 
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/subscriber/
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X POST -d "first_name=Test&last_name=Test&phone_number=99985257541" https://callrecords.herokuapp.com/v1/subscriber/
  ```

* **GET (List)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/subscriber/
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/subscriber/
  ```

* **GET (Retrieve)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/subscriber/{phone_number}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/subscriber/99985257541
  ```

* **DELETE**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/subscriber/{phone_number}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X DELETE https://callrecords.herokuapp.com/v1/subscriber/99985257541
  ```







