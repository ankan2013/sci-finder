import bs4
import json


def parse_ssrn(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h1')
    if title:
        d["Title"] = title[0].text

    authors = []
    for author in page.findAll('a'):
        if 'class' in author.attrs:
            if type(author['class']) != str or author['class'].find("lead-author-profile-link") == -1:
                continue
        if 'title' in author.attrs:
            if author['title'].find("author") != -1:
                authors.append(author.text)
    if authors:
        d["Authors"] = authors

    abstract = page.findAll('div', {'class': 'abstract-text'})

    if abstract:
        d["Abstract"] = abstract[0].text.replace("\n", "<br>").replace("\"", "&quot").replace("Abstract<br>", "")

    for tag in page.findAll("span"):
        if tag.text.find("Posted") != -1 and tag.parent.name == 'p' and 'class' in tag.parent.attrs and 'note-list' in tag.parent['class']:
            d["Received"] = tag.text[len("Posted :"):].replace("\n", "")

    return json.dumps(d, ensure_ascii=False)
