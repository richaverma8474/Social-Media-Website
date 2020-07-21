from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.
class MyProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    name = models.CharField(max_length = 100)
    fname = models.CharField(max_length = 100, null=True,blank=True)
    lname = models.CharField(max_length = 100, null=True,blank=True)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=20, default="prefer not to say", choices=(("male","male"), ("female","female"), ("prefer not to say", "prefer not to say")))
    bio = models.TextField(null=True, blank= True)
    acc_type= models.CharField(max_length=10, default="student", choices=(("student", "student"), ("page", "page")))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    branch = models.CharField(max_length=15 ,default="IT", choices=(("IT","IT"), ("COE", "COE"), ("ECE", "ECE"), ("EE", "EE"), ("SE", "SE"), ("ENE", "ENE"), ("PCT", "PCT"), ("MCE", "MCE"), ("BT", "BT"), ("EP", "EP"), ("AE", "AE"), ("CE", "CE"), ("ME", "ME"), ("PIE", "PIE")))
    societies = models.CharField(default="None",max_length = 100)
    pic=models.ImageField(upload_to = "images\\", null=True , blank=True)
    def __str__(self):
        return "%s" % self.user

class MyPost(models.Model):
    pic=models.ImageField(upload_to = "images\\", null=True)
    subject = models.CharField(max_length = 200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, null=True, blank=True)
    def __str__(self):
        return "%s" % self.subject


class PostComment(models.Model):
    post = models.ForeignKey(MyPost,related_name='postcomments', on_delete=CASCADE)
    msg = models.TextField()
    commented_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20, null=True, blank=True, choices=(("racist","racist"), ("abbusing","abbusing")))

    def __str__(self):
        return self.msg



class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.liked_by


class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)


