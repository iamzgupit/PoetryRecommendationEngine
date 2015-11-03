from flask import (Flask, render_template, redirect, jsonify,
                   request, flash, session)
from Model import Poem


app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


@app.route('/')
def homepage():
    """displays homepage with search bar"""
    search_critera = Poem.create_search_params()

    return render_template("homepage.html", poems=jsonify(search_critera))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
