from flask import (Flask, render_template, redirect, jsonify,
                   request, session)
from flask_debugtoolbar import DebugToolbarExtension
from random import choice, randint
from model import Poem, Metrics, Region, Term, Subject, BestMatch, UserMetrics, connect_to_db, db
from requests import get
from bs4 import BeautifulSoup
from random import shuffle
from sqlalchemy.orm import joinedload
# from os import environ

app = Flask(__name__)

# app.secret_key = environ['SESSION_KEY']
app.secret_key = "Temporary secret key"


def get_wiki_info(poem):
    """returns wikipedia url and link to main picture if applicable"""

    name = poem.poet.name.replace(" ", "_")
    wikipedia_url = "https://en.wikipedia.org/wiki/" + name
    try:
        page = get(wikipedia_url).text
    except:
        print "ERROR WITH WIKIPEDIA PAGE"
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


@app.route('/settings', methods=['POST'])
def set_params():
    new_auth = request.form.get("new")
    print new_auth
    print type(new_auth)
    session["new_auth"] = new_auth
    print session["new_auth"]
    unique_auth = request.form.get("unique")
    print unique_auth
    print type(unique_auth)
    session["unique_auth"] = unique_auth
    print session["unique_auth"]

    return "Success!"


@app.route('/<int:poem_id>')
def display_search_results(poem_id):

    main_poem = Poem.query.get(poem_id)
    main_metrics = Metrics.query.get(main_poem.poem_id)

    unique_auth = session.get("unique_auth")
    if unique_auth == "False":
        unique_auth = False
    else:
        unique_auth = True

    new_auth = session.get("new_auth")
    if new_auth == "False":
        new_auth = False
    else:
        new_auth = True

    match_metrics = main_metrics.vary_methods(unique_auth=unique_auth,
                                              new_auth=new_auth)

    session["match"] = match_metrics

    match_poems = []
    poem_ids = match_metrics.keys()
    shuffle(poem_ids)

    for i in range(1, 6):
        poem = Poem.query.get(poem_ids[i - 1])
        match_poems.append((poem, i))

    wikipedia_url, source = get_wiki_info(main_poem)

    best_selected = session.get(str(poem_id))

    return render_template("displaymatches.html", main_poem=main_poem,
                           match_poem=main_poem, wikipedia_url=wikipedia_url,
                           source=source, match_poems=match_poems,
                           best_selected=best_selected)


@app.route('/<int:poem_id>/about')
def diplay_poem_about_page(poem_id):
    metric = (db.session.query(Metrics)
                        .filter(Metrics.poem_id == poem_id)
                        .options(joinedload('subjects'))
                        .options(joinedload('poem').joinedload('poet'))
                        .options(joinedload('terms'))
                        .options(joinedload('regions'))
                        .first())

    subjects = metric.subjects
    terms = metric.terms
    regions = metric.regions
    poem = metric.poem
    wikipedia_url, source = get_wiki_info(poem)

    return render_template("aboutpoem.html", poem=poem, subjects=subjects,
                           wikipedia_url=wikipedia_url, source=source,
                           regions=regions, terms=terms, metric=metric)


@app.route('/<int:poem_id>/<int:match_id>')
def display_search_poems(poem_id, match_id):

    main_poem = Poem.query.get(poem_id)

    try:
        match_metrics = session.get("match")
    except:
        new_url = "/" + str(poem_id)
        redirect(new_url)

    match_poems = []
    poem_ids = match_metrics.keys()
    for i in range(1, 6):
        poem = Poem.query.get(poem_ids[i - 1])
        match_poems.append((poem, i))

    if match_id:
        match_poem = Poem.query.get(match_id)

    else:
        match_poem = main_poem

    wikipedia_url, source = get_wiki_info(match_poem)

    best_selected = session.get(str(poem_id))
    print best_selected

    return render_template("displaymatches.html", main_poem=main_poem,
                           match_poem=match_poem, wikipedia_url=wikipedia_url,
                           source=source, match_poems=match_poems,
                           best_selected=best_selected)


