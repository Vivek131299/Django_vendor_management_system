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
1) Register new user - POST http://127.0.0.1:8/register/

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

2) Get access token - POST http://127.0.0.1:8000/gettoken/

This takes following fields as a raw JSON body:
```
{
    "username": "vivek",
    "password": "password"
}
```
This will authenticate the user details provided and will return the access token 
and refresh token for that user.

From now onwards, we will require this access token to send upcoming API requests.
So copy the generated access token.

3) Get all users - GET http://127.0.0.1:8000/users/

For this, we will need to provide the access token as a 'Bearer Token' in the 'Authorization' tab of Postman.

This will return all the existing users in the response.

4) 