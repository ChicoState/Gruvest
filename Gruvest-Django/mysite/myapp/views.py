from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import forms
from . import models

import os
import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

# Class based views
'''
PitchCreator inherits from CreateView
    is the Create operation for Pitches in the CRUD model.
'''
class PitchCreator(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'main'
    # the associated html template
    template_name = "post_pitch.html"
    # specified model which this object creates
    model = models.UserModel
    # specified fields to be entered by user
    fields = [
        'header',
        'post',
        'cost'
    ]
    form = forms.PostPitchForm
    # upon creation, stay on current page (which is main since PostModel redirects to main)
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form_instance = self.form(request.POST)
        try:
            obj = models.UserModel.objects.get(author=request.user)
            if form_instance.is_valid():
                obj.post = form_instance.cleaned_data["post"]
                obj.header = form_instance.cleaned_data["header"]
                obj.cost = form_instance.cleaned_data["cost"]
                obj.save()
        except models.UserModel.DoesNotExist:
            if form_instance.is_valid():
                form_instance.save(request)
        return HttpResponseRedirect(reverse("main"))

    # error checking form
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form) # call parent object method
    
    def get_success_url(self):
        return '/'

class CommentCreator(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'main'
    # the associated html template
    template_name = "post_comment.html"
    # specified model which this object creates
    model = models.CommentModel
    # specified fields to be entered by user
    fields = [
        "comment"
    ]
    form = forms.PostCommentForm
    # upon creation, stay on current page (which is main since UserModel redirects to main)
    success_url = "/"
    def post(self, request, *args, **kwargs):
        form_instance = self.form(request.POST)
        if form_instance.is_valid():
            form_instance.post_id = self.kwargs['pk']
            form_instance.save(request, pk=form_instance.post_id)
        return HttpResponseRedirect(reverse("main"))
    # error checking form
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form) # call parent object method
    
    def get_success_url(self):
        return "/"

class AddFunds(UpdateView):
    # the associated html template
    template_name = "add_funds.html"
    # specified model which this object creates
    model = models.CatcherModel
    # specified fields to be entered by user
    fields = [
        'funds'
    ]
    form = forms.AddFundsForm
    # upon creation, stay on current page (which is main since UserModel redirects to main)
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            request.user.catchermodel.funds += int(form['funds'].value())
            request.user.catchermodel.save()
        return HttpResponseRedirect(reverse("main"))
    # error checking form
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form) # call parent object method
    
    def get_success_url(self):
        return '/'

'''
PitchDetail inherits from DetailView
    is a Retrieve operation
PitchDetail is now UserDetail
'''
class UserDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'main'
    template_name = "view_pitch.html"
    model = models.UserModel

    # display tracked stocks
    # how do I get the stocks with foreign key of the pitcher the user is viewing?

    # display pitcher rankings
    # function to get stocks in JSON, insert into TrackedStocksModel
    #   calculate portfolio performance
    #   calculate comparison to S&P500
    #   calculate comparison to Gruvest
    #   calculate user feedback

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.UserModel, id=self.kwargs['pk'])
        is_subscribed = False

        try:
            models.SubscribeModel.objects.get(subscriber=request.user, pitcher=post.author)
            is_subscribed = True
        except models.SubscribeModel.DoesNotExist:
            pass

        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'myapp/CSV/SPY.csv'))

        SUMpoints = data['4. close'].to_numpy()

        SUMdeltas = np.full(100, SUMpoints[-1])
        SUMdeltas = 100*SUMpoints/SUMdeltas-100


        SUMlabels = list(reversed([*range(len(SUMpoints))]))
        SUMdeltas = list(reversed(SUMdeltas.tolist()))

        context = {
            'object': post,
            'SUMlabels': SUMlabels,
            'SUMdeltas': SUMdeltas
        }

        if(is_subscribed or post.author == request.user):
            return render(request, "view_pitch.html", context = context)
        else:
            return render(request, "view_pitch_NS.html", context = context)


