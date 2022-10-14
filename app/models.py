from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone




#Model do post
class Post(models.Model):
        reply_to = models.ForeignKey('self', null = True, on_delete=models.CASCADE,blank = True)
        yt_link = models.TextField(max_length = 20, null = True, blank = True)
        ncomments = models.IntegerField(default = 0)
        content = models.TextField(max_length=300, null = False)
        date_posted = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
        upvotes = models.IntegerField(default= 0)
        downvotes = models.IntegerField(default = 0)
        picture = models.ImageField(null = True, blank = True)
        date_created = models.DateTimeField(auto_now_add=True, null=False)
        reviewed = models.BooleanField(default = False)


        def __str__(self):
            return self.content

        def get_absolute_url(self):
            return reverse('post-detail', kwargs={'pk': self.pk})


#Model do Profile(Para incluir foto de perfil no user)
class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null = False, blank = False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)


    def __str__(self):
        return self.user.first_name

#Model do Anúncio
class Announcement(models.Model):
    CATEGORY = (
			('Comercial', 'Comercial'),
			('Voluntariado', 'Voluntariado'),
			) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    content = models.TextField(max_length=300, null = False)
    reports = models.IntegerField(default = 0)
    category = models.CharField(max_length=20,null = False, choices = CATEGORY)
    picture = models.ImageField(blank = True, null = True)
    title = models.TextField(max_length=20,null = False, blank = False)
    contact = models.TextField(max_length = 60, null = False, blank = False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    reviewed = models.BooleanField(default = False)


    def __str__(self):
	    return self.title

 





