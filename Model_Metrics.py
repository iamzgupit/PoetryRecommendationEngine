from flask_sqlalchemy import SQLAlchemy
from Model_Context import *
from Model_Poem import *
from word_list import *

db = SQLAlchemy()


class Metrics(db.Model):
    """ contains the metrics for each poem """

    __tablename__ = "metrics"

    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        primary_key=True,
                        nullable=False)
    wl_mean = db.Column(db.Float)
    wl_median = db.Column(db.Float)
    wl_mode = db.Column(db.Float)
    wl_range = db.Column(db.Float)
    ll_mean = db.Column(db.Float)
    ll_median = db.Column(db.Float)
    ll_mode = db.Column(db.Float)
    ll_range = db.Column(db.Float)
    pl_char = db.Column(db.Integer)
    pl_lines = db.Column(db.Integer)
    pl_words = db.Column(db.Integer)
    lex_div = db.Column(db.Float)
    the_freq = db.Column(db.Float)
    i_freq = db.Column(db.Float)
    you_freq = db.Column(db.Float)
    is_freq = db.Column(db.Float)
    a_freq = db.Column(db.Float)
    common_percent = db.Column(db.Float)
    poem_percent = db.Column(db.Float)
    object_percent = db.Column(db.Float)
    abs_percent = db.Column(db.Float)
    male_percent = db.Column(db.Float)
    female_percent = db.Column(db.Float)
    assonance = db.Column(db.Integer)  # TO DEFINE
    consonance = db.Column(db.Integer)  # TO DEFINE
    alliteration = db.Column(db.Integer)  # TO DEFINE
    positive = db.Column(db.Integer)  # TO DEFINE
    negative = db.Column(db.Integer)  # TO DEFINE
    RHYME = db.Column(db.Integer)  # TO DEFINE

    # Will add more metrics
    poem = db.relationship('Poem', backref='metrics')
    #include functions to return major_lex, minor_lex and sentiment data

    def find_matches(self):
        poem = Poem.query.get(self.poem_id)
        other_poems = Poem.query.filter(Poem.poem_id != self.poem_id,
                                        Poem.poet_id != poem.poet_id).all()
        for other_poem in other_poems:
            other_metrics = other_poems.metrics
            subjects = [sub.subject for sub in other_poems.subject]
            terms = [term.term for term in other_poems.term]
            regions = [region.region for region in other_poem.regions]
        # PEARSON CALCULATION EXAMINES METRICS FOR EACH POEM
        # CHECK SUBJECTS SHARED, POETIC TERMS SHARED, REGIONS SHARED
        # CHECK WORDS SHARED
        # RETURN LIST OF TUPLES (poem_id, match_percent) SORTED HIGH -> LOW
        # CONTROL FOR ONLY TAKE THE HIGHEST POEM FOR EACH POET

    def get_context_data(self):
        return []

    def get_major_lex_data(self):
        return []

    def get_minor_lex_data(self):
        return []

    def get_sentiment_data(self):
        return []

    @classmethod
    def get_metrics(poem_id):

        text = (db.session.query(Poem.text)
                          .filter(Poem.poem_id == poem_id).one())[0]
        word_list = Poem._clean_word_list(text)

        wl_data = Metrics._get_wl_data(word_list)
        wl_mean, wl_median, wl_mode, wl_range, pl_words, lex_div = wl_data

        ll_data = Metrics._get_ll_data(text)
        ll_mean, ll_median, ll_mode, ll_range, pl_lines, pl_char = ll_data

        freq_data = Metrics._get_freq_data(word_list)
        i_freq, you_freq, the_freq, is_freq, a_freq = freq_data

        common_percent = Metrics._get_percent_out(word_list, COMMON_WORDS)
        poem_percent = Metrics._get_percent_out(word_list, POEM_WORDS)
        object_percent = Metrics._get_percent_in(word_list, OBJECT_WORDS)
        abs_percent = Metrics._get_percent_in(word_list, ABST_WORDS)
        male_percent = Metrics._get_percent_in(word_list, MALE_WORDS)
        female_percent = Metrics._get_percent_in(word_list, FEMALE_WORDS)

        data = Metrics(poem_id=poem_id, wl_mean=wl_mean, wl_median=wl_median,
                       wl_mode=wl_mode, wl_range=wl_range, ll_mean=ll_mean,
                       ll_median=ll_median, ll_mode=ll_mode, ll_range=ll_range,
                       pl_char=pl_char, pl_lines=pl_lines, pl_words=pl_words,
                       lex_div=lex_div, i_freq=i_freq, you_freq=you_freq,
                       the_freq=the_freq, is_freq=is_freq, a_freq=a_freq,
                       common_percent=common_percent, poem_percent=poem_percent,
                       object_percent=object_percent, abs_percent=abs_percent,
                       male_percent=male_percent, female_percent=female_percent)

        db.session.add(data)

    @staticmethod
    def _get_wl_data(word_list):
        num_words = len(word_list)

        wl_range = max(lengths) - min(lengths)
        wl_mean = sum(lengths) / num_words
        if num_words % 2 == 0:
            wl_median = (lengths[num_words/2] + lengths[(num_words/2) + 1])/2
        else:
            wl_median = lengths[num_words/2]
        #FIXME YOU COUNTER HERE AND FOR OTHER .get STATEMENTS
        len_dict = {}
        for length in lengths:
            len_dict[length] = len_dict.get(length, 0) + 1

        maximum = max(len_dict.values())
        for length in len_dict:
            if len_dict[length] == maximum:
                wl_mode = length
                break

        unique = set(word_list)
        lex_div = len(unique) / num_words

        return [wl_mean, wl_median, wl_mode, wl_range, num_words, lex_div]

    @staticmethod
    def _get_ll_data(text):
        line_list = text.split("\n")
        lengths = sorted([len(l) for l in line_list])
        num_lines = len(line_list)

        ll_range = max(lengths) - min(lengths)
        ll_mean = sum(lengths) / num_lines

        if num_lines % 2 == 0:
            ll_median = (lengths[num_lines/2] + lengths[(num_lines/2) + 1])/2
        else:
            ll_median = lengths[num_lines/2]

        len_dict = {}
        for length in lengths:
            len_dict[length] = len_dict.get(length, 0) + 1

        maximum = max(len_dict.values())
        for length in len_dict:
            if len_dict[length] == maximum:
                ll_mode = length
                break

        pl_char = sum(lengths)

        return [ll_mean, ll_median, ll_mode, ll_range, num_lines, pl_char]

    @staticmethod
    def _get_freq_data(word_list):
        word_list = Poem._clean_word_list(text)
        num_words = len(word_list)
        i_freq = word_list.count("i")/num_words
        you_freq = word_list.count("you")/num_words
        the_freq = word_list.count("the")/num_words
        is_freq = word_list.count("is")/num_words
        a_freq = word_list.count("a")/num_words

        return [i_freq, you_freq, the_freq, is_freq, a_freq]

    @staticmethod
    def _clean_word_list(text):
        punctuation = (".", ",", '"', "!", "?", ":", "-", "\n", "\r", "\t")
        for punc in punctuation:
            text = text.replace(punc, " ")
        word_list = text.split(" ")
        word_list = [w.lower() for w in word_list]
        return word_list

    @staticmethod
    def _get_percent_in(poem_word_list, data_word_list):
        total = len(poem_word_list)
        count = 0
        for word in poem_word_list:
            if word in data_word_list:
                count += 1
        return float(count)/float(total)

    @staticmethod
    def _get_percent_out(poem_word_list, data_word_list):
        total = len(poem_word_list)
        count = 0
        for word in poem_word_list:
            if word not in data_word_list:
                count += 1
        return float(count)/float(total)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
