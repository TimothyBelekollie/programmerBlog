# programmerBlog

## Steps to follow to run the project
### 1. Open your terminal and clone the project by writing the following command: git clone https://github.com/TimothyBelekollie/programmerBlog.git
### 2. Install a virtual Environment(Optional but recommended)  for the project by using this command: python -m venv myvenv
### 3.  Activate the environment by using this command: myvenv\Scripts\activate
### 4. Navigate to your project's directory and use pip to install the project's dependencies from the requirements.txt file: pip install -r requirements.txt
### 5. I did use postgrel sql database so if you want to use it go to the server and create a new database and name it progblog_db 
### 5. Run migrations to send the entities to postgrel by using these commands: 1. python manage.py makemigrations 2. python manage.py migrate
### 6. Create a Superuser (Admin User): You can create a superuser to access the Django admin panel by using this command: python manage.py createsuperuser
### 7. Start your local server by using this running this command: python manage.py runserver

