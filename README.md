# Introduction
DjChat is a multi-page chat web app that is built entirely with Python and Django and fully containerized for quick deployment. People can make an account on the app, find other people and chat endlessly for hours. Have a funny meme to share? - then why wait open DjChat, find the person and click send. 

# Local Deployment
Steps to launch DjChat on a local machine 

1. Clone the repository
   ```
   git clone https://github.com/sagarmamodia/django-chat-application.git
   ```
2. Install Python 
   - Ensure that you have latest version of python installed on your machine.
3. Create and activate virtual environment 
   - Use the following command to create a virtual environment
   ```
   python -m venv venv
   ```
   - To active the virtual environment run the command for Linux
   ```source venv/bin/activate```
   for Windows(Powershell)
   ```.\venv\Scripts\Activate.ps1```
5. Install dependencies
   - Next step is to install the dependencies which is very easy in python all you've gotta do is run the following command with your virtual environment activated
   ```
   pip install -r requirements.txt
   ```
7. Database setup
   - Make sure you have MongoDB installed and running at 27017 port on your system because DjChat uses mongodb to store files shared in chats.
8. Run the app (Development)
   ```
   python manage.py runserver
   ```
   
# Architecture
   ![image](https://github.com/user-attachments/assets/783c969c-da52-43a4-997a-57295e2be339)
   - DjChat uses following technologies
     - Django
     - Django Channels (for Asynchronous support and websocket handling)
     - MongoDB and GridFS (for storing files)
     
# Further improvement ideas
   - Add Redis for channels instead of using main memory for channels.
   - Add caching (with Redis preferably) for quicker response to users.
   - Add email verification using OTP to make authorization more robust.
