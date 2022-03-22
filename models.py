from django.db import models
import re
from . import views

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    # FIRST NAME
        #  at least 2 characters
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        # Letters only
        if postData['first_name'].isalpha() == False :
            errors['first_name'] = "First name must be letters only"
        # Required
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name required"

    # LAST NAME
        # at least 2 characters
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        # letters only
        if postData['last_name'].isalpha() == False :
            errors['last_name'] = "Last name must be letters only"
        # Required
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name required"

    # EMAIL
        # valid format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        # Required
        if len(postData['email']) == 0:
            errors['email'] = "Account must have an email"

    #Registered email is unique
        try: 
            self.get(email= postData['email'])
            errors['email_unique'] = "An account is already associated with that email"
        except:
            pass

    # PASSWORD:
        # at least 8 Chars
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        # Required
        if postData['password'] == "":
            errors['password'] = "Account must have a password"
        # Matches Confirmation
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Password and password confirmation must match"

        return errors

    def update_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    # FIRST NAME
        #  at least 2 characters
        if len(postData['first_name']) == 1:
            errors['first_name'] = "First name must be at least 2 characters"
        # Letters only
        if len(postData['first_name']) > 0 and postData['first_name'].isalpha() == False :
            errors['first_name'] = "First name must be letters only"
        # Required
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name required"

    # LAST NAME
        # at least 2 characters
        if len(postData['last_name']) == 1:
            errors['last_name'] = "Last name must be at least 2 characters"
        # letters only
        if len(postData['last_name']) > 0 and postData['last_name'].isalpha() == False :
            errors['last_name'] = "Last name must be letters only"
        # Required
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name required"

    # EMAIL
        # valid format
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        # Required
        if len(postData['email']) == 0:
            errors['email'] = "Account must have an email"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)