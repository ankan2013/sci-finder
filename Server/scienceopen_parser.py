import bs4
import json


def parse_scienceopen(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}
    title = page.findAll('h1')
    if title:
        if len(title) > 1:
            d["Title"] = title[0].text

    authors = []
    i = 0
    for author in page.findAll('span', {'itemprop': 'author'}):
        i += 1
        authors.append(author.text)
    if authors:
        d["Authors"] = authors

    received = page.findAll('span', {'itemprop': 'datePublished'})
    if received:
        d["Received"] = received[0].text[1:][:-1]

    abstract = page.findAll('div', {'itemprop': 'description'})
    if abstract:
        d["Abstract"] = abstract[0].text.replace("\n", "<br>").replace("\"", "&quot")

    doi = ""
    for div in page.findAll('div'):
        if div.text.find("DOI") != -1:
            doi = div.text[len("DOI: "):].replace("\n", "")
    if doi:
        d["DOI"] = doi

    return json.dumps(d, ensure_ascii=False)

