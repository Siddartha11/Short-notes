from django.shortcuts import render
import markdown2 as md
from . import util
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import random



class Newform(forms.Form):
    task=forms.CharField(label="Search Encyclopedia")
class Newpage(forms.Form):
    title=forms.CharField(label="Title for the page")
    text=forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'custom-textarea'}))
class Editpage(forms.Form):
    title=forms.CharField(label="Title for the page")
    content=forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'custom-textarea'}))


def index(request):
    search_list=[]
    if request.method=="GET":
        form=Newform(request.GET)
        if form.is_valid():
            task=form.cleaned_data["task"]
            for i in util.list_entries():
                if task==i :
                    return entry(request,i)
                elif task in i :
                    search_list.append(i)
            if len(search_list)==0 :
                 return render(request,"encyclopedia/entry.html",{
            "title": "No File" ,
            "body": "No file found",
            "form":Newform()
                 })
            return render(request, "encyclopedia/index.html", {
        "entries": search_list,
        "form":Newform()
    })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":Newform()
    })

def entry(request,title):
    if util.get_entry(title) :
        return render(request,"encyclopedia/entry.html",{
            "title":title ,
            "body":md.markdown(util.get_entry(title)),
            "form":Newform()
        })
    else :
        return render(request,"encyclopedia/entry.html",{
            "title": "No File" ,
            "body": "No file found",
            "form":Newform()
        })

def newpage(request):
    if request.method=="POST":
        form=Newpage(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["text"]
            if title in util.list_entries() :
                return render(request,"encyclopedia/entry.html",{
                                    "title": "File already exixts" ,
                                    "body": "   File already exits",
                                    "form":Newform() })
            else :
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry",kwargs={'title': title}))
    return render(request, "encyclopedia/newpage.html", {
        "newform":Newpage()
    })

def edit_page(request,title):
    initial_value_t=title
    initial_value_c = util.get_entry(title)
    print(request.method)
    if request.method=="POST":
        print("hlo")
        form=Editpage(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry",kwargs={'title':title}))
    form = Editpage(initial={'content': initial_value_c,'title':initial_value_t})
    return render(request, "encyclopedia/editpage.html", {
        "editform":form,
        "title":title
    })

def randompage(request):
    a=util.list_entries()
    title=random.choice(a)
    return render(request,"encyclopedia/entry.html",{
            "title":title ,
            "body":md.markdown(util.get_entry(title)),
            "form":Newform()
        })





