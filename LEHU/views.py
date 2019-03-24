from django.shortcuts import render
from .models import User,Activity,Participant,Message,Store
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .recommend import recommend_store
import json


class loginForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password = fields.CharField(max_length=20,min_length=6,required=True)



class registerForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password =  fields.CharField(max_length=20,min_length=6,required=True)
    confirmPassword =  fields.CharField(max_length=20,min_length=6,required=True)
    email = fields.EmailField(max_length=20,min_length=6,required=True)
    gender = fields.CharField(max_length = 7,required=True)




def auth(func):
    def inner(request,*args,**kwargs):
        Session_logname = request.session.get('logname',None)
        if not Session_logname:
            return redirect('/login')

        Select_message = Message.objects.filter(To=Session_logname).filter(Have_read=0)
        if len(Select_message) > 0:
           return func(request,1,*args,**kwargs)
        return func(request,0,*args,**kwargs)
    return inner




def get_profile_info(profile,Select_user):
    profile['city']          = Select_user[0].user_city
    profile['nickname']      = Select_user[0].user_nickname
    profile['bio']           = Select_user[0].user_bio
    profile['favouritegame'] = Select_user[0].user_favouritegame
    profile['email']         = Select_user[0].user_email
    profile['province']      = Select_user[0].user_province
    profile['cellphone']     = Select_user[0].user_cellphone
    profile['image']         = str(Select_user[0].user_image)



def get_favourite(f1,f2,f3):
    if f1 == "" and f2 == "" and f3 == "":
        return ""
    a = set([f1,f2,f3])
    f_set = [i for i in a]
    if "" in f_set:
        f_set.remove("")
    favourite = ""
    for i in f_set:
        favourite = favourite + i
        if i != f_set[-1]:
            favourite = favourite + ';'
    return favourite



@auth
def modify_profile(request,have_message):
    #显示页面
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        Session_profile = request.session.get('profile',None)
        if not Session_logname:
           return redirect('/login')

        if not Session_profile:
            Select_user = User.objects.filter(user_username=Session_logname)
            profile = {}
            get_profile_info(profile,Select_user)
            request.session['profile'] = profile
            Session_profile = profile

        return render(request,'profile_new.html',{'profile':Session_profile,
                                            'Have_message':have_message})
    #修改profile
    if request.method == 'POST':
        Session_logname = request.session.get('logname',None)
        Select_user = User.objects.filter(user_username=Session_logname)
        if len(Select_user) == 0:
            return redirect('/login')

        nickname = request.POST.get('nickname',None)
        bio = request.POST.get('bio',None)
        email = request.POST.get('email',None)
        favourite1 = request.POST.get('favourite1',None)
        favourite2 = request.POST.get('favourite2',None)
        favourite3 = request.POST.get('favourite3',None)
        province = request.POST.get('province',None)
        cellphone = request.POST.get('cellphone',None)
        photo = request.FILES.get('photo')
        city = request.POST.get('city')

        favourite = get_favourite(favourite1,favourite2,favourite3)

        if photo:
            Select_user[0].user_image  = photo

        Select_user[0].user_nickname         = nickname
        Select_user[0].user_bio              = bio
        Select_user[0].user_favouritegame    = favourite
        Select_user[0].user_email            = email
        Select_user[0].user_province         = province
        Select_user[0].user_cellphone        = cellphone

        Select_user[0].user_city             = city
        Select_user[0].save()

        profile = {}
        get_profile_info(profile,Select_user)
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
            return HttpResponse(json.dumps(a))

        #密码错误，登录失败
        if not check_password( Post_password,Select_user[0].user_password):
            return HttpResponse(json.dumps(a))
        #登陆成功
        else:
            request.session['logname'] = Post_username
            a['user'] = 'success'
            return HttpResponse(json.dumps(a))






def register(request):
    if request.method == "GET":
        logout(request)
        return render(request,'register_new.html')

    if request.method == "POST":
        input = registerForm(request.POST)
        if not input.is_valid():
            a = {'register':'fail','msg':'Wrong input format'}
            valid_data = input.cleaned_data
            try:
                input.cleaned_data['username']
                input.cleaned_data['password']
                input.cleaned_data['confirmPassword']
            except:
                a['msg'] = 'Username and password length need to be between 6 to 20.'
            a['valid_data'] = valid_data
            return HttpResponse(json.dumps(a))

        Select_user = User.objects.filter(user_username= input.cleaned_data['username'])

        if len(Select_user)>0:
            a = {'register':'fail','msg':'Usename already exists'}
            valid_data = input.cleaned_data
            valid_data['username'] = ''
            a['valid_data'] = valid_data
            return HttpResponse(json.dumps(a))


        if input.cleaned_data['password'] != input.cleaned_data['confirmPassword']:
            a = {'register':'fail','msg':'Inconsistent password entered'}
            valid_data = input.cleaned_data
            valid_data['confirmPassword'] = ''
            return HttpResponse(json.dumps(a))

        Select_user = User.objects.filter(user_email= input.cleaned_data['email'])
        if len(Select_user)>0:
            a = {'register':'fail','msg':'This Email has been used'}
            valid_data = input.cleaned_data
            valid_data['email'] = ''
            a['valid_data'] = valid_data
            return HttpResponse(json.dumps(a))

        else:
            a = {'register':'success'}
            user = User.objects.create(user_username = input.cleaned_data['username'],
                                       user_password = make_password(input.cleaned_data['password']),
                                       user_email = input.cleaned_data['email'],
                                       user_gender = input.cleaned_data['gender']
                                       )
            return HttpResponse(json.dumps(a))

    # if request.GET.pos('username',None):
    #     input = registerForm(request.GET)
    #     if not input.is_valid():
    #         a = {'register':'success','msg':'Wrong input format'}
    #         valid_data = input.cleaned_data
    #         return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})
    #     Select_user = User.objects.filter(user_username= input.cleaned_data['username'])
    #
    #     if len(Select_user)>0:
    #         a = {'register':'fail','msg':'Usename already exists'}
    #         valid_data = input.cleaned_data
    #         valid_data['username'] = ''
    #         return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})
    #
    #     if input.cleaned_data['password'] != input.cleaned_data['confirmPassword']:
    #         a = {'register':'fail','msg':'Inconsistent password entered'}
    #         valid_data = input.cleaned_data
    #         valid_data['password'] = ''
    #         valid_data['confirmPassword'] = ''
    #         return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})
    #
    #     Select_user = User.objects.filter(user_email= input.cleaned_data['email'])
    #     if len(Select_user)>0:
    #         a = {'register':'fail','msg':'This Email has been used'}
    #         valid_data = input.cleaned_data
    #         valid_data['email'] = ''
    #         return render(request,'register_new.html',{'valid_data':valid_data,'msg':a['msg']})
    #
    #     else:
    #         user = User.objects.create(user_username = input.cleaned_data['username'],
    #                                    user_password = make_password(input.cleaned_data['password']),
    #                                    user_email = input.cleaned_data['email'],
    #                                    user_gender = input.cleaned_data['gender']
    #                                    )
    #         return redirect('/login')