class StockAdder(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'main'
    # the associated html template
    template_name = "add_stock.html"
    # specified model which this object creates
    model = models.StocksModel
    # specified fields to be entered by user
    fields = [
        'ticker',
    ]
    form = forms.StocksForm
    # upon creation, stay on current page (which is main since PostModel redirects to main)
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form_instance = self.form(request.POST)
        #try:
           #models.StocksModel.objects.get(pitcher=request.user, ticker=str(form_instance['ticker'].value()))   
        #except models.StocksModel.DoesNotExist:
        if form_instance.is_valid():
            form_instance.save(request)
        return HttpResponseRedirect(reverse("main"))

    # error checking form
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form) # call parent object method

    def get_success_url(self):
        return '/'


'''
class TrackedStockUpdateView(UpdateView):
    #pitcher = models.UserModel
    model = models.TrackedStocksModel
    #queryset = model.objects.all(id=pk) # get all stocks tracked by the pitcher
    fields = [
        'percentages'
    ]
    form = forms.UpdateStocksForm
    template_name = 'view_pitch.html'

    def post(self, request, *args, **kwargs):
        queryset = model.objects.all(id=self.kwargs['pk']) # get all tracked stocks by the pitcher
        for stock in queryset:
            # update price
'''


'''
ListPitches inherits from ListView
    eventually this can replace parts of def index()
    see http://localhost/list/ for demo
'''
class PitchList(ListView):
    template_name = "pitches.html"
    model = models.UserModel

# Create your views here.
def index(request):
    title = "Gruvest"
    posts = models.UserModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getTotalVotes(), reverse=True)
    data = pd.read_csv(os.path.join(settings.BASE_DIR, 'myapp/CSV/SPY.csv'))

    SPYpoints = data['4. close'].to_numpy()

    SPYdeltas = np.full(100, SPYpoints[-1])
    SPYdeltas = 100*SPYpoints/SPYdeltas-100

    SPYlabels = list(reversed([*range(len(SPYpoints))]))

    SPYdeltas = list(reversed(SPYdeltas.tolist()))
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
    else:
        currentSubs = "Login"
    context = {
        "sort":"Popularity",
        "post":sortedPosts,
        "title":title,
        "subscription":currentSubs,
        "SPYlabels":SPYlabels,
        "SPYdeltas":SPYdeltas
    }
    return render(request, "home.html", context = context)

def sortedCost(request):
    title = "Gruvest"
    posts = models.UserModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getCost(), reverse=True)
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
    else:
        currentSubs = "Login"
    context = {
        "sort": "Cost",
        "post":sortedPosts,
        "title":title,
        "subscription":currentSubs,
    }
    return render(request, 'home.html', context=context)

def sortedDate(request):
    title = "Gruvest"
    posts = models.UserModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getDate(), reverse=True)
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
    else:
        currentSubs = "Login"
    context = {
        "sort": "Date",
        "post":sortedPosts,
        "title":title,
        "subscription":currentSubs,
    }
    return render(request, 'home.html', context=context)

def main(request):
    title="Gruvest"
    posts=models.UserModel.objects.all()

    #Get SPY points
    #apiKey = 'VLG4S2J38MECAW2U'


    #ts = TimeSeries(key="apiKey", output_format='pandas')
    #data, meta_data = ts.get_daily(symbol='SPY', outputsize='compact')

    data = pd.read_csv(os.path.join(settings.BASE_DIR, 'myapp/CSV/SPY.csv'))

    SPYpoints = data['4. close'].to_numpy()

    SPYdeltas = np.full(100, SPYpoints[-1])
    SPYdeltas = 100*SPYpoints/SPYdeltas-100

    SPYlabels = list(reversed([*range(len(SPYpoints))]))

    SPYdeltas = list(reversed(SPYdeltas.tolist()))
    #for i in range(len(SPYpoints)-1):
    #    SPYdeltas.append( (100*SPYpoints[i]/SPYpoints[0]) - 100)

    if(request.user.is_authenticated):
        subscriptions=models.SubscribeModel.objects.all()
        currentSubs=subscriptions.filter(subscriber=request.user)
    else:
        currentSubs="Login"
    context = {
        "user":request.user,
        "posts":posts,
        "title":title,
        "subs":currentSubs,
		"SPYlabels":SPYlabels,
        "SPYdeltas":SPYdeltas
    }
    return render(request, "gruvest-main.html", context=context)

