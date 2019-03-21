import bs4
import json


def parse_arxiv(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h1', {'class': 'title mathjax'})
    if title:
        d['Title'] = title[0].text[len("Title:"):]

    authors_temp = []
    authors = page.findAll('div', {'class': 'authors'})
    i = 0
    if authors:
        for author in authors[0].findAll('a'):
            i += 1
            authors_temp.append((author.text + ", "))
        authors_temp[i-1] = authors_temp[i-1][:-2]  # deleted unwanted comma
    if authors:
        d["Authors"] = authors_temp

    abstract = page.findAll('blockquote', {'class': 'abstract mathjax'})
    if abstract:
        d["Abstract"] = abstract[0].text[len("Abstract:"):].replace("\n", "<br>").replace("\"", "&quot")

    received = page.findAll('div', {'class': 'dateline'})
    if received:
        d["Received"] = received[0].text[len("Submitted on "):-1]

    """arxivid = page.findAll('td', {'class': 'tablecell arxivid'})
    if arxivid:
        d["Arxiv_ID"] = arxivid[0].text"""

    # doi may present or not on an article page

    return json.dumps(d, ensure_ascii=False)

