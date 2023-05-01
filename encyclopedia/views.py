from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import markdown
import re
import random

from . import util

new_list = util.list_entries()
new_set = set(new_list)
def index(request):
    name_list = list(request.POST.keys())
    if (request.method == 'POST' and name_list[-1] == 'q'):
        title = request.POST.get('q')
        link = f"/{title}"
        filename = f"entries/{title}.md"
        highest_match = []
        pattern = rf"{title}"
        for name in util.list_entries():
            if(re.findall(pattern,name,re.IGNORECASE)):
                highest_match.append(name)
        if(default_storage.exists(filename)):
            return HttpResponseRedirect(link)
        else:
            return render(request, 'encyclopedia/index.html', {
            "entries": highest_match
        })
    elif(request.method == 'GET'):
        return render(request, 'encyclopedia/index.html', {
            "entries": new_list,
        })
    else:
        title = request.POST.get(name_list[1])
        content = request.POST.get(name_list[2])
        if(title != '' and content != ''):
            util.save_entry(title,content)
            link = f'\{title}'
            if(title not in new_set):
                new_list.append(title)
                new_set.add(title)
            return HttpResponseRedirect(link)
        else:
            return HttpResponseRedirect('/')

def details(request, title):
    filename = f"entries/{title}.md"
    if(request.method == 'GET'):
        if (default_storage.exists(filename)):
            content = util.get_entry(title)
            content_html = markdown.markdown(content)
            return render(request, 'encyclopedia/page.html', {
                "body_content": content_html,
                "body_md":content,
                "title":title
            })
        else:
            return render(request, 'encyclopedia/notfound.html')

def create(request):

    if(request.method == 'POST'):
        content = request.POST.get('edit')
        title = request.POST.get('tl')
        return render(request, 'encyclopedia/add.html',{
            "content":content,
            "title":title
    })

    else:
        return render(request, 'encyclopedia/add.html')

def enter(request):
    title_entries = util.list_entries()
    random.shuffle(title_entries)
    title = title_entries[0]
    link = f"/{title}"
    return HttpResponseRedirect(link)