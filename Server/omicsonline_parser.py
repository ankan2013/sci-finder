import bs4
import json
import re


def parse_omicsonline(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}
    title = page.findAll('h1')
    if title:
        if len(title) > 1:
            d["Title"] = title[1].text
        # Not title[0](!), there are SOME h1 units on this page
        # probably need ML to recognize which h1 is suitable

    authors = []
    i = 0
    authors_class = page.findAll('dl', {'class': 'authors'})
    if authors_class:
        for author in authors_class[0].findAll('a'):
            if author.get("title"):
                authors.append(author.get("title"))
                i += 1
        if i > 0:
            authors[i - 1] = authors[i - 1][:-2]  # deleted unwanted comma
    if authors:
        d["Authors"] = authors

    abstract = ""
    for div in page.findAll('div'):
        if div.text.find("Abstract") != -1:
            abstract = div.text
    if abstract:
        d["Abstract"] = abstract.replace("\n", "<br>").replace("\"", "&quot")[len("Abstract:")+11:].split("Keywords")[0][:-5]
        # Further a function which automatically deletes all spaces and separators such as <br> may be implemented
        # the idea of counting number of symbols is probably OK
        # now use string formatting specific for each parser

    doi = ""
    for li in page.findAll('li'):
        if li.text.find("DOI") != -1:
            doi = li.text[len("DOI: "):]
    if doi:
        d["DOI"] = doi

    received = ""
    for em in page.findAll('em'):
        if em.text.find("Received Date") != -1:
            received_tmp = re.search('Received Date: (.+?) /', em.text)
            if received_tmp:
                found = received_tmp
                received = found[0][len("Received Date: "):].replace(" /", "")
    if received:
        d["Received"] = received

    return json.dumps(d, ensure_ascii=False)
