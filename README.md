# Django REST API Setup

This repository contains a Django project with a RESTful API using Django REST Framework.

## Prerequisites

- Python (version 3.x recommended)
- Django
- Django REST Framework

# Setup Instructions

## Install Dependencies:
- pip install django
- pip install djangorestframework

## Set up a new project with a single application
- django-admin startproject Vendor_management_system                 
- cd Vendor
- django-admin startapp Vendor              

## Database migration                    
- python manage.py makemigrations      
- python manage.py migrate

## Superuser creation and Token generation
- python manage.py createsuperuser

## Running the server
- python manage.py runserver

## Access Django Admin:
Open the Django admin at http://127.0.0.1:8000/admin/ and log in using the superuser credentials. this is to access the database as a admin user.

## how to run a api endpoint:
- first we need to make sure that we migrated the models to database
- then we need to start the server using "python manage.py runserver" command.
- then we need to open another cmd prompt and open virtual environment and open the project folder and provide curl or httpie commands.

# Testing or Using the API endpoints.
- we can test API endpoints using curl or httpie commands. 

## Create a vendor:
### using httpie:
- http POST http://127.0.0.1:8000/api/vendors/ vendor_code=01 name="Vendor 1" contact_details="Contact 1" address="Address 1"
### About this API endpoint:
- here this endpoint is used to create a vendor by providing the vendor details.

## List all Vendors details:
### using httpie:
- http http://127.0.0.1:8000/api/vendors/ 
### About this API endpoint:
- here this endpoint is used to get the details of all vendors.

## Retrieve a specific vendor's details:
### using httpie:
- http http://127.0.0.1:8000/api/vendors/{vendor_id}/ 
### About this API endpoint:
- here this endpoint is used to get the details of vendor with vendor_id which was mentioned in the command. 

## Update a vendor's details:
### using httpie:
#### PUT method:
- http PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/ vendor_code="updated vendor code" name="Updated Vendor Name" contact_details="Updated Contact Details" address="Updated Address" 
#### PATCH method:
- http PATCH http://127.0.0.1:8000/api/vendors/{vendor_id}/ name="Updated Vendor Name" contact_details="Updated Contact Details" address="Updated Address"
### About this API endpoint:
- here this endpoint we have two commands with different http methods (PUT,PATCH).As we have a primary key in the model the PUT method works as POST method (which means it creates a new vendor with given details). The PATCH method is used to update the vendor's details except vendor's id. here PUT handles updates by replacing the entire entity, so it creates a new entity. but where the PATCH handles by only updating the given fields.

## Delete a vendor:
### using httpie:
- http DELETE http://127.0.0.1:8000/api/vendors/{vendor_id}/ 
### About this API endpoint:
- here this endpoint is used to delete the vendor with given vendor_id.

## Create a purchase_order:
### using httpie:
- http POST http://127.0.0.1:8000/api/purchase_orders/ po_number="01" vendor=01 order_date="2023-01-01" delivery_date="2023-01-10" items='[{"item_name": 20 }]' quality_rating=4.5 issue_date="2023-01-01" status="Pending" acknowledgment_date="2023-01-02"
### About this API endpoint:
- here this endpoint is used to create a purchase_order with given details.

## List all purchase_orders details:
### using httpie:
- http http://127.0.0.1:8000/api/purchase_orders/ 
### About this API endpoint:
- here this endpoint is used to get the details of all purchase_orders.

## Retrieve a specific purchase_order's details:
### using httpie:
- http http://127.0.0.1:8000/api/purchase_orders/{po_id}/
### About this API endpoint:
- here this endpoint is used to get the details of purchase_order with given po_id.

## Update a purchase_order's details:
### using httpie:
#### PUT method:
- http PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/ po_number="UpdatedPO001" vendor="updatedid" order_date="2023-01-02T12:00:00" delivery_date="2023-01-15T12:00:00" items:='[{"item_name": 20 }]' quality_rating:=4.8 issue_date="2023-01-01" status="updated" acknowledgment_date="2023-01-02" 
#### PATCH method:
- http PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/ order_date="2023-01-02T12:00:00" delivery_date="2023-01-15T12:00:00" items:='[{"item_name": "Updated Item", "quantity": 20 }]' quality_rating:=4.8 status="updated" 
### About this API endpoint:
- here this endpoint we have two commands with different http methods (PUT,PATCH).As we have a primary key in the model the PUT method works as POST method (which means it creates a new purchase_order with given details). The PATCH method is used to update the purchase_order's details except purchase_order's number. here PUT handles updates by replacing the entire entity, so it creates a new entity. but where the PATCH handles by only updating the given fields.(we can provide any no of fields in PATCH mathod.)

## Delete a purchase_order:
### using httpie:
- http DELETE http://127.0.0.1:8000/api/purchase_orders/{po_id}/ 
### About this API endpoint:
- here this endpoint is used to delete a purchase_order with given po_id.

## Retrieve a vendor's performance metrics:
### using httpie:
- http http://127.0.0.1:8000/api/vendors/1/performance/ 
### About this API endpoint:
- here this endpoint is used to retrieve the performance metrics of a vendor with given vendor_id. this performance metrics contains on_time Delivery rate, quality rating average, average response time, fulfilment rate
- On time delivery rate is calculated each time a PO status changes to "completed". this is the average of no of po delivered before the delivery_date and no of total po's delivered.
- quality rating average is calculated after every po completion and it is the average of all ratings given to that specific vendor.
- average response time is calculated each time a po is acknowledged by the vendor. it is the time difference between issue_date and acknowledgment_date for each po, and then the average of these times for all po's of the vendor.
- fulfillment rate is calculated when po status is set to "completed". this is the average of no of successfully fulfilled pos (status = "completed" without issues) by the total no of pos issued to the vendor.

## Update acknowledgment_data and trigger the recalculation of average_response_time:
### using httpie:
- http PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/acknowledgment_date="2023-12-20T12:00:00Z"
### About this API endpoint:
- here this endpoint is used to acknowledge the purchase_order with given po_id and trigger the recalculation of average_reponse_time.
