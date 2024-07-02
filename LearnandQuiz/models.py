from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# create user model
class CustomUser(AbstractUser):
    image = models.ImageField(default='/static/1234567890.png')
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','name']


# create user profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

# create Banner model
class Banner(models.Model):
    image = models.ImageField()


# create Ads Banner model
class Ads(models.Model):
    image = models.ImageField()


# create Linux distrubution model to add linux course
class LinuxDistribution(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=200, primary_key=True)
    description = models.TextField(max_length=500)
    update = models.DateField(auto_now=True)


# create Course model to add courses of the linux distribution
class Course(models.Model):
    category = models.ForeignKey(LinuxDistribution, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100, primary_key=True)
    coursename = models.CharField(max_length=100)
    image = models.ImageField()
    update =models.DateField(auto_now=True)
    def name(self):
        return self.category.name


# create content model to add the content of the course
class Content(models.Model):
    category = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contentname = models.CharField(max_length=100)
    pdf = models.FileField()
    image = models.ImageField()
    description = models.TextField(max_length=1000000)
    videolink = models.CharField(max_length=10000, blank=True)
    references = models.TextField(max_length=10000, blank=True)
    update =models.DateField(auto_now=True)
    def name(self):
        return self.category.course


    

# create Question model to add question of the linux distributions
class QuesModel(models.Model):
    category = models.ForeignKey(LinuxDistribution, on_delete=models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.question


# Discussion Forum model
# create forum model to add the discussion  
#parent model
class Forum(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    topic= models.CharField(max_length=300)
    description = models.TextField(max_length=1000000,blank=True)
    link = models.CharField(max_length=100000,null =True)
    date_created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.topic)
 

# create  Discussion model to discuss the topic of Forum
#child model
class Discussion(models.Model):
    forum = models.ForeignKey(Forum,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    discuss = models.TextField(max_length=1000000000)
 
    def __str__(self):
        return str(self.forum)






# # create commenting system model
# class Comment(models.Model):
#     content = models.ForeignKey(Content, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     body = models.TextField()
#     date = models.DateField(auto_now=True)
#     active = models.BooleanField(default=True)
#     def __str__(self):
#         return str(self.content)