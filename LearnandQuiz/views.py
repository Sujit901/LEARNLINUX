import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, LinuxDistribution, Banner, Ads, Profile
from django.core.files.storage import FileSystemStorage
from newsapi import *
from .forms import AddAds, AddBanner, AddLinux, EditProfile, PasswordChangingForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import QuesModel, Forum, Content, Course
from .forms import CreateInDiscussion, CreateInForum, AddContent, AddCourse, addQuestionform
import random
from random import randint
from .forms import *
import random
import itertools
from django.db import models
# Create your views here.

##################################################################################################
##########***** INDEX, ABOUTUS, SINGUP, EMAIL, LOGIN, LOGOUT *****##########

# index or landing page view
def index_view(request):
    banner = Banner.objects.all()
    linux = LinuxDistribution.objects.all()
    ads = Ads.objects.all()
    context = {
        'banner':banner,
        'linux':linux,
        'ads':ads,
    }
    return render(request, 'index.html', context)


#signup view
# def signup_view(request):
#  success = None
#  if request.method=='POST':
#     image = request.FILES.get('image')
#     email = request.POST.get('email')
#     name = request.POST.get('name')
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     confirm_password = request.POST.get('password2')
#     if CustomUser.objects.filter(email= request.POST.get('email')).exists():
#         error = "This email is already taken"
#         return render(request, 'signup.html', {'error': error})
#     if CustomUser.objects.filter(username= request.POST.get('username')).exists():
#         error = "This username is already taken"
#         return render(request, 'signup.html', {'error': error})
#     if password!=confirm_password:
#         error = "Password and Confirm Password doesn't match"
#         return render(request, 'signup.html', {'error': error})
#     import uuid
#     filename = f"{uuid.uuid4().hex}.{image.name.split('.')[-1]}"
#     fs = FileSystemStorage()
#     fs.save(filename, image)
#     new_user = CustomUser.objects.create_user(username=username, name=name, email=email, image=filename, password=password)
#     user = new_user.save()
#     user.save()
#     success = "New User Created Successfully !"
#  return render(request,'signup.html', {'success':success})
def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        try:
            if CustomUser.objects.filter(email = email).first():
                error = "Email has been already taken!!."
                return render(request,'signup.html', {'error':error})
            
            if CustomUser.objects.filter(username = username).first():
                error = "Username is already taken."
                return render(request,'signup.html', {'error':error})
            
            if password != confirm_password:
                error = "Password and Confirm Password don't match!!!."
                return render(request, 'signup.html',{'error':error})
            
            filename = f"{uuid.uuid4().hex}.{image.name.split('.')[-1]}"
            fs = FileSystemStorage()
            fs.save(filename, image)
            user_obj = CustomUser(username = username , email = email, name = name, image = filename)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('token_send')
        except Exception as e:
            print(e)
    return render(request , 'signup.html')


# create success view of signup
def success(request):
    return render(request , 'email/success.html')

# create Token_send view for signup
def token_send(request):
    return render(request , 'email/token_send.html')


# verify view
def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                success="Your account is already verified."
                return render(request,'login.html', {'success':success})
            profile_obj.is_verified = True
            profile_obj.save()
            success = "Your account has been verified."
            return render(request,'login.html', {'success':success})
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

# error view
def error_page(request):
    return  render(request , 'email/error.html')

# send mail view
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

#login view
# def login_view(request):
#     error = None
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user:
#             login(request, user)
#             return redirect("index_view")
#         else:
#             error = "Invalid Credentials !!! Signup to create account"
#     return render(request, "login.html", {'error':error})
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = CustomUser.objects.filter(email=email).first()
        if user_obj is None:
            error ="User not found!!!."
            return render(request,'login.html',{'error':error})
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            error ="Profile is not verified check your mail."
            return render(request,'login.html',{'error':error})

        user = authenticate(request, email = email , password = password)
        if user is None:
            error = "Invalid Credentials !!! Signup to create account."
            return render(request,'login.html',{'error':error})
        
        login(request , user)
        return redirect('index_view')

    return render(request , 'login.html')

# logout view
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect('login_view')

