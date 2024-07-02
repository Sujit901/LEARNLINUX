"""LearnLinux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LearnandQuiz.views import index_view, signup_view, login_view, logout_view, news, showStaff, deleteStaff, editForum, deleteForum
from django.conf.urls.static import static
from django.conf import settings
from LearnandQuiz.views import addLinux, addAds, addBanner, ads, banner, linux, editQuizQues, deleteQuizQues, showQuizQues, surestaff
from LearnandQuiz.views import deleteads, deletebanner, deletelinux, aboutus, terms, createStaff, editDiscuss, deleteDiscuss
from LearnandQuiz.views import editads, editbanner, editlinux, editcourse, deletecourse, editcontent, deletecontent
from LearnandQuiz.views import profile, editprofile, deleteprofile, PasswordChangeView, password_success
from LearnandQuiz.views import token_send, verify, success, error_page, staffSearchView, linuxSearchView, linuxDistrosSearchView
from django.contrib.auth import views as auth_views
from LearnandQuiz.views import addContent, learn, showCourse, addCourse, quiz, discussion, addQuestion, addInForum, addInDiscussion
from LearnandQuiz.views import sureads, surebanner, surecontent, surecourse, surelinux, sureprofile, surequestion, surediscuss, sureforum
# from LearnandQuiz.views import addComment, comments
# from LearnandQuiz.views import addComment
from LearnandQuiz.views import courseSearchView, questionSearchView, discussSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index_view'),
    path('signup/', signup_view, name='signup_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('addLinux/', addLinux, name='addLinux'),
    path('addBanner/', addBanner, name='addBanner'),
    path('addAds/', addAds, name='addAds'),
    path('banner/', banner, name='banner'),
    path('linux/', linux, name='linux'),
    path('ads/', ads, name='ads'),
    path('deletebanner/<int:id>/', deletebanner, name='deletebanner'),
    path('suredeletebanner/<int:id>/', surebanner, name='surebanner'),
    path('deleteads/<int:id>/', deleteads, name='deleteads'),
    path('suredeleteads/<int:id>/', sureads, name='sureads'),
    path('deletelinux/<name>/', deletelinux, name='deletelinux'),
    path('suredeletelinux/<name>/', surelinux, name='surelinux'),
    path('editlinux/<name>/', editlinux, name='editlinux'),
    path('editbanner/<int:id>/', editbanner, name='editbanner'),
    path('editads/<int:id>/', editads, name='editads'),
    path('news/', news, name='news'),
    path('profile/<int:id>/', profile, name='profile'),
    path('deleteprofile/<int:id>/', deleteprofile, name='deleteprofile'),
    path('suredeleteprofile/<int:id>/', sureprofile, name='sureprofile'),
    path('editprofile/<int:id>/', editprofile, name='editprofile'),
    ##########################################

    # change Password
    path('change_password/', PasswordChangeView.as_view(template_name="password/password_change.html"), name='change-password'),
    path('password_success/', password_success, name='password_success'),
    #########################################
    # path('social-auth/', include('social_django.urls', namespace='social')),

    # reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password/password_reset_form.html"),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),name='password_reset_complete'),
    #################################################

    # sigup email verification
    path('token/', token_send, name="token_send"),
    path('success/' , success, name='success'),
    path('verify/<auth_token>/', verify, name="verify"),
    path('error/', error_page, name="error"),
    #################################################
    
    path('addContent/', addContent, name='addContent'),
    path('learn/<course>/', learn, name='learn'),
    path('course/<name>/', showCourse, name='course'),
    path('addCourse/', addCourse, name='addCourse'),
    path('addQuestion/', addQuestion,name='addQuestion'),
    path('course/<name>/quiz/', quiz, name='quiz'),
    path('discussion/', discussion, name='discussion'),
    path('addInDiscussion/<int:id>', addInDiscussion, name='addInDiscussion'),
    path('addInForum/', addInForum, name='addInForum'),
    path('editforum/<int:id>/', editForum, name='editforum'),
    path('deleteforum/<int:id>/', deleteForum, name='deleteforum'),
    path('suredeleteforum/<int:id>', sureforum, name='sureforum'),
    path('editdiscuss/<int:id>/', editDiscuss, name='editdiscuss'),
    path('deletediscuss/<int:id>/', deleteDiscuss, name='deletediscuss'),
    path('suredeletediscuss/<int:id>', surediscuss, name='surediscuss'),
    #################################################

    path('aboutus/', aboutus, name='aboutus'),
    path('termsandcondition/', terms, name='terms'),
    path('editcourse/<course>/', editcourse, name='editcourse'),
    path('deletecourse/<course>/', deletecourse, name='deletecourse'),
    path('suredeletecourse/<course>/', surecourse, name='surecourse'),
    path('editcontent/<id>/', editcontent, name='editcontent'),
    path('deletecontent/<id>/', deletecontent, name='deletecontent'),
    path('suredeletecontent/<id>/', surecontent, name='surecontent'),
    path('showQuizQues/<name>/', showQuizQues, name='showQuizQues'),
    path('editQuizQues/<id>/', editQuizQues, name='editQuizQues'),
    path('deleteQuizQues/<id>/', deleteQuizQues, name='deleteQuizQues'),
    path('suredeletequestion/<id>/', surequestion, name='surequestion'),
    path('createStaff/', createStaff, name="createStaff"),
    path('staff/', showStaff, name='staff'),
    path('deleteStaff/<int:id>', deleteStaff, name='deleteStaff'),
    path('suredeletestaff/<int:id>', surestaff, name='surestaff'),
    path('staffsearch/', staffSearchView, name='staffsearch'),
    path('linuxsearch/', linuxSearchView, name='linuxsearch'),
    path('linuxdistrossearch/', linuxDistrosSearchView, name='linuxdistrossearch'),
    path('coursesearch/<name>/', courseSearchView, name='coursesearch'),
    path('questionsearch/<name>/', questionSearchView, name='questionsearch'),
    path('searchdiscuss/', discussSearchView, name='searchdiscuss'),

    # path('addcomment/<int:id>/', addComment, name='addcomment'),
    # path('comments/<id>/', comments, name='comments'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
