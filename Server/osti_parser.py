import bs4
import json


def parse_osti(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h1')
    if title:
        d["Title"] = title[0].text.replace("Title: ", "")

    authors = []
    for author in page.findAll('span', {'class': 'author'}):
        authors.append(author.text.replace(",", ""))
    if authors:
        d["Authors"] = authors

    received = page.findAll('time', {'itemprop': 'datePublished'})
    if received:
        d["Received"] = received[0].text

    for a in page.findAll('a'):
        if 'href' in a.attrs:
            if a['href'].find("doi.org/") != -1:
                d["DOI"] = a['href'].split("doi.org/")[1]

    abstract = ""
    try:
        for tag in page.findAll():
            if tag.text.find("Abstract") != -1:
                for sibling in tag.next_siblings:
                    if type(sibling) != bs4.Tag:
                        continue
                    elif len(sibling.text) > 20:
                        abstract = sibling.text.replace("\n", "<br>").replace("\"", "&quot").replace(chr(171), "").replace("less", "")

                        break
    except AttributeError as AE:
        abstract = ""
        print("AE")

    if abstract:
        d["Abstract"] = abstract

    return json.dumps(d, ensure_ascii=False)