# aboutus view
def aboutus(request):
    return render(request, "aboutus.html")


# terms view
def terms(request):
    return render(request, "terms.html")
##################################################################################################


##################################################################################################
##########***** NEWS *****##########

# news view using api
def news(request):
    newsapi = NewsApiClient(api_key='3c92d382172947658da9c876ad5f8078')
    linux_news = newsapi.get_everything(q="linux", language="en", sort_by="publishedAt")
    a = linux_news['articles']
    description = []
    title = []
    image = []
    url = []
    publish = []

    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        description.append(f['description'])
        image.append(f['urlToImage'])
        url.append(f['url'])
        publish.append(f['publishedAt'])
    
    mylist = zip(title, image, description, url , publish)
    context = {'mylist':mylist}

    return render(request, "news.html", context)
##################################################################################################


##################################################################################################
##########***** ADS, BANNER, LINUX *****###########

# create add banner view
@login_required(login_url="/login/")
def addBanner(request):
    if request.user.is_staff:
        form=AddBanner()
        if(request.method=='POST'):
            form=AddBanner(request.POST, request.FILES)
            if(form.is_valid()):
                form.save()
                return redirect('banner')
        context={'form':form}
        return render(request,'addBanner.html',context)
    return redirect('index_view')

# create add ads view
@login_required(login_url="/login/")
def addAds(request):
    if request.user.is_staff:
        form=AddAds()
        if(request.method=='POST'):
            form=AddAds(request.POST, request.FILES)
            if(form.is_valid()):
                form.save()
                return redirect('ads')
        context={'form':form}
        return render(request,'addAds.html',context)
    return redirect('index_view')

# create add linux view
@login_required(login_url="/login/")
def addLinux(request):
    if request.user.is_staff:
        form=AddLinux()
        if(request.method=='POST'):
            form=AddLinux(request.POST, request.FILES)
            if(form.is_valid()):
                form.save()
                return redirect('linux')
        context={'form':form}
        return render(request,'addLinux.html',context)
    return redirect('index_view')
 
# create delete banner view
@login_required(login_url="/login/")
def deletebanner(request, id):
    if request.user.is_staff:
        banner = Banner.objects.get(id=id)
        banner.delete()
        return redirect('banner')
    return redirect('index_view')

# create sure delete ads view
@login_required(login_url="/login/")
def surebanner(request, id):
    if request.user.is_staff:
        banner = Banner.objects.get(id=id)
        context = {
            'banner':banner
        }
        return render(request, 'surebanner.html', context)
    return redirect('index_view')


# create delete ads view
@login_required(login_url="/login/")
def deleteads(request, id):
    if request.user.is_staff:
        ads = Ads.objects.get(id=id)
        ads.delete()
        return redirect('ads')
    return redirect('index_view')

# create sure delete ads view
@login_required(login_url="/login/")
def sureads(request, id):
    if request.user.is_staff:
        ads = Ads.objects.get(id=id)
        context = {
            'ads':ads
        }
        return render(request, 'sureads.html', context)
    return redirect('index_view')


# create delete linux view
@login_required(login_url="/login/")
def deletelinux(request, name):
    if request.user.is_staff:
        product = LinuxDistribution.objects.filter(pk=name)
        product.delete()
        return redirect('linux')
    return redirect('index_view')


# create sure delete linux view
@login_required(login_url="/login/")
def surelinux(request, name):
    if request.user.is_staff:
        linux = LinuxDistribution.objects.filter(pk=name)
        context = {
            'linux':linux
        }
        return render(request, 'surelinux.html', context)
    return redirect('index_view')