# Creates view for upvoting
# This function is inspired by this stack overflow post: rb.gy/pb8u2y
@login_required(redirect_field_name='main')
def upVoteView(request, pk):
    is_liked = False
    is_disliked = False
    post = get_object_or_404(models.UserModel, id=request.POST.get('post_id'))
    try:
        models.UpvoteModel.objects.get(upvotedPost = post, upvoter=request.user)
        is_liked = True
    except models.UpvoteModel.DoesNotExist:
        pass
    try:
        models.DownvoteModel.objects.get(downvotedPost = post, downvoter=request.user)
        is_disliked = True
    except models.DownvoteModel.DoesNotExist:
        pass
    if(is_liked == False and is_disliked == False):
        models.UpvoteModel.objects.create(upvoter=request.user, upvotedPost=post)
        post.upVotes = post.upVotes + int(1)
        post.save()
    elif(is_liked == False and is_disliked == True):
        models.UpvoteModel.objects.create(upvoter=request.user, upvotedPost=post)
        dislike = models.DownvoteModel.objects.get(downvoter=request.user, downvotedPost=post)
        dislike.delete()
        post.upVotes = post.upVotes + int(1)
        post.downVotes = post.downVotes - int(1)
        post.save()
    else:
        like = models.UpvoteModel.objects.get(upvoter=request.user, upvotedPost=post)
        like.delete()
        post.upVotes = post.upVotes - int(1)
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Creates view for downvoting
@login_required(redirect_field_name='main')
def downVoteView(request, pk):
    is_liked = False
    is_disliked = False
    post = get_object_or_404(models.UserModel, id=request.POST.get('post_id'))
    try:
        models.UpvoteModel.objects.get(upvotedPost = post, upvoter=request.user)
        is_liked = True
    except models.UpvoteModel.DoesNotExist:
        pass
    try:
        models.DownvoteModel.objects.get(downvotedPost = post, downvoter=request.user)
        is_disliked = True
    except models.DownvoteModel.DoesNotExist:
        pass
    if(is_liked == False and is_disliked == False):
        models.DownvoteModel.objects.create(downvoter=request.user, downvotedPost=post)
        post.downVotes = post.downVotes + int(1)
        post.save()
    elif(is_disliked == False and is_liked == True):
        models.DownvoteModel.objects.create(downvoter=request.user, downvotedPost=post)
        like = models.UpvoteModel.objects.get(upvoter=request.user, upvotedPost=post)
        like.delete()
        post.downVotes = post.downVotes + int(1)
        post.upVotes = post.upVotes - int(1)
        post.save()
    else:
        dislike = models.DownvoteModel.objects.get(downvoter=request.user, downvotedPost=post)
        dislike.delete()
        post.downVotes = post.downVotes - int(1)
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

@login_required(redirect_field_name='main')
def subscribeView(request, pk):
    is_subscribed = False
    currentFunds = request.user.catchermodel.funds
    subcription = get_object_or_404(models.UserModel, id=request.POST.get('post_id'))
    if(request.user == subcription.author):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        models.SubscribeModel.objects.get(subscriber=request.user, pitcher=subcription.author)
        is_subscribed = True
    except models.SubscribeModel.DoesNotExist:
        pass
    if(is_subscribed == False and currentFunds >= subcription.cost):
        models.SubscribeModel.objects.create(subscriber=request.user, pitcher=subcription.author)
        request.user.catchermodel.funds -= subcription.cost
        request.user.catchermodel.save()
        subcription.author.catchermodel.funds += subcription.cost
        subcription.author.catchermodel.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
