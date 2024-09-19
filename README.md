# Planzo

**Planzo** is a web application designed to streamline event planning and organization, allowing users to create, manage, and track events effortlessly.

## Features

- Create, edit, and delete events
- Manage event details (date, time, location)
- Track upcoming and past events
- User-friendly interface for organizing multiple events

## Technologies Used

- **Django 5.1.1**: The primary web framework.
- **asgiref 3.8.1**: Manages asynchronous operations in Django.
- **django-widget-tweaks 1.5.0**: Tools for modifying form attributes and layout.
- **pillow 10.4.0**: Python imaging library for handling media files.
- **python-decouple 3.8**: Manages environment variables and sensitive information.
- **sqlparse 0.5.1**: SQL parsing and formatting in Django's ORM.
- **typing_extensions 4.12.2**: Supports backporting newer type hints.
- **Semantic UI**: A CSS framework used to enhance the user interface, providing a clean and modern look.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MungaSoftwiz/planzo.git
   ```

2. Navigate to the project directory:
   ```bash
   cd planzo
   ```

3. Create and activate a virtual environment:

On macOS/Linux:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

On Windows:

   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables in a .env file:

env
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

- Access the application at http://127.0.0.1:8000/.

### Usage
Once the server is running, users can create an account, log in, and start creating, managing, and tracking events.
