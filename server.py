from flask import (Flask, render_template, redirect, jsonify,
                   request, session)
from flask_debugtoolbar import DebugToolbarExtension
from random import choice
from Model import Poem, Metrics, Region, Term, UserMetrics, connect_to_db, db
from requests import get
from bs4 import BeautifulSoup

app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


def get_wiki_info(poem):
    """returns wikipedia url and link to main picture if applicable"""

    name = poem.poet.name.replace(" ", "_")
    wikipedia_url = "https://en.wikipedia.org/wiki/" + name
    try:
        page = get(wikipedia_url).text
    except:
        return (None, None)

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
    metrics_list = Metrics.query.all()

    wl_avg_data = Metrics.get_wl_average_data(metrics_list)
    wl_range_data = Metrics.get_wl_range_data(metrics_list)

    ll_avg_data = Metrics.get_ll_average_data(metrics_list)
    ll_range_data = Metrics.get_ll_range_data(metrics_list)

    pl_lines_data = Metrics.get_pl_lines_data(metrics_list)
    pl_char_data = Metrics.get_pl_char_data(metrics_list)
    pl_word_data = Metrics.get_pl_words_data(metrics_list)

    sl_avg_data = Metrics.get_stanza_length_data(metrics_list)
    stanza_num_data = Metrics.get_stanza_num_data(metrics_list)
    sl_range_data = Metrics.get_stanza_range_data(metrics_list)

    return render_template("macro.html", wl_avg_data=wl_avg_data,
                           wl_range_data=wl_range_data, ll_avg_data=ll_avg_data,
                           ll_range_data=ll_range_data, pl_lines_data=pl_lines_data,
                           pl_char_data=pl_char_data, pl_word_data=pl_word_data,
                           sl_avg_data=sl_avg_data, sl_range_data=sl_range_data,
                           stanza_num_data=stanza_num_data)


@app.route('/algorithm/micro')
def display_micro_page():
    metrics_list = Metrics.query.all()

    rhyme_rep = Metrics.get_rhyme_rep_data(metrics_list)
    lex_div = Metrics.get_lex_data(metrics_list)
    filler = Metrics.get_filler_data(metrics_list)
    narrator = Metrics.get_narrator_data(metrics_list)
    alliteration = Metrics.get_alliteration_data(metrics_list)

    return render_template("micro.html", rhyme_rep=rhyme_rep, lex_div=lex_div,
                           filler=filler, narrator=narrator,
                           alliteration=alliteration)


@app.route('/algorithm/sentiment')
def display_sentiment_page():
    return render_template("sentiment.html")


@app.route('/algorithm/context')
def display_context_page():
    return render_template("context.html")


@app.route('/algorithm/subjects')
def display_subject_graph():
    subjects = all_subjects
    link = "../static/subjectgraph.csv"
    category = "Subject: "
    page_title = "Subject Graph"
    explanation_text = "Explanation text will go here!"

    return render_template("contextgraph.html", data_url=link,
                           data_categories=subjects, category=category,
                           page_title=page_title,
                           explanation_text=explanation_text)


@app.route('/algorithm/terms')
def display_term_graph():
    term_data = Term.get_term_data()

    return render_template("terms.html", term_data=term_data)


@app.route('/algorithm/regions')
def display_region_graph():
    region_data = Region.get_region_data()
    return render_template("region.html", region_data=region_data)


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

    temp_text = text.replace("<br>", "\n")
    poem = UserMetrics(title=title, text=temp_text)
    matches = poem.find_matches(limit=NUM_RESULTS)

    match_data = []
    for i in range(NUM_RESULTS):
        poem, poet, match = matches[i]
        match = 100 - (match * 10)
        match = "{:.2f}%".format(match)
        match_data.append((poem, match, i + 1))

    session["match"] = match_data

    return "success!"


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
                           wikipedia_url=wikipedia_url, source=source,
                           poet="User")


@app.route('/writer-mode/results<int:index>')
def display_result_poem(index):

    title = session.get("title")
    match_data = session.get("match")
    match_poems = [(Poem.query.get(poem), match, i)
                   for poem, match, i in match_data]
    if index:
        main_poem = match_poems[index - 1][0]
        text = main_poem.formatted_text
        main_title = main_poem.title
        poet = main_poem.poet.name
        wikipedia_url, source = get_wiki_info(main_poem)

    else:
        text = session.get("text")
        main_title = title
        wikipedia_url = None
        source = None
        poet = "User"

    return render_template("writerresults.html", text=text, title=title,
                           main_title=main_title, match_poems=match_poems,
                           wikipedia_url=wikipedia_url, source=source, poet=poet)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
