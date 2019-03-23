import bs4
import json
import re


def parse_citeseerx(data, url=None):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h2')
    if title:
        d["Title"] = title[0].text[:-len(" (2000)")]
        date_field = title[0].text[len(title[0])-len(" (2000)"):][:-2]
        i = 0
        for ch in date_field:
            i += 1
            if ord(ch) - ord("0") < 0 or ord(ch) - ord("0") > 9:
                break
        if i == 4:
            d["Received"] = date_field

    authors_class = page.findAll('div', {'id': 'docAuthors'})
    if authors_class:
        authors = authors_class[0].text.replace("\n", "").replace(" by ", "").split(" , ")
        d["Authors"] = authors

    abstract = ""
    try:
        for tag in page.findAll():
            if tag.text.find("Abstract") != -1:
                for sibling in tag.next_siblings:
                    if type(sibling) != bs4.Tag:
                        continue
                    elif len(sibling.text) > 20:
                        abstract = sibling.text.replace("\n", "<br>").replace("\"", "&quot")
                        break
    except AttributeError as AE:
        abstract = ""
        print("AE")

    if abstract:
        d["Abstract"] = abstract

    if url:
        doi = re.search('doi=(.+?)&', url)
        if doi:
            d["DOI"] = doi.group(1)

    return json.dumps(d, ensure_ascii=False)
