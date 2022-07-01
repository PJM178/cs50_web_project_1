from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.db.models import Q
import operator
from django import forms
import random

from . import util

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

def index_to_wiki(request):
    return HttpResponseRedirect("/wiki/")

def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries(),
    })

def wiki(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })

def title(request, name):
    testi = util.get_entry(name)
    request.session["teksti"] = testi
    request.session["nimi"] = name
    if testi == None:
        return render(request, "encyclopedia/error.html", {
            "name": name,
        })
    return render(request, "encyclopedia/title.html", {
        "title": util.get_entry(name),
        "name": name
    })

def search(request):
    query = request.GET.get("q")
    lista = util.list_entries()
    results = []
    for i in lista:
        if str.lower(i).find(str.lower(query)) != -1:
            results.append(i)
    if not results:
        return render(request, "encyclopedia/error.html",{
            "name": query
        })
    else:
        return render(request, "encyclopedia/search_results.html",{
            "query": results
        })

def new_page(request):
    if request.method == "POST":
        text = request.POST
        if util.get_entry(text["title"]) == None:
            util.save_entry(text["title"], text["text"])
            return HttpResponseRedirect("/wiki/"+text["title"])
        else:
            return render(request, "encyclopedia/new_page_error.html",{
                "text": text["title"]
            })
    else:
        return render(request, "encyclopedia/new_page.html")

def random_page(request):
    lista = util.list_entries()
    random_page = random.choice(lista)
    return HttpResponseRedirect("/wiki/"+random_page)

def edit_page(request):
    return render(request, "encyclopedia/edit_page.html",{
        "text": request.session["teksti"]
    })

def edit_commit(request):
    text = request.POST
    util.save_entry(request.session["nimi"],  text["text"])
    return HttpResponseRedirect("/wiki/"+request.session["nimi"])