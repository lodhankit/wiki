from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import markdown
import re

from . import util


def index(request):
    if (request.method == 'POST'):
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
            "entries": util.list_entries(),
        })


def details(request, title):
    filename = f"entries/{title}.md"
    if (default_storage.exists(filename)):
        content = util.get_entry(title)
        content_html = markdown.markdown(content)
        return render(request, 'encyclopedia/page.html', {
            "body_content": content_html
        })
    else:
        return render(request, 'encyclopedia/notfound.html')