@auth
def activity(request,have_message):
    if request.method=='GET':
        Participant_list = []
        Session_logname = request.session.get('logname',None)
        Select_host = Activity.objects.filter(owner=Session_logname).filter(~Q(status=2))
        Select_participant = Participant.objects.filter(participant=Session_logname)
        No_host = 0
        No_participant = 0
        if len(Select_host) == 0:
            No_host = 1

        if len(Select_participant) == 0:
            No_participant = 1

        else:
            for activity in Select_participant:
                pickid = activity.activity_id

                pick_activity = Activity.objects.filter(activity_id=pickid.activity_id).filter(~Q(status=2))
                if len(pick_activity) == 0:
                    continue
                else:
                    Participant_list.append(pick_activity[0])
            if len(Participant_list) == 0:
                No_participant = 1
        return render(request,'activities.html',{'host_list':Select_host,
                                                 'activity_list':Participant_list,
                                                 'No_host':No_host,
                                                 'No_participant':No_participant,
                                                 'Have_message':have_message})

@auth
def history(request,have_message):
    Participant_list = []
    Session_logname = request.session.get('logname',None)
    Select_host = Activity.objects.filter(owner=Session_logname).filter(status=2).order_by('start_date')
    Select_participant = Participant.objects.filter(participant=Session_logname)
    No_host = 0
    No_participant = 0
    if len(Select_host) == 0:
        No_host = 1

    if len(Select_participant) == 0 :
        No_participant = 1

    else:
        for activity in Select_participant:
            pickid = activity.activity_id
            pick_activity = Activity.objects.order_by('start_date').filter(activity_id=pickid.activity_id).filter(status=2)
            if len(pick_activity) == 0:
                continue
            else:
                Participant_list.append(pick_activity[0])
        if len(Participant_list) == 0:
            No_participant = 1

    return render(request,'history.html',{'host_list':Select_host,
                                             'activity_list':Participant_list,
                                             'No_host':No_host,
                                             'No_participant':No_participant,
                                             'Have_message':have_message})


@auth
def view_other_profile(request,have_message,pick_user):

    Select_user = User.objects.filter(user_username=pick_user)
    if len(Select_user) == 0:
        return HttpResponse('404')

    return render(request,'show_profile.html',{'profile':Select_user[0],
                                        'Have_message':have_message})


@auth
def unread_message(request,have_message):
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        Select_message = Message.objects.filter(To=Session_logname).filter(Have_read=0)
        No_unread_message = 0

        if len(Select_message) == 0:
            No_unread_message = 1
        else:
            for single_message in Select_message:
                single_message.Have_read = 1
                single_message.save()

        return render(request,'Unread.html',{  'Unread_message_list':Select_message,
                                                 'No_unread_message':No_unread_message,
                                                 'Have_message':0})


@auth
def all_message(request,have_message):
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        Select_message = Message.objects.filter(To=Session_logname)

        No_message = 0

        if len(Select_message) == 0:
            No_message = 1

        return render(request,'Read.html',{'Message_list':Select_message,
                                                 'No_message':No_message,
                                                  'Have_message':have_message})


@auth
def refresh_recommend(request,have_messgae):
    if request.method == 'POST':
        recommend_list = recommend_store(request)
        return HttpResponse(json.dumps(recommend_list))


@auth
def main(request,have_message):
    recommend_list = recommend_store(request)
    return render(request,'index_new.html',{'recommend':recommend_list,'Have_message':have_message})




def logout(request):
    #del request.session['logname']
    request.session.clear()
    request.session.clear_expired()
    return redirect('/login')


# def search(request):
#     if request.method == 'GET':
#         return render(request,'search.html')

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q == "":
            titles = None
        else:
            titles = Activity.objects.filter(activity_title__icontains=q)
        return render(request, './search.html', {'titles': titles, 'query': q})
    else:
        return redirect('/')

#request.session.clear_expired()
#request.session.set_expiry()
