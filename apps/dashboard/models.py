from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
NAME_REGEX = re.compile(r'^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        # First name validation
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = 'First name must only be alphabet'
        # Last name validation
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['last_name'] = 'Last name must only be alphabet'
        # Email validation
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = 'Email has already been registered'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is an invalid format'
        # Password validation
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        elif postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords must match'

        if not errors:
            # Generate salt
            salt = bcrypt.gensalt()
            # Form data must be encoded before hashing
            password = postData['password'].encode()
            # Hash password with salt
            hashed_pw = bcrypt.hashpw(password, salt)

            # Create user object
            user = User()
            user.first_name = postData['first_name'].title()
            user.last_name = postData['last_name'].title()
            user.email = postData['email']
            user.password = hashed_pw
            user.description = ''
            user.save()

        return errors

    def validate_login(self, postData):
        errors = []
        user_exist = User.objects.filter(email=postData['email'])

        if len(user_exist) == 0:
            errors.append('Email has not been registered')
        else:
            form_pw = postData['password'].encode()
            db_pw = User.objects.get(email=user_exist[0].email).password.encode()
            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')

        return errors

    def validate_info(self, postData):
        errors = {}
        # First name validation
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = 'First name must only be alphabet'
        # Last name validation
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['last_name'] = 'Last name must only be alphabet'
        # Email validation
        found_user = User.objects.filter(email=postData['email'])

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is an invalid format'
        # If email has already been registered and is not same email as original
        elif len(found_user) == 1 and found_user[0].email != postData['prev_email']:
            errors['email'] = 'Email belongs to another user'

        if not errors:
            user = User.objects.get(email=postData['prev_email'])
            user.email = postData['email']
            user.first_name = postData['first_name']
            user.last_name = postData['last_name']
            user.admin_level = postData['admin_level']
            user.save()

        return errors

    def validate_password(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        elif postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords must match'

        if not errors:
            salt = bcrypt.gensalt()
            password = postData['password'].encode()
            hashed_pw = bcrypt.hashpw(password, salt)

            user = User.objects.get(email=postData['prev_email'])
            user.password = hashed_pw
            user.save()

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    admin_level = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # Connect an instance of UserManager to User model that overwrites the keyword       # 'object' with a new one with extra properties inheried from models.Manager
    objects = UserManager()

    def __str__(self):
        return '{} - {} - {} - {} - {} - {}'.format(self.first_name, self.last_name, self.email, self.password, self.admin_level, self.description)

class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="posts")
    wall = models.ForeignKey(User, related_name="wall")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    post = models.ForeignKey(Post, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
