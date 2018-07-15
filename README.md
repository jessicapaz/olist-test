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
* **Computer**
`Notebook Asus Core i3-4005U 4GB 1TB`

* **Operating System**
`Ubuntu 16.04`

* **Code Editor**
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
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/subscriber/99988526423
  ```

* **DELETE**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/subscriber/{phone_number}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X DELETE https://callrecords.herokuapp.com/v1/subscriber/99988526423
  ```

## Price 
Receives a Price.

### **Base URL**:
```
https://callrecords.herokuapp.com/v1/price/
```

* **POST (Create)** 
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/price/
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X POST -d "tarrif_type=standard&standing_charge=0.38&call_charge=0.08" https://callrecords.herokuapp.com/v1/price/
  ```

* **GET (List)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/price/
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/price/
  ```

* **GET (Retrieve)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/price/{id}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/price/1/
  ```

* **DELETE**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/price/{id}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X DELETE https://callrecords.herokuapp.com/v1/price/1/
  ```

## Call Record
Receives a call record pair (start and end).

### **Base URL**:
```
https://callrecords.herokuapp.com/v1/call_record/
```

* **POST (Create)** 
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/call_record/
  ```
  * **Exemple (Call Start Record):**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X POST -d "id=1&type=start&timestamp=2016-02-29T12:00:00Z&call_id=1&source=99981848345&destination=9993468277" https://callrecords.herokuapp.com/v1/call_record/
  ```
  * **Exemple (Call End Record):**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X POST -d "id=1&type=start&timestamp=2016-02-29T13:00:00Z&call_id=1" https://callrecords.herokuapp.com/v1/call_record/
  ```

* **GET (List)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/call_record/
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/call_record/
  ```

## Bill Record
Return a bill records list of one subscriber.

### **Base URL**:
```
https://callrecords.herokuapp.com/v1/bill_record/{phone_number}
```

* **GET (Considering the previous month)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/bill_record/{phone_number}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/bill_record/99988526423/

  ```
* **GET (Considering the given period)**
  * **URL**
  ```
  https://callrecords.herokuapp.com/v1/bill_record/{phone_number}/?month={month}&year={year}
  ```
  * **Exemple:**
  ```bash
  $ curl -H "Authorization: JWT <your_token>" -X GET https://callrecords.herokuapp.com/v1/bill_record/99988526423/?month=12&year=2017/
  ```






