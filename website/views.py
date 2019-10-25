from __future__ import unicode_literals
#-*- coding: utf-8 -*-
from django.shortcuts import render
from ingretools import settings

import os
import uuid

from lxml import etree
from bs4 import BeautifulSoup

import pdb

# Create your views here.
def home(request):
    files =os.listdir(settings.PROJECT_ROOT)
    html_files = []
    search_key = 'Ingrédients'

    # filter html files
    for a_file in files:
        if a_file[-5:] == '.html':
            html_files.append(a_file)

    for filename in html_files:
        content = ''
        with open(os.path.join(settings.PROJECT_ROOT, filename)) as f:
            content = f.read()
        
        tree = etree.HTML(content)
        # extract title
        title = ''

        # extract th fields
        theads = tree.xpath("//th//text()")
        tbodys = tree.xpath("//tr//td")

        table_body = dict()
        has_ingredients = True if search_key in theads else False
        if not has_ingredients:
            title_text = tree.xpath("//title/text()")[0].split(':')
            if len(title_text) > 0:
                title = title_text[1].strip()

            for idx, th in enumerate(theads):
                td_str = etree.tostring(tbodys[idx])
                table_body[theads[idx]] = td_str
        else:
            trows = tree.xpath("//tr")
            for row in trows:
                tr_tbodys = row.xpath(".//td")
                for idx, th in enumerate(theads):
                    if theads[idx] != search_key:
                        td_str = etree.tostring(tr_tbodys[idx])
                        table_body[theads[idx]] = td_str
                    else:
                        title = theads[idx]

    return render(request, 'home.html', {'files': html_files})