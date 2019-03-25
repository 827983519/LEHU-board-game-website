from django.shortcuts import render
from .models import User,Activity,Participant,Message,Store
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms import Form,fields,widgets
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
import random



def get_profile_info(profile,Select_user):
    profile['city']          = Select_user[0].user_city
    profile['nickname']      = Select_user[0].user_nickname
    profile['bio']           = Select_user[0].user_bio
    profile['favouritegame'] = Select_user[0].user_favouritegame
    profile['email']         = Select_user[0].user_email
    profile['province']      = Select_user[0].user_province
    profile['cellphone']     = Select_user[0].user_cellphone
    profile['image']         = str(Select_user[0].user_image)


def recommend_preference(request,Session_profile):
    favourite = Session_profile['favouritegame'].split(';')




def recommend_popular(request):
    popular_list = Store.objects.filter(Rating__gte=3.6)
    pick = list(set([random.randint(0,len(popular_list)-1) for i in range(10)]))
    random.shuffle(pick)
    recommend_list = []
    for i in pick:
        recommend_list.append(popular_list[i].to_dict())
    return recommend_list


def recommend_store(request):
    Session_logname = request.session.get('logname',None)
    Session_profile = request.session.get('profile',None)

    if not Session_profile:
        Select_user = User.objects.filter(user_username=Session_logname)
        profile = {}
        get_profile_info(profile,Select_user)
        request.session['profile'] = profile
        Session_profile = request.session.get('profile',None)

    favourite = Session_profile['favouritegame']
    # if favourite == "" or favourite == None:
    recommend_list = recommend_popular(request)

    # else:
         # recommend_list = recommend_preference(request,Session_profile)
    return recommend_list
