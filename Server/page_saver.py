import bs4


def save(data):
    page = bs4.BeautifulSoup(data, features="html.parser")
    page.prettify()
    outfile = open("loaded_page.txt", 'w+', encoding='utf-8')
    print(page, file=outfile)
    outfile.close()
