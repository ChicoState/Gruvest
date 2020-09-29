from django.shortcuts import render
from django.http import HttpResponse
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

