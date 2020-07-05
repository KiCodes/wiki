import random
from django.shortcuts import render
import markdown2
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from . import util

class Search(forms.Form):
    item = forms.CharField()

class CreatePost(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label='')

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='')
#creating search form

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item == i:
                    entry = f'/wiki/{item}'
                    return HttpResponseRedirect(entry)
                if item.lower() in i.lower():
                    searched.append(i)
            return render(request, "encyclopedia/search_result.html", {
            "form": Search(),
            "list": searched
            })
        else:
            return render(request, "encyclopedia/error.html", {
            "form": Search(),
            "message": "page not found"
            })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search()
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
        "page": convert_page, "title": name.capitalize(),
        "form": Search()
        })
    else:
        return render(request, "encyclopedia/error.html", {
        "message": "No page found",
        "form": Search()
        })

def create(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html",{
                "message": "post already exists", "form": Search()
                })
            else:
                util.save_entry(title, content)
                newPost = util.get_entry(title)
                convert_page = markdown2.markdown(newPost)
                return render(request, "encyclopedia/entry.html", {
                "form": Search(),
                "message": "success",
                "page": convert_page })
    else:
        return render(request, "encyclopedia/create.html", {
        "form": Search(),
        "create": CreatePost()
        })

def edit(request, name):
    if request.method == 'GET':
        page = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
        "form": Search(),
        "edit": EditForm(initial={'content':page})
        })
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            page = util.get_entry(name)
            convert_page = markdown2.markdown(page)
            return render(request, 'encyclopedia/entry.html', {
            "form": Search(),
            "title": name,
            "page": convert_page,
            "message": "success"
            })

def random_page(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) -1)
        random_p = entries[num]
        page = util.get_entry(random_p)
        convert_page = markdown2.markdown(page)
        return render(request, 'encyclopedia/entry.html', {
        "form":Search(),
        "title": random_p,
        "page": convert_page
        })
