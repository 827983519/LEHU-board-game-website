from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .recommend import recommend_store
import json
import datetime
from .models import Activity,User,Participant,Message,Store
import random






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
# def index(request):
#     return HttpResponse('hello')
# @auth
class IndexView(generic.ListView):
    template_name = 'LEHU/index.html'



# class ActivityPostView(generic.CreateView):
#     model = Activity
#     template_name = 'post.html'
#     fields = ('activity_title','Category','activity_content','numberofmem','start_date','start_time','budget','location')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['owner'] = self.request.session.get('logname',None)
#
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.session.get('logname',None)
#         self.object = form.save()
class PostForm(Form):
    title = fields.CharField(required=True)
    people =  fields.IntegerField(required=True)
    time =  fields.DateTimeField(required=True,input_formats=['%Y-%m-%dT%H:%M'])
    budget = fields.IntegerField(required=True)
    location = fields.CharField(required=True)
    content = fields.CharField(required=True)
    category = fields.IntegerField(required=True)

@auth
def post(request,have_message):
    if request.method == 'GET':
        return render(request,'post_new.html',{'Have_message':have_message})
    else:
        Session_logname = request.session.get('logname',None)

        input = PostForm(request.POST)
        a = {'user':'fail','msg':'Please fill in all information correctly'}

        if not input.is_valid():
            # print(input.errors)
            return HttpResponse(json.dumps(a))
        else:
            a = {'user':'correct','msg':'Please fill in all information correctly'}
            activity = Activity.objects.create(owner = Session_logname,numberofmem = input.cleaned_data['people'],
                                        activity_title = input.cleaned_data['title'], budget =input.cleaned_data['budget'] ,
                                        start_date =  input.cleaned_data['time'].date(),
                                        start_time = input.cleaned_data['time'].time(),
                                        location = input.cleaned_data['location'],
                                         activity_content = input.cleaned_data['content'],
                                        Category = input.cleaned_data['category'] )

        return HttpResponse(json.dumps(a))




class PostDetailView(generic.DetailView):
    model = Activity
    #template_name = 'LEHU/PostDetail.html'
    template_name = 'event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def join(request, activity_id):
        activity = get_object_or_404(Activity, pk=activity_id)
        status = activity.status
        r_member = activity.numberofmem
        owner = activity.owner
        activity_id = activity.activity_id
        activity_title = activity.activity_title

        if status != 1:
            return redirect('/join_fail')
        else:
            try:
                #user_input = request.POST.get('mytextbox')
                user_id = request.session.get('logname',None)
            except (KeyError, user_id.DoesNotExist):
                # Redisplay the question voting form.
                return render(request, 'LEHU/PostDetail.html', {
                    'error_message': "You didn't enter input.",
                })
            else:
                activity_instance = Participant.objects.create_activity(activity, user_id)
                #participant_instance = Participant.objects.create_participant(user_input)
                activity_instance.save()

                c_member = Participant.objects.member_count(activity)
                if c_member == r_member:
                    activity.status = 3
                    activity.save()

                # generate join message
                messagetext = "has joint"
                message_instance = Message.objects.create_message(activity_id, user_id, owner, messagetext, activity_title,2)
                message_instance.save()

                return HttpResponseRedirect('/index')
                # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class JoinFailedView(generic.TemplateView):
    # model = Activity
    template_name = 'LEHU/Join_fail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

# def modify(request, activity_id):
#         activity = get_object_or_404(Activity, pk=activity_id)
#         print(type(activity))
#         try:
#             user_input = request.POST.get('mytextbox')
#         except (KeyError, user_input.DoesNotExist):
#             # Redisplay the question voting form.
#             return render(request, 'LEHU/PostDetail.html', {
#                 'error_message': "You didn't enter input.",
#             })
#         else:
#             activity_instance = Participant.objects.create_activity(activity, user_input)
#             #participant_instance = Participant.objects.create_participant(user_input)
#             activity_instance.save()

#             return HttpResponseRedirect('/index')
#             # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



class ActivityUpdateView(generic.UpdateView, SuccessMessageMixin):
    model = Activity

    fields = ('activity_title','status','Category','activity_content','numberofmem','start_date','start_time','budget','location')
    template_name_suffix = '_update_form'
    success_message = 'List successfully saved!!!!'
    success_url = reverse_lazy('postlist')

    def form_valid(self, form):
        #form.instance.owner_user = self.request.user

        user_id = self.request.session.get('logname',None)
        print(user_id)
        activity = self.get_object()
        activity_id = activity.activity_id
        #print(type(activity_id))
        #activity = get_object_or_404(Activity, pk=activity_id)
        owner = activity.owner
        activity_title = activity.activity_title
        participant = Participant.objects.get_all_participant(activity_id)
        #print(participant)
        for person in participant:
            messagetext = "has updated"
            person = str(person)
            print(person)
            message_instance = Message.objects.create_message(activity_id, owner, person, messagetext, activity_title, 3)
            message_instance.save()
        #success_url = self.get_success_url()

        return super(ActivityUpdateView, self).form_valid(form)



