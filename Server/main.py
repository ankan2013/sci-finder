from flask import Flask, request
from springer_parser import parse_springer
from arxiv_parser import parse_arxiv
app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive():
    if request.method == 'POST':
        if request.form['url'].find("link.springer.com/article") != -1:
            return parse_springer(request.form['code'])
        elif request.form['url'].find("arxiv.org/abs") != -1:
            return parse_arxiv(request.form['code'])
        else:
            return "Server : Not a valid page received"


if __name__ == '__main__':
    app.run()
