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
import json

from .models import Activity,User,Picture,Participant,Message

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

# def index(request):
#     return HttpResponse('hello')
# @auth
class IndexView(generic.ListView):
    template_name = 'LEHU/index.html'

class ActivityPostView(generic.CreateView):
    model = Activity
    template_name = 'LEHU/post.html'
    fields = ('activity_title','Category','activity_content','numberofmem','start_date','start_time','budget','location')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.request.session.get('logname',None)
        return context

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        form.instance.owner = self.request.session.get('logname',None)
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
    #template_name = 'LEHU/event.html'
    
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
        #if status != 1 or owner == request.session.get('logname',None):
        if status != 1:
            return redirect('/join_fail')
            # messages.error(request, "Error")
            # return render(request, 'LEHU/PostDetail.html', {
            #     'error_message': "Selected activity is not available.",
            # })
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
                messagetext = user_id + " has joined " + activity_title + "!"
                message_instance = Message.objects.create_message(activity_id, user_id, owner, messagetext,2)
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
            messagetext = owner + " has updated " + activity_title + "!"
            person = str(person)
            print(person)
            message_instance = Message.objects.create_message(activity_id, owner, person, messagetext, 1)
            message_instance.save()
        #success_url = self.get_success_url()
    
        return super(ActivityUpdateView, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    # #def get_queryset(self):
    #     user_id = self.request.session.get('logname',None)
    #     print(user_id)
    #     activity = self.get_object()
    #     activity_id = activity.activity_id
    #     #print(type(activity_id))
    #     #activity = get_object_or_404(Activity, pk=activity_id)
    #     owner = activity.owner
    #     activity_title = activity.activity_title
    #     participant = Participant.objects.get_all_participant(activity_id)
    #     #print(participant)
    #     for person in participant:
    #         messagetext = owner + " has cancelled " + activity_title + "!"
    #         person = str(person)
    #         print(person)
    #         message_instance = Message.objects.create_message(activity, owner, person, messagetext, 1)
    #         message_instance.save()
    #     #success_url = self.get_success_url()
    #     #self.model.objects.filter(activity_id=activity_id).delete()
    #     return HttpResponseRedirect(self.success_url)

# class ActivityDeleteView(generic.DeleteView):
#     model = Activity
#     template_name_suffix = '_delete_confirm'
#     success_message = "Activity was deleted successfully."
#     success_url = reverse_lazy('postlist')

#     def delete(self, request, *args, **kwargs):
#     #def get_queryset(self):
#         user_id = self.request.session.get('logname',None)
#         print(user_id)
#         activity = self.get_object()
#         activity_id = activity.activity_id
#         #print(type(activity_id))
#         #activity = get_object_or_404(Activity, pk=activity_id)
#         owner = activity.owner
#         activity_title = activity.activity_title
#         participant = Participant.objects.get_all_participant(activity_id)
#         #print(participant)
#         for person in participant:
#             messagetext = owner + " has cancelled " + activity_title + "!"
#             person = str(person)
#             #print(person)
#             message_instance = Message.objects.create_message(activity, owner, person, messagetext, 1)
#             message_instance.save()
#         #success_url = self.get_success_url()
#         messages.success(self.request, self.success_message)
#         return super(ActivityDeleteView, self).delete(request, *args, **kwargs)
        #return self.request

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
            messagetext = owner + " has cancelled " + activity_title + "!"
            person = str(person)
            print(person)
            message_instance = Message.objects.create_message(activity_id, owner, person, messagetext, 1)
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

        messagetext = user_id + " has quitted " + activity_title + "!"
        message_instance = Message.objects.create_message(activity_id, user_id, owner, messagetext, 1)
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
            print(input.cleaned_data['username'])


            user = User.objects.create(user_username = input.cleaned_data['username'],
                                       user_password = make_password(input.cleaned_data['password']),
                                       user_email = input.cleaned_data['email'],
                                       user_gender = input.cleaned_data['gender']
                                       )
            return redirect('/login')



@auth
def main(request):
    #print
    # return render(request,'index_new.html')
    return redirect('/index')




def logout(request):
    #del request.session['logname']
    request.session.clear()
    request.session.clear_expired()
    return redirect('/login')


#request.session.clear_expired()
#request.session.set_expiry()
