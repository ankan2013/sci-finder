import bs4
import json


def parse_microsoft(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('div', {'class': 'name'})
    if title:
        d["Title"] = title[0].text

    received = page.findAll('span', {'class': 'year'})
    if received:
        d["Received"] = received[0].text.replace(" ", "")

    authors = []
    authors_class = page.findAll('ma-author-string-collection', {'items.bind': 'info.entity.authors'})
    for author in authors_class[0].findAll('a', {'aria-label': 'Author name'}):
        authors.append(author.text)
    if authors:
        d["Authors"] = authors

    abstract = ""
    try:
        if authors_class:
            for sibling in authors_class[0].next_siblings:
                if type(sibling) != bs4.Tag:
                    continue
                    # Further may replace all similar cases to "if != bs4.Tag
                elif len(sibling.text) > 20:
                    abstract = sibling.text.replace("\n", "<br>").replace("\"", "&quot")
                    break
    except AttributeError as AE:
        abstract = ""
        print("AE")

    if abstract:
        d["Abstract"] = abstract

    return json.dumps(d, ensure_ascii=False)
