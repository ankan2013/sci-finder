import bs4
import json
import re


def parse_scipub(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    d = {}

    title = page.findAll('h2')
    authors = []
    doi = ""
    if title:
        d["Title"] = title[0].text.replace("\n", "<br>")[len("<br>"):][:-len("<br>")]
        try:
            authors_tag = title[0].next_sibling.next_sibling
            lst = authors_tag.text.split(", ")
            for author in lst:
                authors.append(author)
            for sibling in authors_tag.next_siblings:
                if sibling == "\n":
                    continue
                elif sibling.text.find("DOI") != -1:
                    doi = sibling.text[len("DOI : "):]
        except AttributeError as AE:
            authors = ""
            doi = ""
            print(AE)
    if authors:
        d["Authors"] = authors
    if doi:
        d["DOI"] = doi

    abstract = ""
    try:
        for hdr in page.findAll('h3'):
            if hdr.text.find("Abstract") != -1:
                for sibling in hdr.next_siblings:
                    if sibling == "\n":
                        continue
                    elif len(sibling.text) > 20:
                        abstract = sibling.text.replace("\n", "<br>").replace("\"", "&quot")
                        break
    except AttributeError as AE:
        abstract = ""
        print("AE")

    if abstract:
        d["Abstract"] = abstract

    # Received may not present

    return json.dumps(d, ensure_ascii=False)
