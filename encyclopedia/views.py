from django.shortcuts import render
import markdown2
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from . import util

#creating search form

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    #calling list of entries
    entries = util.list_entries()
    #also the entry funtion passing in the name of the md file
    page = util.get_entry(name)
    #if name in entries then convert the md using markdown
    if name in entries:
        convert_page = markdown2.markdown(page)
        return render(request, "encyclopedia/entry.html", {
        "page": convert_page, "title": name.capitalize()
        })
    else:
        return render(request, "encyclopedia/error.html", {
        "message": "No page found"
        })

def search(request):
    searched = request.POST.get('q',"")
    check_entry = util.get_entry(searched)
    list_names = util.list_entries()
    result = []

    if check_entry:
        return redirect(f"/wiki/{searched}")