def cancel(request, activity_id):
        #activity = get_object_or_404(Activity, pk=activity_id)
        #user_input = request.POST.get('mytextbox')
        user_id = request.session.get('logname',None)
        activity = get_object_or_404(Activity, pk=activity_id)
        activity_id = activity.activity_id
        #print(type(activity_id))
        #activity = get_object_or_404(Activity, pk=activity_id)
        owner = activity.owner
        activity_title = activity.activity_title
        participant = Participant.objects.get_all_participant(activity_id)
        #Activity.objects.filter(activity_id=activity_id).delete()
        #print(participant)
        for person in participant:
            messagetext = "has cancelled"
            person = str(person)
            print(person)
            message_instance = Message.objects.create_message(activity_id, owner, person, messagetext, activity_title, 4)
            message_instance.save()
        #success_url = self.get_success_url()
        Activity.objects.filter(activity_id=activity_id).delete()
        return HttpResponseRedirect('/index')


def quit(request, activity_id):
        #activity = get_object_or_404(Activity, pk=activity_id)
        #user_input = request.POST.get('mytextbox')

        user_id = request.session.get('logname',None)
        instance = Participant.objects.find_activity(activity_id=activity_id, participant = user_id)
        #participant = get_object_or_404(Participant, activity_id=activity_id, participant = user_input)
        instance.delete()
        activity = get_object_or_404(Activity, pk=activity_id)
        status = activity.status
        owner = activity.owner
        activity_id = activity.activity_id
        activity_title = activity.activity_title

        messagetext = "has quitted"
        message_instance = Message.objects.create_message(activity_id, user_id, owner, messagetext, activity_title, 1)
        message_instance.save()

        if status == 3:
            Activity.objects.filter(pk=activity_id).update(status=1)
        return HttpResponseRedirect('/index')




class loginForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password = fields.CharField(max_length=20,min_length=6,required=True)



class registerForm(Form):
    username = fields.CharField(max_length=20,min_length=6,required=True)
    password =  fields.CharField(max_length=20,min_length=6,required=True)
    confirmPassword =  fields.CharField(max_length=20,min_length=6,required=True)
    email = fields.EmailField(max_length=20,min_length=6,required=True)
    gender = fields.CharField(max_length = 7,required=True)






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
        request.session.clear()
        request.session.clear_expired()
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

        select_message = []

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
                                                 # '':activity_list
                                                  'Have_message':have_message})


@auth
def refresh_recommend(request,have_messgae):
    if request.method == 'POST':
        recommend_list = recommend_store(request)
        return HttpResponse(json.dumps(recommend_list))


@auth
def main(request,have_message):
    if request.method == 'GET':
        Session_logname = request.session.get('logname',None)
        Select_activity = Activity.objects.order_by('-pub_date').filter(~Q(owner=Session_logname))[:5]
        select_activity  = []
        for i in Select_activity:
            select_activity.append(i.to_dict())


        recommend_list = recommend_store(request)
        return render(request,'index_new.html',{'recommend':recommend_list,'Have_message':have_message

                                                ,'object_list':select_activity})
    else:
        Session_logname = request.session.get('logname',None)
        Select_activity = Activity.objects.order_by('-pub_date').filter(~Q(owner=Session_logname))[:100]
        recommend_num = []
        for i in range(5):
            recommend_num.append(random.randint(0,len(Select_activity)-1))

        select_activity  = []
        recommend_num = list(set(recommend_num))
        random.shuffle(recommend_num)
        for i in recommend_num:
            select_activity.append(Select_activity[i].to_dict())
        print(select_activity)
        return HttpResponse(json.dumps(select_activity, indent=4, sort_keys=True, default=str))




def logout(request):
    #del request.session['logname']
    request.session.clear()
    request.session.clear_expired()
    return redirect('/login')


# def search(request):
#     if request.method == 'GET':
#         return render(request,'search.html')
@auth
def search(request,have_message):
    if 'q' in request.GET:
        q = request.GET['q']
        if q == "":
            titles = None
        else:
            titles = Activity.objects.filter(activity_title__icontains=q)
        return render(request, './search.html', {'titles': titles, 'query': q,'Have_message':have_message})
    else:
        return redirect('/')

#request.session.clear_expired()
#request.session.set_expiry()
