from flask import Flask, request
from springer_parser import parse_springer
from arxiv_parser import parse_arxiv
from omicsonline_parser import parse_omicsonline
from page_saver import save
from scipub_parser import parse_scipub
from scienceopen_parser import parse_scienceopen
from citeseerx_parser import parse_citeseerx
from microsoft_parser import parse_microsoft
from ssrn_parser import parse_ssrn
from osti_parser import parse_osti
from ncbi_parser import parse_ncbi
app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive():
    if request.method == 'POST':
        if request.form['url'].find("link.springer.com/article") != -1:
            return parse_springer(request.form['code'])
        elif request.form['url'].find("arxiv.org/abs") != -1:
            return parse_arxiv(request.form['code'])
        elif request.form['url'].find("omicsonline.org/open-access/") != -1:
            save(request.form['code'])
            return parse_omicsonline(request.form['code'])
        elif request.form['url'].find("thescipub.com/abstract/") != -1:
            return parse_scipub(request.form['code'])
        elif request.form['url'].find("scienceopen.com/document") != -1:
            return parse_scienceopen(request.form['code'])
        elif request.form['url'].find("citeseerx.ist.psu.edu/viewdoc/") != -1:
            return parse_citeseerx(request.form['code'], request.form['url'])
        elif request.form['url'].find("academic.microsoft.com/paper") != -1:
            return parse_microsoft(request.form['code'])
        elif request.form['url'].find("papers.ssrn.com/sol3/") != -1:
            return parse_ssrn(request.form['code'])
        elif request.form['url'].find("osti.gov/biblio") != -1:
            return parse_osti(request.form['code'])
        elif request.form['url'].find("ncbi.nlm.nih.gov") != -1:
            return parse_ncbi(request.form['code'])
        else:
            return "Server : Not a valid page received"


if __name__ == '__main__':
    app.run()
