from flask import (Flask, render_template, redirect, jsonify,
                   request, session)
from random import choice
from Model import Poem, Metrics, UserMetrics, connect_to_db, db
from requests import get
from bs4 import BeautifulSoup


app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


def get_wiki_info(poem):
    name = poem.poet.name.replace(" ", "_")
    wikipedia_url = "https://en.wikipedia.org/wiki/" + name
    page = get(wikipedia_url).text
    if "does not have an article with this exact name" in page:
        wikipedia_url = None
        source = None
    else:
        soup = BeautifulSoup(page, "html5lib")
        info_box = soup.find("table", class_="infobox vcard")
        if info_box:
            image = info_box.find("img")
            if image:
                attrib = image.attrs
                source = attrib['src']
                source = "https:" + source
            else:
                source = '/static/parchment.jpg'
        else:
            wikipedia_url = None
            source = None

    return (wikipedia_url, source)


# @app.route('/subjectgraph.json')
# def subjectData():
#     return jsonify()


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

    NUM_RESULTS = 5

    main_poem = Poem.query.get(poem_id)
    main_metrics = Metrics.query.get(main_poem.poem_id)

    match_metrics = main_metrics.find_matches(limit=NUM_RESULTS)

    match_data = []
    for i in range(NUM_RESULTS):
        poem, poet, match = match_metrics[i]
        match = 100 - (match * 10)
        match = "{:.2f}%".format(match)
        match_data.append((poem, match, i + 1))

    session["match"] = match_data
    match_poems = [(Poem.query.get(p), m, i) for p, m, i in match_data]

    wikipedia_url, source = get_wiki_info(main_poem)

    return render_template("displaymatches.html", main_poem=main_poem,
                           match_poem=main_poem, wikipedia_url=wikipedia_url,
                           source=source, match_poems=match_poems)


@app.route('/<int:poem_id>/<int:index>')
def display_search_poems(poem_id, index):

    main_poem = Poem.query.get(poem_id)

    match_data = session.get("match")
    match_poems = [(Poem.query.get(poem), match, i)
                   for poem, match, i in match_data]

    if index:
        match_poem = match_poems[index - 1][0]
    else:
        match_poem = main_poem

    wikipedia_url, source = get_wiki_info(match_poem)

    return render_template("displaymatches.html", main_poem=main_poem,
                           match_poem=match_poem, wikipedia_url=wikipedia_url,
                           source=source, match_poems=match_poems)


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

    NUM_RESULTS = 5

    title = request.form.get("title")
    text = request.form.get("text")
    session["title"] = title
    session["text"] = text

    poem = UserMetrics(title=title, text=text)
    matches = poem.find_matches(limit=NUM_RESULTS)

    match_data = []
    for i in range(NUM_RESULTS):
        poem, poet, match = matches[i]
        match = 100 - (match * 10)
        match = "{:.2f}%".format(match)
        match_data.append((poem, match, i + 1))

    session["match"] = match_data

    return redirect('/writer-mode/results')


@app.route('/writer-mode/results')
def display_results():
    title = session.get("title")
    text = session.get("text")

    match_data = session.get("match")
    match_poems = [(Poem.query.get(poem), match, i)
                   for poem, match, i in match_data]

    wikipedia_url = None
    source = None

    return render_template("writerresults.html", text=text, title=title,
                           main_title=title, match_poems=match_poems,
                           wikipedia_url=wikipedia_url, source=source)


@app.route('/writer-mode/results/<int:index>')
def display_result_poem(index):

    title = session.get("title")
    match_data = session.get("match")
    match_poems = [(Poem.query.get(poem), match, i)
                   for poem, match, i in match_data]
    if index:
        main_poem = match_poems[index - 1][0]
        text = main_poem.formatted_text
        main_title = main_poem.title
        wikipedia_url, source = get_wiki_info(main_poem)

    else:
        text = session.get("text")
        main_title = title
        wikipedia_url = None
        source = None

    return render_template("writerresults.html", text=text, title=title,
                           main_title=main_title, match_poems=match_poems,
                           wikipedia_url=wikipedia_url, source=source)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
