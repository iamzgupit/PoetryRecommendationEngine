from flask import (Flask, render_template, redirect, jsonify,
                   request, flash, session)
from Model_Poem import Poem
from Model_Metrics import Metrics
from Model_Context import *
from searchpoems import poem


app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


@app.route('/')
def homepage():
    """displays homepage with search bar"""

    return render_template("homepage.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
