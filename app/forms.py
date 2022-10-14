from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Post, Announcement
from django.forms import ModelForm
# Form de login
class loginForm(forms.Form):
    user = forms.CharField()
    passwords = forms.CharField(widget=forms.PasswordInput)

    #Form de criação do user
class userForm(UserCreationForm):
    username = forms.CharField(required=True, min_length= 5, max_length=30)
    first_name = forms.CharField(required=True, min_length= 5, max_length=30)
    last_name = forms.CharField(required=True, min_length= 5, max_length=30)
    email = forms.EmailField(required=True, min_length= 10, max_length=50)
    class Meta:
        model = User
        fields = {'first_name','username','last_name','email','password1','password2'}    

    def save(self, commit=True):
        user = super(userForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

#Forms de update do user e do profile
class UserChange(UserChangeForm):
    class Meta:
        model = User
        fields = {'username','first_name','last_name','email'}

         
                            
class ProfileForm(ModelForm):
        class Meta:
            model= Profile
            fields = {'profile_pic'}
                
            


        






