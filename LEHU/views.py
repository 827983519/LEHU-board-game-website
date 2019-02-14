from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Activity

# def index(request):
#     return HttpResponse('hello')

class IndexView(generic.ListView):
    template_name = 'LEHU/index.html'

class ActivityPostView(generic.CreateView):
    model = Activity
    template_name = 'LEHU/ActivityPost.html'
    fields = ['activity_title', 'activity_content', 'owner', 'numberofmem', 'budget', 'start_time', 'duration', 'location']

    def form_valid(self, form):
        self.object = form.save()
    # do something with self.object
    # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/post/list')

class PostListView(generic.ListView):
    model = Activity
    template_name = 'LEHU/PostList.html'
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