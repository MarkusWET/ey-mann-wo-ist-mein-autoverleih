# WebService 1 - Autoverleih

* Python
* Flask
* Flask-RESTful

For all requirements see [requirements.txt](./requirements.txt)

## CURL Requests
### Get token for user - `GET /api/token`
***Requires authetication***

Tokens are required for most of the REST endpoints. 
To request a token, submit username and password (e.g. `test_user:test_pass`).
The response will consist of a JSON Web Token (JWT) and the configured duration during which the token is valid.

**Request**
```shell
curl -u test_user:test_pass -i -X GET http://127.0.0.1:5000/api/token
``` 

**Response**
```json 
{
  "duration": 600,
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc"
}
```

### List all available cars - `PUT /api/car/available`
***Requires authetication***

Returns a list of all available cars (meaning: cars that are not rented during the submitted timeframe).

**Request**
```bash
curl -u $JWT:x \
-i -X PUT -H "Content-Type: application/json" \
-d '{"start":"2018-03-12","end":"2018-03-15"}' \
http://127.0.0.1:5000/api/car/available
```

**Response**
```json
{
  "available": [
    {
      "color": "#0088CC", 
      "company": "Ford", 
      "gps_lat": 48.213024, 
      "gps_long": 16.384843, 
      "id": 1, 
      "model": "Mustang", 
      "price_per_day": 150.0
    }, 
    {
      "color": "#FF2800", 
      "company": "Ferrari", 
      "gps_lat": 48.213024, 
      "gps_long": 16.384843, 
      "id": 3, 
      "model": "Enzo", 
      "price_per_day": 6000.0
    }
  ]
}
```

### List all cars - `PUT /api/car/all`
Returns a list of all available cars, regardless of availability.

**Request (with currency conversion to Russian Rubel)**
```shell
curl -u $JWT -i -X GET http://127.0.0.1:5000/api/car/all?currency=RUB
```

**Response**
```json
{
  "available": [
    {
      "color": "#0088CC", 
      "company": "Ford", 
      "gps_lat": 48.213024, 
      "gps_long": 16.384843, 
      "id": 1, 
      "model": "Mustang", 
      "price_per_day": 10633.455
    }, 
    {
      "color": "#50191F", 
      "company": "Lada", 
      "gps_lat": 48.213024, 
      "gps_long": 16.384843, 
      "id": 2, 
      "model": "Taiga", 
      "price_per_day": 708.897
    }, 
    {
      "color": "#FF2800", 
      "company": "Ferrari", 
      "gps_lat": 48.213024, 
      "gps_long": 16.384843, 
      "id": 3, 
      "model": "Enzo", 
      "price_per_day": 425338.2
    }
  ]
}
```

### List all rented cars of user - `GET /api/user/<user_id>/rented`
***Requires authetication***

**Request**
```shell
curl -u $JWT:x \
-i -X GET -H "Content-Type: application/json" \
http://127.0.0.1:5000/api/user/1/rented
```

**Response**
```json
{
  "rentals": [
    {
      "car_id": 1, 
      "id": 13, 
      "rented_from": "Mon, 12 Mar 2012 00:00:00 GMT", 
      "rented_to": "Sat, 15 Sep 2012 23:59:59 GMT", 
      "total_price": 28050.0, 
      "user_id": 1
    }
  ]
}
```

### Rent car - `GET /api/car/<car_id>/rent`
***Requires authetication***

**Request**

```shellcurl -u $JWT:x \
-i -X PUT -H "Content-Type: application/json" \
-d '{"start":"2018-03-12","end":"2018-09-15"}' \
http://127.0.0.1:5000/api/car/2/rent  
```

**Response**
```
Car 2 rented successfully.
```

### Return car - `GET /api/car/<car_id>/return`

***Requires authetication***

**Request**
```shell
curl -u $JWT:x \
-i -X PUT -H "Content-Type: application/json" \
http://127.0.0.1:5000/api/car/1/return
```

**Response**
```
Car with ID 1 returned successfully.
```


### Update car's GPS coordinates - `PUT /api/car/<car_id>/gps`

***Requires authetication***

**Request**
```shell
curl -u $JWT \
-i -X PUT -H "Content-Type: application/json" \ 
-d '{"longitude":"20","latitude":"-50"}' \
http://127.0.0.1:5000/api/car/1/gps

```

**Response**
```json
{
  "car": {
    "color": "#0088CC", 
    "company": "Ford", 
    "gps_lat": -50.0, 
    "gps_long": 20.0, 
    "id": 1, 
    "image_file_name": "mustang.JPG", 
    "model": "Mustang", 
    "price_per_day": 150.0
  }
}
```
