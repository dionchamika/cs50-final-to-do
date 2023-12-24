## CS50 To-DO Application
Video Demo: [https://youtu.be/7T9Jsk_HRpI]


## Description
Welcome to my web application project, powered by Python and Flask! This application serves as a versatile task management tool, offering user authentication, task creation, completion tracking, and data persistence through SQLite.


## Project Structure
app.py: This is the main file containing the Flask application configuration, routes, and database initialization. Key features such as user authentication, task management, and database interactions are implemented here.

templates: This folder contains all HTML templates used in the project. Each template corresponds to a specific route and is responsible for rendering the user interface.

static: This directory houses static files like CSS stylesheets and images that enhance the visual aspects of the application.

models.py: Defines the data models for the SQLAlchemy database, including the User and Task tables.

requirements.txt: Lists all the Python dependencies required for the project. Use pip install -r requirements.txt to install them.

Getting Started

## Prerequisites
## Make sure you have the following installed:

Python 3.x
Flask
SQLite
Installation
Clone the repository: git clone https://github.com/dionchamika/cs50-final.git
Navigate to the project directory: cd your-project
Install dependencies: pip install -r requirements.txt
Run the application: python app.py
The application will be accessible at http://localhost:5000 by default.

## Usage
Open your web browser and go to http://localhost:5000.
Sign up for a new account or log in if you already have one.
Explore the task management features: add new tasks, mark tasks as complete, and more.
Contributing
Contributions are highly encouraged! If you encounter any issues or have suggestions for improvements, please feel free to create a pull request. Your contributions will play a crucial role in enhancing the project.

## Design Choices
The project embraces simplicity for user interactions, ensuring a seamless experience. The choice of Flask and SQLite facilitates quick development and easy integration.
