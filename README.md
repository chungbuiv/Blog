# GotItBlog Installation

Step 1:
- Install requirements: pip install -r requirements.txt

Step2: Install and configure MySQL 
- Install MySQL 5.7
- Create database and user/password, then config these information in config.py file. 
In my project, I created database=blog, user=gotit and password=secret, so the configuration is as follow:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gotit:secret@localhost/blog'

Step 3: Create applications in Facebook and Google
- Create applications in Facebook and Google
- Configure Valid OAuth Redirect URIs on Facebook as http://127.0.0.1:5000/callback/facebook and http://localhost:5000/callback/facebook
- Configure Valid OAuth Redirect URIs on Google as http://127.0.0.1:5000/callback/google and http://localhost:5000/callback/google
- Get APP ID and SECRET from Facebook/Google application configurations
- Configure OAUTH_CREDENTIALS in config.py file based on APP ID and SECRET from Facebook and Google