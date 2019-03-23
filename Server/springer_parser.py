import bs4
import json


def parse_springer(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h1', {'class': 'ArticleTitle'})
    if title:
        d["Title"] = title[0].text

    authors = []
    i = 0
    for author in page.findAll('span', {'class': 'authors__name'}):
        i += 1
        authors.append(author.text)
    if i > 0:
        authors[i - 1] = authors[i - 1][:-2]  # deleted unwanted comma
    if authors:
        d["Authors"] = authors

    abstract = page.findAll('section', {'class': 'Abstract'})
    if abstract:
        d["Abstract"] = abstract[0].text[len("Abstract"):].replace("\n", "<br>").replace("\"", "&quot")

    for info in page.findAll('li', {'class': 'bibliographic-information__item'}):
        name = info.findAll('span', {'class': 'bibliographic-information__title'})
        if name:
            if name[0].text == 'Received' or name[0].text == 'DOI':
                value = info.findAll('span', {'class': 'bibliographic-information__value u-overflow-wrap'})
                d[name[0].text] = value[0].text

    return json.dumps(d, ensure_ascii=False)


