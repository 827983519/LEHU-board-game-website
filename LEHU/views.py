from django.shortcuts import render
from .models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password

class loginForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password = fields.CharField(max_length=20,min_length=6,required=True)



class registerForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password =  fields.CharField(max_length=20,min_length=6,required=True)
    confirm_password =  fields.CharField(max_length=20,min_length=6,required=True)
    email = fields.EmailField(max_length=20,min_length=6,required=True)
    #gender = fields.ChoiceField(initial='Male',choices=(("Female", u'Female'), ("Male", u'Male')),widget=widgets.RadioSelect)
    gender = fields.CharField(max_length = 7,initial='Male',widget=widgets.RadioSelect(choices=(("Female", 'Female'), ("Male",'Male'))))


#unsalted_md5


def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    if request.method == "POST":
        input = loginForm(request.POST)

        if not input.is_valid():
            message = " Incorrect username or password. "
            return render(request,'login.html',{'message':message})

        Post_username = input.cleaned_data['username']
        Post_password = input.cleaned_data['password']
        print(Post_username)
        print(Post_password)
        Select_user = User.objects.filter(user_username=Post_username)
        if len(Select_user) == 0:
            return render(request,'login.html',{'message':message})

        if check_password( Post_password,Select_user[0].user_password):
            res = redirect('/')
            #res.set_cookie('logname',Post_username,max_age = 30,httponly=True)#expires  path='/li' | path='/'all urls can get this cookies
            request.session['logname'] = Post_username
            return res


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    if request.method == 'POST':
        input = registerForm(request.POST)
        input.is_valid()
        print(input.cleaned_data)

'''
        if not input.is_valid():
            return render(request,'register.html',{'errors':input.errors})

        Select_user = User.objects.filter(user_username= input.cleaned_data['username'])

        if len(Select_user>0):
            errors = {'username':['Username has already exists']}
            return render(request,'register.html',{'errors':errors})

        if input.cleaned_data['password'] != input.cleaned_data['confirm_password']:
            errors = {'password':['Inconsistent password entered twice']}
            return render(request,'register.html',{'errors':errors})

        else:
            user = User.objects.create(user_username = input.cleaned_data['username'],
                                       user_password = make_password(input.cleaned_data['password']),
                                       user_nickname = 'No name',
                                       user_email = input.cleaned_data['email']
                                                   )
'''

# def login(request):
#     if request.method == 'GET':
#         return render(request,'login.html')
#     else:
#         obj = loginForm(request.POST)
#         if obj.is_valid():
#             #obj.cleaned_data
#             return HttpResponse('Hello')
#         else:
#             return render(request,'login.html',{'error':obj.errors})




def auth(func):
    def inner(request,*args,**kwargs):
        Session_logname = request.session.get('logname',None)
        if not Session_logname:
            return redirect('/login')
        # try:
        #     v = request.get_signed_cookie('logname',salt='login')
        # except:
        #     return redirect('/login')
        return func(request,*args,**kwargs)
    return inner


@auth
def main(request):
    #print
    return render(request,'main.html')






# def login(request):
#     if request.method=='GET':
#         return render(request,'login.html')
#     if request.method == "POST":
#         Post_username = request.POST.get('username',None)
#         Post_password = request.POST.get('password',None)
#         message = " Incorrect username or password. "
#
#         if Post_username == None or Post_password == None or len(Post_username)>20 or len(Post_password)>20:
#             return render(request,'login.html',{'message':message})
#
#         Select_user = User.objects.filter(user_username=Post_username)
#
#         if len(Select_user) == 0:
#             return render(request,'login.html',{'message':message})
#
#         if Select_user[0].user_password == Post_password:
#             res = redirect('/')
#             #res.set_signed_cookie('logname',Post_username,salt='login')
#             #res.set_cookie('logname',Post_username,max_age = 30,httponly=True)#expires  path='/li' | path='/'all urls can get this cookies
#             request.session['logname'] = Post_username
#             return res


#request.session.clear_expired()
#request.session.set_expiry()


def logout(request):
    del request.session['logname']
    return redirect('/login')
