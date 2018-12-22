import bs4


def parse(request_data):
    page = bs4.BeautifulSoup(request_data['code'], features="html.parser")
    page.prettify()
    url = request_data['url']
    outfile = open("loaded_page.txt", 'w+', encoding='utf-8')
    print(page, file=outfile)
    outfile.close()
    #if url.find("link.springer.com/article"):
