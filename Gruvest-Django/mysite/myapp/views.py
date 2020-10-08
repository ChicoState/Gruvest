from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from . import forms
from . import models

# Class based views
'''
PitchCreator inherits from CreateView
    is the Create operation for Pitches in the CRUD model.
'''
class PitchCreator(CreateView):
     # the associated html template
    template_name = "post_pitch.html"
    # specified model which this object creates
    model = models.PostModel
    # specified fields to be entered by user
    fields = [
        'header',
        'post'
    ]
    form = forms.PostPitchForm
    # upon creation, stay on current page (which is main since PostModel redirects to main)
    success_url = '/'

    # error checking form
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form) # call parent object method
    
    def get_success_url(self):
        return '/'


# Create your views here.
def index(request):
    if request.method == "POST":
        post_form = forms.postForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            post_form = forms.postForm()

    else:
        post_form = forms.postForm()
        title = "Gruvest"
        posts = models.PostModel.objects.all()
        context = {
            "post":posts,
            "title":title,
            "form":post_form,
        }
        return render(request, "base.html", context = context)

# Creates view for upvoting
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
    return HttpResponseRedirect(reverse("main"))

# Creates view for downvoting
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
    return HttpResponseRedirect(reverse("main"))

#def addComment(request, pk):
#    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))