from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import md5
import os, binascii
import datetime
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        if len(postData['name']) < 3:
            errors.append("Name should be more than 3 characters")
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Invalid letter")
        if len(postData['username']) < 3:
            errors.append("Username Name should be more than 3 characters")
        elif not NAME_REGEX.match(postData['username']):
            errors.append("Invalid letter")
        if len(postData['password']) < 8:
            errors.append("Password should be more than 8 characters")
        elif postData['password'] != postData['password_confirm']:
            errors.append("Password is not matched")

            
#if there's no error then password 
        if len(errors) == 0 :
            salt = binascii.b2a_hex(os.urandom(15)) 
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
             # add to database
            User.objects.create(name=postData['name'], username=postData['username'], salt=salt, password=hashed_pw)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(username=postData['username']):
            salt = User.objects.get(username=postData['username']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            # compare hashed passwords
            if User.objects.get(username=postData['username']).password != hashed_pw:
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('username has not been registered')
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "user object: ---,{} ----{}".format(self.name, self.username)

class TravelManager(models.Manager):
    def t_validator(self, postData):
        errors = []
        # today = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        # date_from = datetime.datetime.strptime(postData['date_from'], '%Y-%m-%d')
        # date_to = datetime.datetime.strptime(postData['date_to'], '%Y-%m-%d')

        if len(postData['destination']) < 0:
            errors.append("destination should not be empty!")
        if len(postData['description']) < 0:
            errors.append("description should not be empty!")

        return errors

        # try:
        #     current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        #     date_from = datetime.datetime.strptime(postData['date_from'], '%Y-%m-%d')
        #     date_to = datetime.datetime.strptime(postData['date_to'], '%Y-%m-%d')
        #     print date_to
        #     if current_date > date_from:
        #         errors['date_from'] = "Please correct your date"
        # except:
        #     errors['date_from'] = "Please input a date"
        # else:
        #     Travel.objects.create(destination= postData['destination'], description=postData['description'], date_from=postData['date_from'],date_to=postData['date_to'])

        


class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    join = models.ManyToManyField(User, related_name="join_travel")
    user = models.ForeignKey(User, related_name="upload_q")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelManager()
    def __repr__(self):
        return "object: {}, {}, {},{}".format(self.destination,self.description, self.date_from, self.date_to)
