import bs4
import json


def parse_ncbi(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title_tag = None
    for h1 in page.findAll('h1'):
        if h1.parent.name == 'div' and 'class' in h1.parent.attrs and 'abstract' in h1.parent['class']:
            d["Title"] = h1.text
            title_tag = h1

    authors = []
    authors_tag = None
    for sibling in title_tag.next_siblings:
        if type(sibling) != bs4.Tag:
            continue
        else:
            authors_tag = sibling
            break
    for a in authors_tag.findAll('a'):
        authors.append(a.text)
    if authors:
        d["Authors"] = authors

    title = page.findAll('div', {'class': 'abstr'})
    if title:
        d["Abstract"] = title[0].text.replace("Abstract", "").replace("\n", "<br>").replace("\"", "&quot")

    for a in page.findAll('a'):
        if 'href' in a.attrs:
            if a['href'].find("doi.org/") != -1:
                d["DOI"] = a['href'].split("doi.org/")[1]

    span = page.find('span', {'role': 'menubar'})
    if span:
        if span.next_sibling:
            s = span.next_sibling
            if type(s) != bs4.Tag:
                d["Received"] = s.split(";")[0]

    return json.dumps(d, ensure_ascii=False)
