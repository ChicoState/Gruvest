from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def index(request):
    title = "Brandon's Website"
    body = "whats up"
    context = {
        "title":title,
        "body":body,
    }
    return render(request, "base.html", context = context)