@app.route('/feedback', methods=['POST'])
def log_feedback():
    main_id = request.form.get("main_poem")
    match_data = request.form.get("match_poem")
    match_list = match_data.split("/")
    match_id = int(match_list[0])
    index = match_list[1]
    id_string = str(main_id)

    match_poem = Poem.query.get(match_id)
    match_author = match_poem.poet.name
    match_author = match_author.split(" ")
    match_author = match_author[-1]

    session[id_string] = match_author

    match_metrics = session.get("match")
    print match_metrics
    match_info = match_metrics[str(match_id)]
    methods = match_info["methods"]
    list_index = match_info["list_index"]
    euc_distance = match_info["euc_distance"]
    for i in range(len(methods)):
        x = BestMatch(primary_poem_id=main_id, match_poem_id=match_id,
                      euc_distance=euc_distance[i], page_order=index,
                      match_index=list_index[i], method_code=methods[i])
        db.session.add(x)
        db.session.commit()

    return "success"


@app.route('/writerfeedback', methods=['POST'])
def log_writer_feedback():

    main_id = None
    match_data = request.form.get("match_poem")
    match_list = match_data.split("/")
    match_id = int(match_list[0])
    index = match_list[1]

    #creating a re-creatable key from the text to store in the session
    #so that the best match can be saved properly
    text = session.get("text")
    id_string = text.replace(" ", "")
    id_string = id_string[0:5] + id_string[-6:-1]

    match_poem = Poem.query.get(match_id)
    # storing the match_author's last name as the value -- this will be
    # in the class of the appropriate button so that we can mark it as
    # checked if it's already been pressedn.
    match_author = match_poem.poet.name
    match_author = match_author.split(" ")
    match_author = match_author[-1]

    session[id_string] = match_author

    match_metrics = session.get("match")

    match_info = match_metrics[str(match_id)]
    methods = match_info["methods"]
    list_index = match_info["list_index"]
    euc_distance = match_info["euc_distance"]
    for i in range(len(methods)):
        x = BestMatch(primary_poem_id=main_id, match_poem_id=match_id,
                      euc_distance=euc_distance[i], page_order=index,
                      match_index=list_index[i], method_code=methods[i])
        db.session.add(x)
        db.session.commit()

    return "success"


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
    metrics_list = Metrics.query.all()
    pos_neg = Metrics.get_pos_neg_data(metrics_list)
    obj_abs = Metrics.get_obj_abs_data(metrics_list)
    common = Metrics.get_common_data(metrics_list)
    gender = Metrics.get_gender_data(metrics_list)
    active = Metrics.get_active_data(metrics_list)

    return render_template("sentiment.html", pos_neg=pos_neg, obj_abs=obj_abs,
                           common=common, gender=gender, active=active)


@app.route('/algorithm/context')
def display_context_page():

    return render_template("context.html")


@app.route('/algorithm/subjects')
def display_subject_graph():
    show_number = 12
    last_subj_id = 138
    start_at = randint(1, last_subj_id - show_number)
    stop_before = start_at + show_number

    subject_data = Subject.get_subject_data(start_at=start_at,
                                            stop_before=stop_before)

    rough_subjects = db.session.query(Subject.subject, Subject.subject_id).all()
    all_subjects = {}
    for subject, subject_id in rough_subjects:
        all_subjects[subject] = subject_id

    return render_template("subjects.html", subject_data=subject_data, all_subjects=all_subjects)


@app.route('/subjects/<int:subject_id>')
def display_subject_about(subject_id):
    subject = (db.session.query(Subject)
                         .options(joinedload('metrics').joinedload('subjects'))
                         .options(joinedload('metrics').joinedload('poem').joinedload('poet'))
                         .get(subject_id))
    metrics = subject.metrics
    poems = [m.poem for m in metrics]
    subject_data = subject.get_graph_data(metrics=metrics)

    return render_template("aboutsubject.html", subject=subject, poems=poems,
                           subject_data=subject_data)


@app.route('/algorithm/terms')
def display_term_graph():
    show_number = 12
    last_term_id = 49

    start_at = randint(1, last_term_id - show_number)
    stop_before = start_at + show_number

    term_data = Term.get_term_data(start_at=start_at, stop_before=stop_before)

    rough_terms = db.session.query(Term.term, Term.term_id).all()
    all_terms = {}
    for term, term_id in rough_terms:
        all_terms[term] = term_id

    return render_template("terms.html", term_data=term_data, all_terms=all_terms)