# create edit banner view
@login_required(login_url="/login/")
def editbanner(request, id):
    if request.user.is_staff:
        banner = Banner.objects.get(id=id)
        form = AddBanner(instance=banner)
        if request.method == "POST":
            banner = Banner.objects.get(id=id)
            form = AddBanner(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                return redirect('banner')
        return render(request,'editbanner.html', {'form':form})
    return redirect('index_view')

# create edit ads view
@login_required(login_url="/login/")
def editads(request, id):
    if request.user.is_staff:
        ads = Ads.objects.get(id=id)
        form = AddAds(instance=ads)
        if request.method == "POST":
            ads = Ads.objects.get(id=id)
            form = AddAds(request.POST, request.FILES, instance=ads)
            if form.is_valid():
                form.save()
                return redirect('ads')
        return render(request,'editads.html', {'form':form})
    return redirect('index_view')

# create edit linux view
@login_required(login_url="/login/")
def editlinux(request, name):
    if request.user.is_staff:
        product = LinuxDistribution.objects.get(pk=name)
        form = AddLinux(instance=product)
        if request.method == "POST":
            product = LinuxDistribution.objects.get(pk=name)
            form = AddLinux(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('linux')
        return render(request,'editlinux.html', {'form':form})
    return redirect('index_view')

# create linux view to see all distributions of linux
@login_required(login_url="/login/")
def linux(request):  
    if request.user.is_staff:
        linux = LinuxDistribution.objects.all()
        context = {
            'linux':linux
        }
        return render(request, 'linux.html', context)
    return redirect('index_view')

# create banner view to see all the added banner in the banner page
@login_required(login_url="/login/")
def banner(request):
    if request.user.is_staff:
        banner = Banner.objects.all()
        context = {
            'banner':banner
        }
        return render(request, 'banner.html', context)
    return redirect('index_view')

# create ads view to see all the added banner in the banner page
@login_required(login_url="/login/")
def ads(request):
    if request.user.is_staff:
        ads = Ads.objects.all()
        context = {
            'ads':ads
        }
        return render(request, 'ads.html', context)
    return redirect('index_view')
##################################################################################################


##################################################################################################
##########***** Profile  *****##########

# create profile view to see the profile
@login_required(login_url="/login/")
def profile(request, id):
    account = CustomUser.objects.get(id=id)
    context = {
        'account':account
    }
    return render(request, 'profile.html', context)

# create profile edit view to edit the profile
@login_required(login_url="/login/")
def editprofile(request, id):
    success= None
    account = CustomUser.objects.get(id=id)
    form = EditProfile(instance=account)
    if request.method == "POST":
        account = CustomUser.objects.get(id=id)
        form = EditProfile(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            success = "Update Successfully. Please referesh !!!"
            return render(request, 'profile.html', {'success':success})
    return render(request,'editprofile.html', {'form':form})

# create profile delete view to delete the profile from the application
@login_required(login_url="/login/")
def deleteprofile(request, id):
    account = CustomUser.objects.get(id=id)
    account.delete()
    return redirect('login_view')



# create sure delete profile view
@login_required(login_url="/login/")
def sureprofile(request, id):
    account = CustomUser.objects.get(id=id)
    context = {
        'account':account
    }
    return render(request, 'sureprofile.html', context)
##################################################################################################


##################################################################################################
##########***** PASSWORD *****##########

# create password change view
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, "password/password_change_success.html")
##################################################################################################


##################################################################################################
##########*****Quiz, Content, Course*****##########

# create quiz game view
@login_required(login_url="/login/")
def quiz(request, name):
    pame = LinuxDistribution.objects.get(pk=name)
    if request.method == 'POST':
        questions=QuesModel.objects.filter(category=pame)
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'pame':pame,
        }
        return render(request,'result.html',context)
    else:
        questions=QuesModel.objects.filter(category=pame)
        permutations = list(itertools.permutations(questions))
        shuffled_lst = random.choice(permutations)
        # randomQuestion= random.shuffle(questions)
        # print("QU",randomQuestion)
        context = {
            'questions':shuffled_lst,
        }
        return render(request,'quiz.html',context)



# crate views of discussion forum
@login_required(login_url="/login/")
def discussion(request):
    forums=Forum.objects.all()
    discuss = Discussion.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
    context={'forums':forums,
              'count':count,
              'discussions':discussions,
              'discuss':discuss,
              }
    return render(request,'discussion.html',context)
 

# create add in forum of discussion
@login_required(login_url="/login/")
def addInForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discussion')
    context ={'form':form}
    return render(request,'addInForum.html',context)

@login_required(login_url="/login/")
def editForum(request, id):
    forum = Forum.objects.get(id=id)
    form = EditForum(instance=forum)
    if request.method == 'POST':
        form = EditForum(request.POST,instance=forum)
        if form.is_valid():
            form.save()
            return redirect('discussion')
    context ={'form':form}
    return render(request, 'editforum.html', context)

@login_required(login_url="/login/")
def deleteForum(request, id):
    forum = Forum.objects.get(pk=id)
    forum.delete()
    return redirect('discussion')


# create sure delete discuss view
@login_required(login_url="/login/")
def sureforum(request, id):
    field_name = 'email'
    obj = Forum.objects.first()
    field_object = Forum._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    if request.user.email==field_value:
        forum = Forum.objects.get(id=id)
        context = {
            'forum':forum
        }
        return render(request, 'sureforum.html', context)
    return redirect('index_view')


# create add discussion view
@login_required(login_url="/login/")
def addInDiscussion(request, id):
    forum = Forum.objects.get(id=id)
    discuss = Discussion.objects.filter(forum = forum)
    form = CreateInDiscussion()
    new_discuss = None
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            new_discuss = form.save(commit=False)
            new_discuss.forum = forum
            new_discuss.save()
            return redirect('discussion')
    context ={'form':form,
              'discuss':discuss,
              'forum':forum}
    return render(request,'addInDiscussion.html',context)


@login_required(login_url="/login/")
def editDiscuss(request, id):
    discuss = Discussion.objects.get(id=id)
    form = CreateInDiscussion(instance=discuss)
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST,instance=discuss)
        if form.is_valid():
            form.save()
            return redirect('discussion')
    context ={'form':form}
    return render(request, 'editdiscuss.html', context)

