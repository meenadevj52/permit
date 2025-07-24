Residential Parking Permit – Quick Setup
A simple Django REST API to manage parking permits. 
Citizens can apply. Admins can approve or reject.


1. Clone the Project
Run these commands: `git clone https://github.com/meenadevj52/permit.git`
after cloning run `cd residential_parking_permit`


2. Start with Docker
To run the app using Docker: `docker-compose up --build`


3. Admin User
After Docker runs, a user is created:
- Username: admin_user
- Password: Admin@123
- Role: admin
To manually run seed: `python manage.py seed` 


4. Run Tests
Run this to test the app: `docker exec -it permit-web-1 sh`
after this run `pytest`