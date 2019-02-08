from django.shortcuts import render
from .models import User,Picture
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password
import json

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

class pictureForm(Form):
    picture = fields.ImageField()


def upload(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    if request.method == "POST":
        imgs=request.FILES.get('img')
        content = {
        'imgs':imgs,
    }
    print(imgs.name)

    imgs.name='nsssss'
    new = Picture()
    new.Image = imgs
    new.save()

    #for i in imgs:
    #    print(i.img.url)
    return render(request,'showimg.html',{'imgs':new})



def show_profile(request):
    Select_user = User.objects.filter(user_username=Session_username)
    if len(Select_user == 0):
        return redirect('/login')
    username = Select_user[0].user_username
    bio = Select_user[0].user_bio
    favourite = Select_user[0].user_favouritegame
    email = Select_user[0].user_email
    province = Select_user[0].user_province
    cellphone = Select_user[0].user_cellphone
    photo = Select_user[0].photo

    return HttpResponse('ddd')




def modify_profile(request):
    #显示页面
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        if not Session_logname:
            return redirect('/login')


        username = Select_user[0].user_username
        bio = Select_user[0].user_bio
        favourite = Select_user[0].user_favouritegame
        email = Select_user[0].user_email
        province = Select_user[0].user_province
        cellphone = Select_user[0].user_cellphone
        photo = Select_user[0].photo
        return HttpResponse('find')

    if request.method == 'POST':
        Select_user = User.objects.filter(user_username=Session_username)
        if len(Select_user == 0):
            return redirect('/login')

        username = request.POST.get('username',None)
        bio = request.POST.get('bio',None)
        favourite = request.POST.get('username',None)
        email = request.POST.get('bio',None)
        province = request.POST.get('username',None)
        cellphone = request.POST.get('bio',None)
        photo = request.FILES.get('photo')

        Select_user[0].user_username      = username
        Select_user[0].user_bio           = bio
        Select_user[0].user_favouritegame = favourite
        Select_user[0].email              = email
        Select_user[0].province           = province
        Select_user[0].cellphone          = cellphone
        Select_user[0].photo              = photo
        Select_user[0].save()

        return render(request,'showimg.html',{'imgs':new})



def login(request):
    if request.method=='GET':
        return render(request,'loginC.html')
    if request.method == "POST":
        input = loginForm(request.POST)
        a = {'user':'fail','msg':message}
        #数据格式不合适,登录失败
        if not input.is_valid():
            message = " Incorrect username or password. "
            #return render(request,'login.html',{'message':message})
            return HttpResponse(json.dumps(a))
        Post_username = input.cleaned_data['username']
        Post_password = input.cleaned_data['password']
        Select_user = User.objects.filter(user_username=Post_username)

        #username不存在,登录失败
        if len(Select_user) == 0:
            #return render(request,'loginC.html')
            return HttpResponse(json.dumps(a))

        #密码错误，登录失败
        if not check_password( Post_password,Select_user[0].user_password):
            return HttpResponse(json.dumps(a))

        #登陆成功
        else:
            #res = redirect('/')
            #res.set_cookie('logname',Post_username,max_age = 30,httponly=True)#expires  path='/li' | path='/'all urls can get this cookies
            request.session['logname'] = Post_username
            #return res
            a['user'] = 'success'
            return HttpResponse(json.dumps(a))




def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    if request.method == 'POST':
        input = registerForm(request.POST)

        if not input.is_valid():
            #return render(request,'register.html',{'errors':input.errors})
            a = {'register':'fail','msg':'Wrong input format'}
            return HttpResponse(json.dumps(a))

        Select_user = User.objects.filter(user_username= input.cleaned_data['username'])

        if len(Select_user>0):
            a = {'register':'fail','msg':'Usename already exists'}
            return HttpResponse(json.dumps(a))
            #return render(request,'register.html',{'errors':errors})

        if input.cleaned_data['password'] != input.cleaned_data['confirm_password']:
            a = {'register':'fail','msg':'Inconsistent password entered'}
            return HttpResponse(json.dumps(a))
            #return render(request,'register.html',{'errors':errors})
        else:
            user = User.objects.create(user_username = input.cleaned_data['username'],
                                       user_password = make_password(input.cleaned_data['password']),
                                       user_nickname = 'No name',
                                       user_email = input.cleaned_data['email']
                                       user_gender = input.cleaned_data['gender']
                                                   )


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




def logout(request):
    del request.session['logname']
    return redirect('/login')


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
