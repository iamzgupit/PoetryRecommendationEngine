from flask import (Flask, render_template, redirect, jsonify,
                   request, session)
from random import choice
from Model import Poem, connect_to_db, db
from requests import get
from bs4 import BeautifulSoup


app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


@app.route('/')
def homepage():
    """displays homepage with search bar"""

    return render_template("homepage.html")


@app.route('/search.json')
def get_search_criteria():
    """returns a list of dictionaries w/title, author, poem_id """
    search_critera = Poem.create_search_params()

    return jsonify(search_critera)


@app.route('/random')
def get_random_poem():
    """redirects to the search page for a random poem"""
    poem_ids = db.session.query(Poem.poem_id).all()
    chosen_id = choice(poem_ids)
    poem = str(chosen_id[0])
    url = "/" + poem

    return redirect(url)


@app.route('/<int:poem_id>')
def display_search_results(poem_id):
    main_poem = Poem.query.get(poem_id)
    name = main_poem.poet.name.replace(" ", "_")
    wikipedia_url = "https://en.wikipedia.org/wiki/" + name
    page = get(wikipedia_url).text
    if "does not have an article with this exact name" in page:
        wikipedia_url = None
        source = None
    else:
        soup = BeautifulSoup(page, "html5lib")
        info_box = soup.find("table", class_="infobox vcard")
        image = info_box.find("img")
        if image:
            attrib = image.attrs
            source = attrib['src']
            source = "https:" + source
        else:
            source = '/static/parchment.jpg'

    match_poems = Poem.query.all()[0:5]
    mp1, mp2, mp3, mp4, mp5 = match_poems

    return render_template("searchresults.html", main_poem=main_poem,
                           wikipedia_url=wikipedia_url, source=source, mp1=mp1,
                           mp2=mp2, mp3=mp3, mp4=mp4, mp5=mp5)


@app.route('/<int:poem_id>/<int:index>')
def display_search_results(poem_id, index):
    main_poem = Poem.query.get(poem_id)
    match_poems = Poem.query.all()[0:5]

    match_poem = match_poems[index]
    match_poems[index] = None
    mp1, mp2, mp3, mp4, mp5 = match_poems

    name = match_poem.poet.name.replace(" ", "_")
    wikipedia_url = "https://en.wikipedia.org/wiki/" + name
    page = get(wikipedia_url).text
    if "does not have an article with this exact name" in page:
        wikipedia_url = None
        source = None
    else:
        soup = BeautifulSoup(page, "html5lib")
        info_box = soup.find("table", class_="infobox vcard")
        image = info_box.find("img")
        if image:
            attrib = image.attrs
            source = attrib['src']
            source = "https:" + source
        else:
            source = '/static/parchment.jpg'


    return render_template("displaymatches.html", main_poem=main_poem,
                           match_poem=match_poem, wikipedia_url=wikipedia_url,
                           source=source, mp1=mp1, mp2=mp2, mp3=mp3, mp4=mp4, mp5=mp5)


@app.route('/about')
def display_about():
    return render_template("about.html")


@app.route('/algorithm')
def display_algorithm_page():
    return render_template("algorithm.html")


@app.route('/algorithm/macro')
def display_macro_page():
    return render_template("macro.html")


@app.route('/algorithm/micro')
def display_micro_page():
    return render_template("micro.html")


@app.route('/algorithm/sentiment')
def display_sentiment_page():
    return render_template("sentiment.html")


@app.route('/algorithm/context')
def display_context_page():
    return render_template("context.html")


@app.route('/writer-mode')
def display_writer_input():
    return render_template("writermode.html")


@app.route('/writer-mode/interim', methods=["POST"])
def save_info():
    title = request.form.get("title")
    text = request.form.get("text")
    session["title"] = title
    session["text"] = text
    return redirect('/writer-mode/results')


@app.route('/writer-mode/results')
def display_results():
    title = session.get("title")
    text = session.get("text")
    return render_template("writerresults.html", text=text, title=title)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
