from flask import (Flask, render_template, redirect, jsonify,
                   request, flash, session)
from Model import Poem, connect_to_db


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


@app.route('/<int:poem_id>')
def display_search_results(poem_id):
    main_poem = Poem.query.get(poem_id)
    return render_template("searchresults.html", main_poem=main_poem)


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
