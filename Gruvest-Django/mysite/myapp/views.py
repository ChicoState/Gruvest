from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms
from . import models


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
    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
    post.upVotes = post.upVotes + int(1)
    post.save()
    return HttpResponseRedirect(reverse("main"))

# Creates view for downvoting
def downVoteView(request, pk):
    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
    post.downVotes = post.downVotes + int(1)
    post.save()
    return HttpResponseRedirect(reverse("main"))

#def addComment(request, pk):
#    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
    
    