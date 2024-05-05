# Vendor Management System #

## Project Setup ##

1) Clone the repository.

2) Open terminal and cd into the root project directory (where manage.py and requirements.txt file exists).

3) Create a new virtual environment with command: `python -m venv venv`

4) Activate the virtual environment using command(for Windows): `.\venv\Scripts\activate`

5) Install required python packages (including django) using requirements.txt file with command: `pip install -r requirements.txt`

6) Set up a database: Create a MySQL database/schema with the name "vendor_management_system" 
Or you can optionally import the sample data provided in the folder "Vendor_Management_System_sample_data".
Update the database credentials (user and password) in settings.py file.

7) Run following commands for applying database migrations:
`python manage.py makemigrations`
`python manage.py migrate`

8) Start the server with the command: `python manage.py runserver`


## Testing using Postman ##

1) Import the postman collection named "Test Vendor Management System.postman_collection" 
provided in the root project folder into the Postman for API testing.
2) This will populate all important API requests into the Postman.
3) This API requests list is provided in a sequence of project's workflow.
It is advised to send the requests in the same order as given for a better understanding of project.


## API Documentation ##

### Users ###
#### 1) Register new user - POST http://127.0.0.1:8/register/

This takes following fields as a raw JSON body:
```
{
    "username": "john",
    "email": "john@gmail.com",
    "password": "password"
}
```
This will create a new user which will be used to generate the access token 
needed to access the APIs listed below.


#### 2) Get access token - POST http://127.0.0.1:8000/gettoken/

This takes following fields as a raw JSON body:
```
{
    "username": "vivek",
    "password": "password"
}
```
This will authenticate the user details provided and will return the access token 
and refresh token for that user. The access token will be valid for 30 minutes as configured in settings.py file.

From now onwards, we will require this access token to send upcoming API requests.
So copy the generated access token.


#### 3) Get all users - GET http://127.0.0.1:8000/users/

For this, we will need to provide the access token as a 'Bearer Token' in the 'Authorization' tab of Postman.

This will return all the existing users in the response.


### Vendors ###
#### 4) Create new Vendor - POST http://127.0.0.1:8000/vendors/

This POST request takes the access token and a raw JSON body to create a new vendor.
It will require Vendor's name, contact details and address in the body as follows:
```
{
    "name": "ABC enterprises",
    "contact_details": "1234567890",
    "address": "Pune"
}
```
This will return the details of a created user along with its metrics like 
on_time_delivery_rate, quality_rating_avg, average_response_time and fulfillment_rate set to null.


#### 5) Get all vendors - GET http://127.0.0.1:8000/vendors/

This GET request just takes the access token and returns the list of all existing vendors.


#### 6) Get vendor by id - GET http://127.0.0.1:8000/vendors/2

This GET request takes the access token and an id of a vendor as a path variable and returns 
the vendor matching the given id.


### Purchase Orders ###
#### 7) Create purchase order - POST http://127.0.0.1:8000/purchase_orders/

This POST request takes the access token and a raw JSON body having purchase order details.
It expects vendor(id of vendor) and items(list of items) in the body like below:
```
{
    "vendor": 1,
    "items": [
                {
                    "name": "Motorola Edge 50",
                    "price": 30000
                },
                {
                    "name": "Airpods pro",
                    "price": 2
                }
            ]
}
```

This will return the details of the created purchase order which includes below additional fields:

1. po_number: unique 10 digit order number.

2. order_date: current date at which order has been placed.

3. delivery_date: this is expected delivery date which is, for now, has been configured to set at 7 days from the current order date.

4. quantity: it is calculated based on how many items has been provided inside items list in the request.

5. status: it is by default set to Pending.

6. quality_rating: it is set to null initially. We can provide its value when we update the order to complete it(covered later in this documentation).

7. issue_date: the timestamp when this purchase order has been placed.

8. acknowledgment_date: Initially set to null. It is updated when we acknowledge the order(covered later in this documentation).


#### 8) Get purchase order by id - GET http://127.0.0.1:8000/purchase_orders/10

This GET request takes the access token and an id of a purchase order as a path variable and returns 
the purchase order matching the given id.


#### 9) Acknowledge purchase order - POST http://127.0.0.1:8000/purchase_orders/2/acknowledge/

This GET request takes the access token and an id of a purchase order which is to be acknowledged as a path variable.

This request acknowledges the purchase order and updates the acknowledgment_date field of the purchase order to the 
current timestamp and sends the successful message in the response.

This also triggers the calculation of average_response_time performance metrics.


#### 10) Complete purchase order - PUT http://127.0.0.1:8000/purchase_orders/10/

This request takes the access token, a raw JSON body and a purchase order id which we want to mark as completed as a path variable.

This expects 'status' and 'quality_rating'(optional) in the body as follows:
```
{
    "status": "Completed",
    "quality_rating": 90
    
}
```
This will update the status of the purchase order matching the passed id as a path variable to 'Complete' and 
will also update the quality rating if passed.

This also triggers the calculation of on_time_delivery_rate, quality_rating_avg and fulfilment_rate performance metrics.


### Historical Performance ###
#### 11) Get vendor performance - GET http://127.0.0.1:8000/vendors/2/performance

This GET request takes the access token and a vendor id as a path variable.

This returns all the performance metrics of a vendor matching the given id which include following fields:

1. date - recording date of performance metric.
2. on_time_delivery_rate - number of all on-time(on or before expected delivery date) completed orders 
divided by total number of completed orders for that vendor.
3. quality_rating_avg - average of all quality ratings for all completed orders of that vendor.
4. average_response_time - average of all the time differences (in hours) between issue_date and acknowledgment_date 
for each purchase order of that vendor.
5. fulfillment_rate - number of successfully completed order divided by total number of purchase orders issued to that vendor.

**NOTE**: The Historical Performance metrics table adds a new record each day for a vendor if any of the metrics has changed.
If the metrics of a certain vendor changes multiple times a day, it will update the existing metric record for that day 
and will only add a new record once a day. This is to avoid adding multiple records for a single vendor multiple times a day 
causing unnecessary storage for new records for a slight change in data while also maintaining the daily track record of a 
vendor's performance metrics.

Also, the metrics fields in the Vendor table just stores the latest calculated metrics. So they will be updated multiple times a day.


### Deleting ###
#### 12) Delete a purchase order - DELETE http://127.0.0.1:8000/purchase_orders/10/

This takes the access token and a purchase order id as a path variable and deletes the 
purchase order matching the id.


#### 13) Delete a vendor - DELETE http://127.0.0.1:8000/vendors/2/

This takes the access token and a vendor id as a path variable and deletes the 
vendor matching the id. 

This will also delete all the purchase orders and performance metrics of that vendor.

