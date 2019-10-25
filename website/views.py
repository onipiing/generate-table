from __future__ import unicode_literals
#-*- coding: utf-8 -*-
from django.shortcuts import render
from ingretools import settings
from .models import TableRow

import os
import uuid
import json

from lxml import etree
from bs4 import BeautifulSoup

import pdb

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
    search_key = 'Ingrédients'
    required_field = 'Effets'

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
        has_ingredients = True if search_key in theads else False

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
                        if theads[idx] != search_key:
                            td_str = etree.tostring(row.xpath(td_xpath)[0]).decode('utf-8')
                            table_body[theads[idx]] = td_str
                        else:
                            try:
                                title = row.xpath(td_xpath)[0].xpath(".//text()")[0]
                            except:
                                title = title

                    if required_field in table_body.keys() and table_body[required_field] != "":
                        obj, created = TableRow.objects.get_or_create(title=title,
                                                                body=json.dumps(table_body),
                                                                guid=initial_guid)
                        if created:
                            print('Row: {} is created!'.format(title))
                    else:
                        print('Row: {} has no effects!'.format(title))

    results = TableRow.objects.filter(guid=initial_guid)
    table_rows = []
    HEADERS.remove(search_key)
    for result in results:
        tmp_body = json.loads(result.body)
        tmp_rows = []
        for header in HEADERS:
            if header in tmp_body.keys():
                tmp_rows.append(tmp_body[header])
            else:
                tmp_rows.append('<td class="confluenceTd"><p></p></td>')

        print(len(tmp_rows), "\n")
        print(len(HEADERS))
        # pdb.set_trace()
        table_rows.append({
            'title': result.title,
            'body': tmp_rows
        })

    return render(request, 'table.html', {'rows': table_rows,
                                        'headers': HEADERS,
                                        'created': results[0].created,
                                        'range': range(len(HEADERS))})