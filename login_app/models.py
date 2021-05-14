from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        if User.objects.filter(email = postData['email']):
            errors['email'] = f"{postData['email']} is already in use"
        if len(postData['pw']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['confirm']:
            errors['password'] = "Passwords do not match"
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['pw'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['fname'],
            last_name = form['lname'],
            email = form['email'],
            password = pw,
        )

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()