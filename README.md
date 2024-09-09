# Planzo

This is an event management platform where users can browse and purchase tickets for various events. The platform allows event organizers to list their events and provides users with a seamless experience for discovering, booking, and managing their tickets. Whether it's concerts, conferences, or workshops, this platform aims to simplify the ticketing process.

## 🚧 Work in Progress

This project is currently under development. Features, documentation, and code are subject to change as the project evolves.

Please create your virtual environment first so that we can all have the required packages for this project when you create the requirements.txt
Please do a `pip freeze requirements.txt` when you work on the project so that we can get all dependencies from there.

to get all the project packages: `pip install -r requirements.txt`


How to run the web app:

1. **Clone the project repository:**
 
   ```git clone https://github.com/MungaSoftwiz/planzo.git```
2.  Navigate to the project directory:
  ``` cd src``
3. Create a Virtual Environment:
 ``` python3 -m venv ...``
4.  Activate the Virtual Environment (macOS/Linux):
  ```source .../bin/activate```
5.  Install Required Packages:
 ``` pip install -r requirements.txt```
6.  Migrate the Database:
  ```python manage.py migrate```
7.  Create a Super User:
  ```python manage.py createsuperuser```
8.  Start the Development Server:
 ``` python3 manage.py runserver``` to start the app

