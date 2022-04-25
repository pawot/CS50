import random
import markdown2
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title in util.list_entries():
        markdownConvert = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "entry": markdownConvert,
            "title": title
        })
    
    else:
        return render(request, "encyclopedia/notexist.html")

def search(request):
    query = request.GET["q"]

    queryList = [query, query.capitalize(), query.upper(), query.lower()]
    print(queryList)
    for item in queryList:
        if item in util.list_entries():
            return HttpResponseRedirect(reverse("entry", args=(item,)))

    entriesList = []
    for item in util.list_entries():
        for queryItem in queryList:
            if queryItem in item:
                entriesList.append(item)
                break
    if entriesList:
        return render(request, "encyclopedia/result.html", {
                "entries": entriesList
            })
    
    return render(request, "encyclopedia/notexist.html")

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-title"}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control form-content"}), label="New entry")

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

        titleList = [title, title.capitalize(), title.upper(), title.lower()]

        for item in titleList:
            if item in util.list_entries():
                return render(request, "encyclopedia/already-exist.html")
        
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("entry", args=(title,)))

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    class EditEntryForm(forms.Form):
        formTitle = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-title"}), label="Title", initial=title, disabled=True)
        content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-content"}), label="Edit entry", initial=util.get_entry(title))

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["formTitle"]
            content = form.cleaned_data["content"]
        
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("entry", args=(title,)))

    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(),
        "title": title
    })

def randomEntry(title):
    title = random.choice(util.list_entries())

    return HttpResponseRedirect(reverse("entry", args=(title,)))

