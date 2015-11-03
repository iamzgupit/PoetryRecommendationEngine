from flask import (Flask, render_template, redirect, jsonify,
                   request, flash, session)
from Model_Poem import Poem
from Model_Metrics import Metrics
from Model_Context import *


app = Flask(__name__)

app.secret_key = "TEMPORARY SECRET KEY"


@app.route('/')
def homepage():
    """displays homepage with search bar"""

    return render_template("homepage.html")
