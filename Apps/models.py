from django.db import models

# Create your models here.
from django.db import models

# User
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    Category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False)
    def __str__(self):
        return self.name
    

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #used to store pass , email , name 
    profile =  models.ImageField(upload_to="images/UserProfiles")
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,null=False)
    content = models.TextField()
    date_timeStamp = models.DateTimeField(auto_now_add=True,null=False)
    thumbnail = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(User, related_name="favourite",blank=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    email = models.EmailField(null=False)
    message = models.TextField(null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.email} | {self.time}'


class CommentModel(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    get_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date_time = models.DateTimeField(auto_now_add=True)
    comment_message = models.TextField()
    reply_on_comment = models.ForeignKey("self", on_delete=models.CASCADE,null=True)


    