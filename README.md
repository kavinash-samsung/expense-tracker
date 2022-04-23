## Hi there

# Expense Tracker

For Sample Images Scroll at last

#### This project is implementation of the following topics related to technologies used in Django

- Used built in Django Auth Model
- Login, SignUp, Reset Password, Change Password, Logout implemented.
- Username/Email availability is checked after every key press asynchronously
- Password validation is checked at client side.
- Account verification send via Sending EMail 
- User is restricted to login till account is activated (Activation link send on mail)
- Used inbuilt views for building templates
- Pagination is Implemented to show limited record per page
- Implemented Django Messages for showing success/Error (all type of messages)

#### Implemented Crud Operation for Expenses and Income
- Built list view to show all the records
- Can Edit/Delete the particular record 
- Implemented search functionality using Ajax

#### Additional Functionality
- Can Export data in Excel and CSV format
- PDF report can be generated for all the Expenses/ Income 
- Dashboard to view Income and Expense Summary 
- Used Charts Js For Visualization 
- Implemented charts to show summary of Income/Expenses
- Currency Prefrences can also be changed(INR Default)
- User can update their Prefrences as per their prefrence

#### Hosting
- Deployed on PythonAnywhere
- Static files handled within python anywhere

##

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

[![Charts js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Sqllite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)](https://code.visualstudio.com/)

## Demo

Available at: [Expense Tracker](https://avi15.pythonanywhere.com)

Demo Login 

#### User With Staff Status
- Username : demoUser
- Password : Demo@123

Staff Login [(Staff URL)](https://avi15.pythonanywhere.com/admin)

#### Normal User
- Username : demoUser2
- Password : Demo@123


## Run code locally 

- Python3 required [(Download From here)](https://www.python.org/downloads/)

1. Create .env file in main directory 
    1. EMAIL_HOST_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    2. EMAIL_HOST = "smtp.gmail.com"
    3. EMAIL_HOST_USER = <Your email>
    4. EMAIL_HOST_PASSWORD = <Your email password>
2. Make sure Your have enabled less secure app in gmail 
3. If not refer this article [Click](https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail)
4. Follow below Steps

go to project directory
- inside project directory on cmd
  Execute this command : pip install -r requirements.txt
  
- make migrations and migrate them

1. python manage.py makemigrations
2. python manage.py migrate
  
- For creating system admin 
  
1. python manage.py createsuperuser
2. Enter the details asked
After creation of superuser

Now you are ready to run the project 

  python manage.py runserver
 
Visit [localhost:8000](http://localhost:8000/) in your browser
  
Either SIGNUP 
  
OR

LOGIN via superuser you created

- If Your Liked this project 
- Give it a Star
    
### Thanks
  

  
  ## Register 
  ![image](https://user-images.githubusercontent.com/43076709/164882058-4bc23b05-6f7b-442f-89c4-7ee294a466d4.png)

  ## Login
  ![image](https://user-images.githubusercontent.com/43076709/164882150-52e99a83-49cd-434a-970c-f040f7a940bc.png)

  ## Password reset 
  ![image](https://user-images.githubusercontent.com/43076709/164882250-5249c63b-6af6-4e86-b67f-35ac750d3a06.png)
  
  ## Password reset Email 
  ![image](https://user-images.githubusercontent.com/43076709/164882355-8ff00452-04e2-499d-9464-3615749ebca0.png)

  ## Dashboard
  ![image](https://user-images.githubusercontent.com/43076709/164880800-ed0fd618-884d-442f-8c1e-a64929c4db5f.png)

  ## Expense List
  ![image](https://user-images.githubusercontent.com/43076709/164880968-8ab7681d-6621-4d86-b215-3e0a59b77a00.png)
  
  ## Expense Summary
  ![image](https://user-images.githubusercontent.com/43076709/164881574-874344ae-9e11-4fc6-9be7-4ea29536ce8c.png)
  
  ## PDF summary
 ![image](https://user-images.githubusercontent.com/43076709/164881801-e2dfab60-cc72-4c91-8625-a9b84b54c08e.png)

 ## Accounts Page
  ![image](https://user-images.githubusercontent.com/43076709/164882461-88ef18d0-0781-480a-a348-3e0b07292734.png)

 ## Currency Prefrence
  ![image](https://user-images.githubusercontent.com/43076709/164882479-2695600c-2543-4ab9-acfc-9b05a2c76617.png)
  
  
  
 



