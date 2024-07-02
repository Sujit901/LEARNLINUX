from django.contrib.auth import models
from .models import CustomUser, Banner, Ads, LinuxDistribution
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Content, Course, Forum, Discussion, QuesModel

# create Banner Form
class AddBanner(ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

# create Linux Form
class AddLinux(ModelForm):
    class Meta:
        model = LinuxDistribution
        fields = "__all__"

# create ADS Form
class AddAds(ModelForm):
    class Meta:
        model = Ads
        fields = "__all__"

# create Edit profile form
class EditProfile(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["image","name"]

# create password change form
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]

# create add content form
class AddContent(ModelForm):
    class Meta:
      model = Content
      fields = "__all__"

# create add course form
class AddCourse(ModelForm):
    class Meta:
      model = Course
      fields = "__all__"

# create discussion forum
#############################################
class CreateInForum(ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"
 
class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = ["name", "email", "discuss"]

class EditForum(ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"
#############################################

# create Quiz Form
class addQuestionform(ModelForm):
    class Meta:
        model = QuesModel
        fields = "__all__"


# create Comment form
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name','email','body']


# create edit course
class EditCourse(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


# create edit content
class EditContent(ModelForm):
    class Meta:
        model = Content
        fields = "__all__"


# create edit quiz question form
class EditQuizQuestion(ModelForm):
    class Meta:
        model = QuesModel
        fields = "__all__"


# create staff form
class CreateStaff(ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"