@app.route('/terms/<int:term_id>')
def display_term_about(term_id):
    term = (db.session.query(Term)
                      .options(joinedload('metrics').joinedload('terms'))
                      .options(joinedload('metrics').joinedload('poem').joinedload('poet'))
                      .get(term_id))
    metrics = term.metrics
    poems = [m.poem for m in metrics]
    term_data = term.get_graph_data(metrics=metrics)

    return render_template("aboutterm.html", term=term, poems=poems,
                           term_data=term_data)


@app.route('/algorithm/regions')
def display_region_graph():
    show_number = 12
    last_region_id = 34

    start_at = randint(1, last_region_id - show_number)
    stop_before = start_at + show_number

    region_data = Region.get_region_data(start_at=start_at,
                                         stop_before=stop_before)

    rough_regions = db.session.query(Region.region, Region.region_id).all()
    all_regions = {}
    for region, region_id in rough_regions:
        all_regions[region] = region_id

    return render_template("region.html", region_data=region_data, all_regions=all_regions)


@app.route('/regions/<int:region_id>')
def display_region_about(region_id):
    region = (db.session.query(Region)
                        .options(joinedload('metrics').joinedload('regions'))
                        .options(joinedload('metrics').joinedload('poem').joinedload('poet'))
                        .get(region_id))

    metrics = region.metrics
    poems = [m.poem for m in metrics]
    region_data = region.get_graph_data(metrics=metrics)

    return render_template("aboutregion.html", region=region, poems=poems,
                           region_data=region_data)


@app.route('/writer-mode')
def display_writer_input():

    return render_template("writermode.html")


@app.route('/writer-mode/interim', methods=["POST"])
def save_info():

    title = request.form.get("title")
    text = request.form.get("text")
    unique_auth = request.form.get("unique_auth")
    if unique_auth == "False":
        unique_auth = False
    else:
        unique_auth = True

    session["title"] = title
    session["text"] = text

    temp_text = text.replace("<br>", "\n")
    poem = UserMetrics(title=title, text=temp_text)
    match_metrics = poem.vary_methods(unique_auth=unique_auth)

    session["match"] = match_metrics

    return "success!"


@app.route('/writer-mode/results')
def display_results():
    title = session.get("title")
    text = session.get("text")

    match_metrics = session.get("match")
    match_poems = []
    poem_ids = match_metrics.keys()
    for i in range(1, 6):
        poem = Poem.query.get(poem_ids[i - 1])
        match_poems.append((poem, i))

    wikipedia_url = None
    source = None
    url = None
    main_id = None

    id_string = text.replace(" ", "")
    id_string = id_string[0:5] + id_string[-6:-1]
    best_selected = session.get(id_string)

    return render_template("writerresults.html", text=text, title=title,
                           main_title=title, match_poems=match_poems,
                           wikipedia_url=wikipedia_url, source=source,
                           poet="User", best_selected=best_selected,
                           main_id=main_id, url=url)


@app.route('/writer-mode/about')
def about_your_poem():
    title = session.get("title")
    text = session.get("text")

    temp_text = text.replace("<br>", "\n")
    metric = UserMetrics(title=title, text=temp_text)

    return render_template("aboutwriting.html", title=title, text=text,
                           metric=metric)


@app.route('/writer-mode/<int:match_id>')
def display_result_poem(match_id):

    title = session.get("title")
    best_selected = session.get(title)

    text = session.get("text")
    id_string = text.replace(" ", "")
    id_string = id_string[0:5] + id_string[-6:-1]
    best_selected = session.get(id_string)

    match_metrics = session.get("match")

    match_poems = []
    poem_ids = match_metrics.keys()
    for i in range(1, 6):
        poem = Poem.query.get(poem_ids[i - 1])
        match_poems.append((poem, i))

    if match_id:
        match_poem = Poem.query.get(match_id)
        text = match_poem.formatted_text
        main_title = match_poem.title
        main_id = match_poem.poem_id
        poet = match_poem.poet.name
        url = match_poem.url
        wikipedia_url, source = get_wiki_info(match_poem)

    else:
        main_title = title
        wikipedia_url = None
        source = None
        main_id = None
        poet = "User"
        url = None

    return render_template("writerresults.html", text=text, title=title,
                           main_title=main_title, main_id=main_id, url=url,
                           match_poems=match_poems, wikipedia_url=wikipedia_url,
                           source=source, poet=poet, best_selected=best_selected)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
