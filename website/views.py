from __future__ import unicode_literals
#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ingretools import settings
from .models import TableRow, TableHeader

import os
import uuid
import json

from lxml import etree
from bs4 import BeautifulSoup

import pdb
SEARCH_KEY = 'Ingrédients'
REQUIRED_FIELD = 'Effets'

def merge_arrary_without_duplicate(arr1, arr2):
    return arr1 + list(set(arr2) - set(arr1))

# Create your views here.
def home(request):
    files =os.listdir(settings.PROJECT_ROOT)
    return render(request, 'home.html')


# Create your views here.
def create_table(request):
    HEADERS = []

    files =os.listdir(settings.PROJECT_ROOT)
    html_files = []

    TableHeader.objects.all().delete()
    TableRow.objects.all().delete()

    # filter html files
    for a_file in files:
        if a_file[-5:] == '.html':
            html_files.append(a_file)

    initial_guid = uuid.uuid4()
    for filename in html_files:
        content = ''
        with open(os.path.join(settings.PROJECT_ROOT, filename)) as f:
            content = f.read()
        
        tree = etree.HTML(content)
        # extract title
        title = ''

        # extract th fields
        theads = tree.xpath("//table[@class='confluenceTable']//tbody//th//text()")
        tbodys = tree.xpath("//table[@class='confluenceTable']//tbody//tr//td[@class='confluenceTd']")

        HEADERS = merge_arrary_without_duplicate(HEADERS, theads)
        table_body = dict()
        has_ingredients = True if SEARCH_KEY in theads else False

        if not has_ingredients:
            title_text = tree.xpath("//title/text()")[0].split(':')
            if len(title_text) > 0:
                title = title_text[1].strip()

            for idx, th in enumerate(theads):
                td_str = etree.tostring(tbodys[idx]).decode('utf-8')
                table_body[theads[idx]] = td_str

            obj, created = TableRow.objects.get_or_create(title=title,
                                                        body=json.dumps(table_body),
                                                        guid=initial_guid)
            if created:
                print('Row: {} is created!'.format(title))

        else:
            trows = tree.xpath("//table[@class='confluenceTable']//tbody//tr")
            title = ''
            for row in trows:
                table_body = dict()
                tr_tbodys = row.xpath(".//td")
                if len(tr_tbodys) > 0:
                    
                    for idx, th in enumerate(theads):
                        td_xpath = ".//td[@class='confluenceTd'][{}]".format(idx)
                        if theads[idx] != SEARCH_KEY:
                            td_str = etree.tostring(row.xpath(td_xpath)[0]).decode('utf-8')
                            table_body[theads[idx]] = td_str
                        else:
                            try:
                                title = row.xpath(td_xpath)[0].xpath(".//text()")[0]
                            except:
                                title = title

                    if REQUIRED_FIELD in table_body.keys() and table_body[REQUIRED_FIELD] != "":
                        obj, created = TableRow.objects.get_or_create(title=title,
                                                                body=json.dumps(table_body),
                                                                guid=initial_guid)
                        if created:
                            print('Row: {} is created!'.format(title))
                    else:
                        print('Row: {} has no effects!'.format(title))

    TableHeader.objects.get_or_create(content=json.dumps(HEADERS))
    table_rows = TableRow.objects.all()
    return render(request, 'home.html', {'rows': table_rows})


@csrf_exempt
def download_table(request):
    if request.method == "GET":
        return render(request, 'table.html', {'error': 'Method Get not allowed!'})

    selected = json.loads(request.body)
    results = TableRow.objects.filter(id__in=selected)
    headers = TableHeader.objects.filter()
    header = None
    if len(headers) == 0:
        return render(request, 'home.html', {'error': 'Please analyze html files before downloa'})

    table_rows = []
    headers = json.loads(headers[0].content)
    headers.remove(SEARCH_KEY)
    for result in results:
        tmp_body = json.loads(result.body)
        tmp_rows = []
        for header in headers:
            if header in tmp_body.keys():
                tmp_rows.append(tmp_body[header])
            else:
                tmp_rows.append('<td class="confluenceTd"><p></p></td>')

        # pdb.set_trace()
        table_rows.append({
            'title': result.title,
            'body': tmp_rows
        })

    return render(request, 'table.html', {'rows': table_rows,
                                        'headers': headers,
                                        'created': results[0].created,
                                        'range': range(len(headers))})