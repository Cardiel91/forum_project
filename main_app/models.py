from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 5:
            errors['first_name'] = "First name must be at least 5 characters long"

        if len(postData['last_name']) < 5:
            errors['last_name'] = "Last name must be at least 5 characters long"

        if len(postData['email']) < 5:
            errors['email'] = "Email must be at least 5 characters long"

        if len(postData['password']) < 5:
            errors['password'] = "Password must be at least 5 characters long"

        if postData['password'] != postData['password_conf']:
            errors['password_conf'] = "password and password conf need to match"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = "Email is not in correct fomat"

        result = User.objects.filter(email=postData['email'])
        if len(result)> 0:
            errors['email'] = "Email is already registered"
        return errors   
        

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User, related_name="user_message", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="post_likes")

class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Message, related_name="comment_post", on_delete=models.CASCADE)
