from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from chartjs.views.lines import BaseLineChartView
from . import forms
from . import models

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
    model = models.PostModel
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
    # upon creation, stay on current page (which is main since PostModel redirects to main)
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
    # upon creation, stay on current page (which is main since PostModel redirects to main)
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
'''

class PitchDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'main'
    template_name = "view_pitch.html"
    model = models.PostModel

    def get(self, request, *args, **kwargs):
        currentFunds = request.user.catchermodel.funds
        purchased = False
        post = get_object_or_404(models.PostModel, id=self.kwargs['pk'])
        try:
            models.PurchaseModel.objects.get(purchasedPost = post, purchaser=request.user)
            purchased = True
        except models.PurchaseModel.DoesNotExist:
            pass
        if(currentFunds >= post.cost and purchased == False):
            models.PurchaseModel.objects.create(purchasedPost = post, purchaser=request.user)
            request.user.catchermodel.funds -= post.cost
            request.user.catchermodel.save()
            context = {
                'object': post
            }
            return render(request, "view_pitch.html", context = context)
        elif(purchased == True):
            context = {
                'object': post
            }
            return render(request, "view_pitch.html", context = context)
        else:
            return HttpResponseRedirect(reverse("main"))

'''
ListPitches inherits from ListView
    eventually this can replace parts of def index()
    see http://localhost/list/ for demo
'''
class PitchList(ListView):
    template_name = "pitches.html"
    model = models.PostModel

# Create your views here.
def index(request):
    title = "Gruvest"
    posts = models.PostModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getTotalVotes(), reverse=True)
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
    else:
        currentSubs = "Login"
    context = {
        "post":sortedPosts,
        "title":title,
        "subscription":currentSubs,

    }
    return render(request, "home.html", context = context)


# Creates view for upvoting
# This function is inspired by this stack overflow post: rb.gy/pb8u2y
@login_required(redirect_field_name='main')
def upVoteView(request, pk):
    is_liked = False
    is_disliked = False
    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
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
    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
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
    subcription = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
    try:
        models.SubscribeModel.objects.get(subscriber=request.user, pitcher=subcription.author)
        is_subscribed = True
    except models.SubscribeModel.DoesNotExist:
        pass
    if(is_subscribed == False):
        models.SubscribeModel.objects.create(subscriber=request.user, pitcher=subcription.author)
    else:
        sub = models.SubscribeModel.objects.get(subscriber=request.user, pitcher=subcription.author)
        sub.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

'''View Chart'''

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


lineChart = TemplateView.as_view(template_name='chartjs.html')
lineChartJSON = LineChartJSONView.as_view()