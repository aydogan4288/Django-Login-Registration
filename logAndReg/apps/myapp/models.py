from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must contain at least 2 characters!'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = 'Name must contain only letters!'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must contain at least 2 characters!'
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last Name must contain only letters!"

        if len(postData['email']) < 1:
            errors['email'] = 'You muts provide an email!'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid!'
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "Email is already taken."

        if len(postData['password']) <2 :
            errors['password'] = 'Password must contain at least 8 characters'
        if postData['confirm'] != postData['password']:
            errors['confirm'] = 'Password confirmation doesn not match the Password!'

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['passwordlogin']) < 1:
            errors['passwordlogin'] = "Password cannot be blank."

        if len(postData['emaillogin']) < 1:
            errors['emaillogin'] = "Email cannot be blank."
        elif not User.objects.filter(email=postData['emaillogin']):
            errors['emaillogin'] = "Email is not in database."

        else:
            user = User.objects.filter(email=postData['emaillogin'])
            print(user)
            if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
                errors['passwordlogin'] = "Passwords don't match"
            return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return self.first_name



# Create your models here.