@login_required(login_url="/login/")
def deleteDiscuss(request, id):
    discuss = Discussion.objects.get(pk=id)
    discuss.delete()
    return redirect('discussion')

# create sure delete discuss view
@login_required(login_url="/login/")
def surediscuss(request, id):
    field_name = 'email'
    obj = Discussion.objects.first()
    field_object = Discussion._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    if request.user.email==field_value:
        discuss = Discussion.objects.get(id=id)
        context = {
            'discuss':discuss
        }
        return render(request, 'surediscuss.html', context)
    return redirect('index_view')


# create add content view
@login_required(login_url="/login/")
def addContent(request):
    form = AddContent()
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddContent(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index_view')
        return render(request, 'ADDCONTENT.html',{'form':form})
    return redirect('index_view')


# create learn view
def learn(request, course):
    pame = Course.objects.get(pk=course)
    content = Content.objects.filter(category=pame)
    context={
        'content':content,
        'pame':pame,
        }
    return render(request,'learn.html',context)


# create edit content view
@login_required(login_url="/login/")
def editcontent(request, id):
    if request.user.is_staff:
        c = Content.objects.get(pk=id)
        form = EditContent(instance=c)
        if request.method == "POST":
            c = Content.objects.get(pk=id)
            form = EditContent(request.POST, request.FILES, instance=c)
            if form.is_valid():
                form.save()
                return redirect('index_view')
        return render(request,'editcontent.html', {'form':form})
    return render(request, 'login.html')


# create add course view
@login_required(login_url="/login/")
def addCourse(request):
    form = AddCourse()
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddCourse(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index_view')
        return render(request, 'addcourse.html',{'form':form})
    return redirect('index_view')


# create delete content view
@login_required(login_url="/login/")
def deletecontent(request, id):
    if request.user.is_staff:
        c = Content.objects.get(pk=id)
        c.delete()
        return redirect('index_view')
    return render(request, 'login.html')


# create sure delete content view
@login_required(login_url="/login/")
def surecontent(request, id):
    if request.user.is_staff:
        c = Content.objects.get(pk=id)
        context = {
            'c':c
        }
        return render(request, 'surecontent.html', context)
    return redirect('index_view')



# create show course view
def showCourse(request, name):
    pame = LinuxDistribution.objects.get(pk=name)
    course=Course.objects.filter(category=pame)
    context={
        'course':course,
        'pame':pame,
        }
    return render(request,'course.html',context)


# create edit course view
@login_required(login_url="/login/")
def editcourse(request, course):
    if request.user.is_staff:
        c = Course.objects.get(pk=course)
        form = EditCourse(instance=c)
        if request.method == "POST":
            c = Course.objects.get(pk=course)
            form = EditCourse(request.POST, request.FILES, instance=c)
            if form.is_valid():
                form.save()
                return redirect('index_view')
        return render(request,'editcourse.html', {'form':form})
    return render(request, 'login.html')


# create delete course view
@login_required(login_url="/login/")
def deletecourse(request, course):
    if request.user.is_staff:
        c = Course.objects.get(pk=course)
        c.delete()
        return redirect('index_view')
    return render(request, 'login.html')


# create sure delete course view
@login_required(login_url="/login/")
def surecourse(request, course):
    if request.user.is_staff:
        c = Course.objects.get(pk=course)
        context = {
            'c':c
        }
        return render(request, 'surecourse.html', context)
    return redirect('index_view')



# create add quiz question view
@login_required(login_url="/login/")
def addQuestion(request):    
    form=addQuestionform()
    if request.user.is_staff:
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('addQuestion')
        context={'form':form}
        return render(request,'addQuestion.html',context)
    return redirect('index_view')
##################################################################################################


##################################################################################################
##########*****Comment*****##########

# show comment
# def comments(request, id):
#     contents = Content.objects.get(pk=id)
#     comment = Comment.objects.filter(content = contents)
#     context = {
#         'comment':comment,
#     }
#     return render(request,'learn.html',context)

# add comment
# @ login_required(login_url="/login/")
# def addComment(request, id):
#     c = Content.objects.get(pk=id)
#     comments = Comment.objects.filter(content=c)
#     new_comment = None
#     if request.method == 'POST':
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.content = c
#             new_comment.save()
#     else:
#         form = CommentForm()
#     context = {
#         'comments':comments,
#         'new_comment':new_comment,
#         'form':form,
#         'c':c
#     }
#     return render(request, 'learn.html', context)
##################################################################################################


##################################################################################################
##########*****Edit delete quiz questions*****##########

# create show question view
@login_required(login_url="/login/")
def showQuizQues(request, name):
    if request.user.is_staff:
        pame = LinuxDistribution.objects.get(pk=name)
        questions=QuesModel.objects.filter(category=pame)
        context = {
            'questions':questions,
            'pame':pame
        }
        return render(request, 'showquizquestion.html', context)
    return redirect('/')

# create edit question view
@login_required(login_url="/login/")
def editQuizQues(request, id):
    if request.user.is_staff:
        a = QuesModel.objects.get(pk=id)
        form = EditQuizQuestion(instance=a)
        if request.method == 'POST':
            a = QuesModel.objects.get(id=id)
            form = EditQuizQuestion(request.POST, instance=a)
            if form.is_valid():
                form.save()
                return redirect('/')
        context = {
            'form':form
        }
        return render(request, 'editquizquestion.html', context)
    return redirect('index_view')


# create delete quiz question view
@login_required(login_url="/login/")
def deleteQuizQues(request, id):
    if request.user.is_staff:
        q = QuesModel.objects.get(pk=id)
        q.delete()
        return redirect('/')
    return redirect('index_view')



# create sure delete quiz question view
@login_required(login_url="/login/")
def surequestion(request, id):
    if request.user.is_staff:
        q = QuesModel.objects.get(pk=id)
        context = {
            'q':q
        }
        return render(request, 'surequestion.html', context)
    return redirect('index_view')
##################################################################################################

##################################################################################################
##########*****create staff*****##########
@login_required(login_url="/login/")
def createStaff(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('password2')
            try:
                if CustomUser.objects.filter(email = email).first():
                    error = "Email has been already taken!!."
                    return render(request,'createstaff.html', {'error':error})
                
                if CustomUser.objects.filter(username = username).first():
                    error = "Username is already taken."
                    return render(request,'createstaff.html', {'error':error})
                
                if password != confirm_password:
                    error = "Password and Confirm Password don't match!!!."
                    return render(request, 'createstaff.html',{'error':error})
                user_obj = CustomUser(username = username , email = email, name = name, is_staff=True)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
                profile_obj.is_verified = True
                profile_obj.save()
                return redirect('staff')
            except Exception as e:
                print(e)
        return render(request , 'createstaff.html')
    return redirect('/')
##################################################################################################



##################################################################################################
##########*****staff*****##########

# create staff view 
@login_required(login_url="/login/")
def showStaff(request):
    if request.user.is_superuser:
        staff = CustomUser.objects.filter(is_staff=True, is_superuser=False)
        context = {
            'staff':staff
        }
        return render(request, 'staff.html', context)
    return redirect('/')

# create staff view 
@login_required(login_url="/login/")
def deleteStaff(request, id):
    if request.user.is_superuser:
        s = CustomUser.objects.filter(is_staff=True, id=id)
        s.delete()
        staff = CustomUser.objects.filter(is_staff=True, is_superuser=False)
        context = {
            'staff': staff,
        }
        return render(request, 'staff.html', context)
    return redirect('/')


# create sure delete staff view
@login_required(login_url="/login/")
def surestaff(request, id):
    if request.user.is_superuser:
        staff = CustomUser.objects.filter(is_staff=True, id=id)
        context = {
            'staff':staff
        }
        return render(request, 'surestaff.html', context)
    return redirect('/')
##################################################################################################



##################################################################################################
##########*****SearchStaff*****##########
@login_required(login_url="/login/")
def staffSearchView(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        post = CustomUser.objects.filter(models.Q(name__icontains=query) | models.Q(email__icontains=query) | models.Q(username__icontains=query))
        staff = CustomUser.objects.filter(is_staff=True, is_superuser = False)
        context = {
            'staff':staff,
            'post': post,
        }
        return render(request, 'searchstaff.html', context)
    

def linuxSearchView(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        post = LinuxDistribution.objects.filter(models.Q(name__icontains=query))
        linux = LinuxDistribution.objects.all()
        context = {
            'linux': linux,
            'post': post,
        }
        return render(request, 'searchlinux.html', context)
    


@login_required(login_url="/login/")
def linuxDistrosSearchView(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        post = LinuxDistribution.objects.filter(models.Q(name__icontains=query))
        linux = LinuxDistribution.objects.all()
        context = {
            'linux': linux,
            'post': post,
        }
        return render(request, 'searchlinuxdistros.html', context)
    


def courseSearchView(request, name):
    if request.method == 'GET':
        query = request.GET.get('search')
        pame = LinuxDistribution.objects.get(pk=name)
        course = Course.objects.filter(category=pame)
        if course:
            post = Course.objects.filter(models.Q(coursename__icontains=query))
            context = {
                'course': course,
                'post': post,
                'pame': pame,
            }
        return render(request, 'searchcourse.html', context)
    

@login_required(login_url="/login/")
def questionSearchView(request, name):
    if request.method == 'GET':
        query = request.GET.get('search')
        pame = LinuxDistribution.objects.get(pk=name)
        questions = QuesModel.objects.filter(category=pame)
        if questions:
            post = QuesModel.objects.filter(models.Q(question__icontains=query) | models.Q(ans__icontains=query) | models.Q(op1__icontains=query) | models.Q(op2__icontains=query) | models.Q(op3__icontains=query) | models.Q(op4__icontains=query))
            context = {
                'questions': questions,
                'post': post,
                'pame': pame,
            }
        return render(request, 'searchquestions.html', context)
    


@login_required(login_url="/login/")
def discussSearchView(request):
    if request.method == 'GET':
        forums=Forum.objects.all()
        discuss = Discussion.objects.all()
        count=forums.count()
        d = discuss.count()
        discussions=[]
        for i in forums:
            discussions.append(i.discussion_set.all())
        query = request.GET.get('search')
        post = Forum.objects.filter(models.Q(name__icontains=query) | models.Q(email__icontains=query) | models.Q(topic__icontains=query))
        forum = Forum.objects.all()
        context = {
            'forum': forum,
            'post': post,
            'forums':forums,
            'count':count,
            'discussions':discussions,
            'discuss':discuss,
            'd':d,
        }
        return render(request, 'searchdiscuss.html', context)
##################################################################################################