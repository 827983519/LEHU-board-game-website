from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import Activity,User,Picture


# def index(request):
#     return HttpResponse('hello')

class IndexView(generic.ListView):
    template_name = 'LEHU/index.html'

class ActivityPostView(generic.CreateView):
    model = Activity
    template_name = 'LEHU/post.html'
    fields = ('activity_title','Category','activity_content','numberofmem','start_date','start_time','budget','location')

    def form_valid(self, form):
        self.object = form.save()
    # do something with self.object
    # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/index')

class PostListView(generic.ListView):
    model = Activity
    template_name = 'LEHU/index.html'
    context_object_name = 'latest_activity'

    def get_queryset(self):
        return Activity.objects.order_by('-pub_date')[:5]
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class PostDetailView(generic.DetailView):
    model = Activity
    template_name = 'LEHU/PostDetail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class loginForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password = fields.CharField(max_length=20,min_length=6,required=True)



class registerForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password =  fields.CharField(max_length=20,min_length=6,required=True)
    confirmPassword =  fields.CharField(max_length=20,min_length=6,required=True)
    email = fields.EmailField(max_length=20,min_length=6,required=True)
    gender = fields.CharField(max_length = 7,required=True)



#unsalted_md5
def upload(request):
    if request.method == 'GET':
        #return render(request,'index_new.html')
        return render(request,'upload.html')
    if request.method == "POST":
        imgs=request.FILES.get('img')
        content = {
        'imgs':imgs,
    }

    imgs.name='nsssss'
    new = Picture()
    new.Image = imgs
    new.save()
    print(new.Image)
    #for i in imgs:
    #    print(i.img.url)
    return render(request,'showimg.html',{'imgs':str(new.Image)})



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
def show_profile(request):
    Select_user = User.objects.filter(user_username=Session_username)
    if len(Select_user) == 0:
        return redirect('/login')
    nickname = Select_user[0].user_nickname
    bio = Select_user[0].user_bio
    favourite = Select_user[0].user_favouritegame
    email = Select_user[0].user_email
    province = Select_user[0].user_province
    cellphone = Select_user[0].user_cellphone
    photo = Select_user[0].photo

    return HttpResponse('ddd')



@auth
def modify_profile(request):
    #显示页面
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        Session_profile = request.session.get('profile',None)
        print(Session_profile)
        if not Session_logname:
           return redirect('/login')

        if not Session_profile:
            Select_user = User.objects.filter(user_username=Session_logname)
            profile = {}
            profile['city']          = Select_user[0].user_city
            profile['nickname']      = Select_user[0].user_nickname
            profile['bio']           = Select_user[0].user_bio
            profile['favouritegame'] = Select_user[0].user_favouritegame
            profile['email']         = Select_user[0].user_email
            profile['province']      = Select_user[0].user_province
            profile['cellphone']     = Select_user[0].user_cellphone
            profile['image']         = str(Select_user[0].user_image)

            request.session['profile'] = profile
            Session_profile = profile
        return render(request,'profile_new.html',{'profile':Session_profile})



    if request.method == 'POST':
        print("here")
        Session_logname = request.session.get('logname',None)
        Select_user = User.objects.filter(user_username=Session_logname)
        if len(Select_user) == 0:
            return redirect('/login')

        nickname = request.POST.get('nickname',None)
        bio = request.POST.get('bio',None)
        email = request.POST.get('email',None)
        favourite = request.POST.get('favouritegame',None)
        province = request.POST.get('province',None)
        cellphone = request.POST.get('cellphone',None)
        photo = request.FILES.get('photo')
        city = request.POST.get('city')

        Select_user[0].user_nickname         = nickname
        Select_user[0].user_bio              = bio
        Select_user[0].user_favouritegame    = favourite
        Select_user[0].user_email            = email
        Select_user[0].user_province         = province
        Select_user[0].user_cellphone        = cellphone
        Select_user[0].user_image            = photo
        Select_user[0].user_city             = city
        Select_user[0].save()

        profile = {}
        profile['city']          = Select_user[0].user_city
        profile['nickname']      = Select_user[0].user_nickname
        profile['bio']           = Select_user[0].user_bio
        profile['favouritegame'] = Select_user[0].user_favouritegame
        profile['email']         = Select_user[0].user_email
        profile['province']      = Select_user[0].user_province
        profile['cellphone']     = Select_user[0].user_cellphone
        profile['image']         = str(Select_user[0].user_image)

        request.session['profile'] = profile
        return HttpResponse(json.dumps(request.session['profile']))





def login(request):
    if request.method=='GET':
        logout(request)
        return render(request,'login_new.html')
    if request.method == "POST":
        input = loginForm(request.POST)
        a = {'user':'fail','msg':'Username or password is worng'}
        #数据格式不合适,登录失败
        if not input.is_valid():
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
    if not request.GET.get('username',None):
        logout(request)
        return render(request,'register_new.html')

    if request.GET.get('username',None):
        input = registerForm(request.GET)
        if not input.is_valid():
            a = {'register':'success','msg':'Wrong input format'}
            valid_data = input.cleaned_data
            return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})
        Select_user = User.objects.filter(user_username= input.cleaned_data['username'])

        if len(Select_user)>0:
            a = {'register':'fail','msg':'Usename already exists'}
            valid_data = input.cleaned_data
            valid_data['username'] = ''
            return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})

        if input.cleaned_data['password'] != input.cleaned_data['confirmPassword']:
            a = {'register':'fail','msg':'Inconsistent password entered'}
            valid_data = input.cleaned_data
            valid_data['password'] = ''
            valid_data['confirmPassword'] = ''
            return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})

        Select_user = User.objects.filter(user_email= input.cleaned_data['email'])
        if len(Select_user)>0:
            a = {'register':'fail','msg':'This Email has been used'}
            valid_data = input.cleaned_data
            valid_data['email'] = ''
            return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})

        else:


            user = User.objects.create(user_username = input.cleaned_data['username'],
                                       user_password = make_password(input.cleaned_data['password']),
                                       user_email = input.cleaned_data['email'],
                                       user_gender = input.cleaned_data['gender']
                                       )
            return redirect('/login')



@auth
def main(request):
    #print
    return render(request,'index_new.html')




def logout(request):
    #del request.session['logname']
    request.session.clear()
    request.session.clear_expired()
    return redirect('/login')


#request.session.clear_expired()
#request.session.set_expiry()
