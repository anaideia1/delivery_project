# Delivery system project
Simplified api-service for managing users and their orders. 


# Local development
1. ```docker-compose build``` (Env file already exist in project)
2. ```docker-compose up```
3. (optional) ```docker-compose exec web python manage.py delayed_orders``` for updating statuses of outdated orders type
