from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#THIS IS NOT YOUR EXAM
class UserManager(models.Manager):
    def register(self,data):
        errors=[]
        if data['name']=="":
            errors.append("Name cannot be left blank.")
        if len(data['name'])<2:
            errors.append("Name cannot be less than two characters long.")
        if data['alias']=="":
            errors.append("Alias name cannot be left blank.")
        if len(data['alias'])<2:
            errors.append("Alias name cannot be less than two characters long.")
        if not data['name'].isalpha():
            errors.append("Name can only accept letters.")
        if len(data['email'])<1:
            errors.append("Email cannot be left blank.")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email.")
        if data['birthday'] == '':
            errors.append("You must enter your birthday.")
        elif datetime.datetime.strptime(data['birthday'], '%Y-%m-%d') >= datetime.datetime.now():
            errors.append("You haven't been born yet!")
        if len(data['password'])<8:
            errors.append("Your password must be at least 8 characters long.")
        if not data['password']==data['conf_password']:
            errors.append("Your passwords must match.")
        try:
            User.objects.get(email=data['email'])
# Looking in our database to see if we can 'get' this same email from our saved info
            errors.append("You already have an account! Please Login.")
        except:
# Means if our get came up with nothing, this person does not have an account and is eligible to register for the first timeself.
# so we pass to the next thing
            pass
        if len(errors)==0:
            user=User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], birthday=data['birthday'], password=bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt()))
#refferring to user HERE from line 30 in views
            print id
            return {'user':user, 'errors':None}
#user at line 40 in models is the value that can be unlocked by the key 'user'
        else:
            return {'user':None, 'errors':errors}

    def login(self,data):
        errors=[]
        try:
            user=User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode(),user.password.encode())!= user.password.encode():
                errors.append("Wrong password!")
        except:
            errors.append("You do not have an account, please register!")
        if len(errors)!=0:
            return {'user':None, 'errors':errors}
        else:
            return {'user':user, 'errors':None}

class QuoteManager(models.Manager):
    def process_quotes(self,data):
        errors=[]
        if data['quoted_by']=="":
            errors.append("The quote must have an author and cannot be left blank.")
        if len(data['quoted_by'])<3:
            errors.append("This field must have more than 3 characters.")
        if len(data['content'])<10:
            errors.append("This quot must have more than 10 characters")
        if len(errors)==0:
            my_quote=Quote.objects.create(content=data['content'], quoted_by=data['quoted_by'], creator=data['creator'])
            print my_quote
            return {'my_quote':my_quote, 'errors':None}
        else:
            return {'my_quote':None, 'errors':errors}


class User(models.Model):
    name=models.CharField(max_length=50)
    alias=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=255)
    birthday=models.DateField()
    objects=UserManager()

class Quote(models.Model):
    content=models.CharField(max_length=255)
    quoted_by=models.CharField(max_length=255, default=None)
    creator=models.ForeignKey(User, related_name='my_quote')
    objects=QuoteManager()

class Favorite(models.Model):
    user=models.ForeignKey(User, related_name='user_favorites')
    quote=models.ForeignKey(Quote, related_name='quote_favorite')
    objects=QuoteManager()
