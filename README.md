# Example Django Rest API

## Development Environment
* Windows 10
* Python 3.6.1
* Virtualenv (15.1.0)

## How to run
First if on a POSIX based system `source bin/activate` and if on Windows `\path\to\env\Scripts\activate` to acivate virtualenv.

Then `pip install -Ur requirements.txt`.

(from parent directory of repository):
```
cd products_app
python manage.py runserver
```

Open a browser and paste the development server url specified in the command prompty where the runserver command was executed, and add products/ to get to the Products listing page or attributes/ to get to the Attributes listing page.

## How to run unit tests 
Run everything through installing requirements.txt from the How to run section if the steps have not yet been run.

(from parent directory of repository):
```
cd products_app
python manage.py test api.tests
```

## URLs with HTTP method and the functionality they correspond to

| URL | HTTP Method | Functionality |
| --- | --- | --- |
| products/ | GET | List Products |
| products/?some_query_param=some_query_value | GET | Search Products |
| products/ | POST | Create Product |
| products/<id>/ | GET | Read Product |
| products/<id>/ | POST | Update Product |
| products/<id>/delete/ | POST | Delete Product | 
| products/<pid>/add-attribute/ | POST | Add Attribute to Product |
| products/<pid>/remove-attribute/ | POST | Remove Attribute from Product |
| attributes/ | GET | List Attributes |
| attributes/?some_query_param=some_query_value | GET | Search Attributes |
| attributes/ | POST | Create Attribute |
| attributes/<id> | GET | Read Attribute |
| attributes/<id> | POST | Update Attribute |
| attributes/<id>/delete/ | POST | Delete Attribute |

Both search routes only support exact matching. For products, the valid query parameters are:
* name
* price
* manufacturer
* product_type
* release_date
* created_at
* modified_at
* attributes__type
* attributes__value

For attributes, the valid query parameters are:
* type
* value

All endpoints have paging on with a default limit of 10. That limit can be increased by using limit=<desired_value> in the query string.

The add and remove attribute routes expect the request body to have a key-value pair with the key being "attribute_id" and the value being a valid attribute id.

For both the product and attribute models the update route expects all non-readonly fields to be supplied.

## Learnings
This was a great experience to learn Django Rest Framework. In retrospect, I may have tried to use Viewsets instead of Views to see if the amount of necessary code could have been reduced. Also, I would not have made all fields required on updates if I had more time to play around with that, and would've allowed partial updates via POST, even though that's not completely RESTFUL ideals, since through conversation the acceptable HTTP methods were limited to GET and POST. Having DELETE available would've allowed for some code reduction as the individual product/attribute view could've handled deletes, then. Also, with more time I definitely would've broken the view classes up into individual files inside of a views directory.
