"""This file contains the model for the Metrics db table and class"""

from flask_sqlalchemy import SQLAlchemy
from Model_Context import *
from Model_Poem import *
from word_lists import *

db = SQLAlchemy()


class Metrics(db.Model):
    """ contains the metrics for each poem """

    __tablename__ = "metrics"

    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        primary_key=True,
                        nullable=False)
    poet_id = db.Column(db.Integer,
                        db.ForeignKey('poets.poet_id'))
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
    alliteration = db.Column(db.Float)
    positive = db.Column(db.Float)
    negative = db.Column(db.Float)
    active_percent = db.Column(db.Float)
    passive_percent = db.Column(db.Float)

    #FIXME DEFINE THESE FUNCTIONS
    assonance = db.Column(db.Integer)  # TO DEFINE
    consonance = db.Column(db.Integer)  # TO DEFINE
    rhyme = db.Column(db.Integer)  # TO DEFINE

    poem = db.relationship('Poem', backref='metrics')

    def find_matches(self):
        """returns a list with (poem_id, match percent) for every other poem"""

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
        """given poem id, calculates req. data and creates row in metrics"""

        text = (db.session.query(Poem.text)
                          .filter(Poem.poem_id == poem_id).one())[0]
        word_list = Poem._clean_word_list(text)

        wl_data = Metrics._get_wl_data(word_list)
        wl_mean, wl_median, wl_mode, wl_range, pl_words, lex_div = wl_data

        ll_data = Metrics._get_ll_data(text)
        ll_mean, ll_median, ll_mode, ll_range, pl_lines, pl_char = ll_data

        freq_data = Metrics._get_freq_data(word_list)
        i_freq, you_freq, the_freq, is_freq, a_freq = freq_data

        common_percent = Metrics._get_percent_out(word_list, COMMON_W)
        poem_percent = Metrics._get_percent_out(word_list, POEM_W)
        object_percent = Metrics._get_percent_in(word_list, OBJECTS)
        abs_percent = Metrics._get_percent_in(word_list, ABSTRACT)
        male_percent = Metrics._get_percent_in(word_list, MALE)
        female_percent = Metrics._get_percent_in(word_list, FEMALE)
        active_percent = Metrics._get_percent_in(word_list, ACTIVE)
        passive_percent = Metrics._get_percent_in(word_list, PASSIVE)
        positive = Metrics._get_percent_in(word_list, POSITIVE)
        negative = Metrics._get_percent_in(word_list, NEGATIVE)
        alliteration = Metrics._get_alliteration_score(text)

        data = Metrics(poem_id=poem_id, wl_mean=wl_mean, wl_median=wl_median,
                       wl_mode=wl_mode, wl_range=wl_range, ll_mean=ll_mean,
                       ll_median=ll_median, ll_mode=ll_mode, ll_range=ll_range,
                       pl_char=pl_char, pl_lines=pl_lines, pl_words=pl_words,
                       lex_div=lex_div, i_freq=i_freq, you_freq=you_freq,
                       the_freq=the_freq, is_freq=is_freq, a_freq=a_freq,
                       common_percent=common_percent, poem_percent=poem_percent,
                       object_percent=object_percent, abs_percent=abs_percent,
                       male_percent=male_percent, female_percent=female_percent,
                       active_percent=active_percent,
                       passive_percent=passive_percent,
                       positive=positive, negative=negative,
                       alliteration=alliteration)

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
        """returns a list with fequency data for a given list of words

        i_freq is the number of times "i" occurs on it's own (i.e. not as part
            of another word) as a percentage of overall words in the poem.
        you_freq is the number of times "you" occurs on it's own as a percentage
            of overall words in the poem.
        the_freq, is_freq, and a_freq follow the same model, but for "the",
            "is", and "a" respectively.

            >>> x = ['this', 'is', 'a', 'sample', 'text', '.', 'normally',
                     'this', 'would', 'come', 'from', 'a', 'poem', '.',
                     'but', 'i', 'am', 'feeding', 'this', 'in', 'to',
                     'test', 'the', 'function', '.']
            >>> freq_data = Metrics._get_freq_data(x)
            >>> i_freq, you_freq, the_freq, is_freq, a_freq = freq_data
            >>> i_freq
            0.045454545454545456
            >>> you_freq
            0.0
            >>> the_freq
            0.045454545454545456
            >>> is_freq
            0.045454545454545456
            >>> a_freq
            0.09090909090909091]

        this method is called by Metrics.get_metrics to create a new instance
        of the metrics class and will not need to be used directly.
        """

        just_words_list = [w for w in word_list if w.isalpha()]
        num_words = float(len(just_words_list))
        i_freq = word_list.count("i")/num_words
        you_freq = word_list.count("you")/num_words
        the_freq = word_list.count("the")/num_words
        is_freq = word_list.count("is")/num_words
        a_freq = word_list.count("a")/num_words

        return [i_freq, you_freq, the_freq, is_freq, a_freq]

    @staticmethod
    def _clean_word_list(text):
        """returns a list of lowercase words and puncuation for a given text

            >>> text = '\t\t\t Here is some odd sample text: \
                        \n\n I    like to eat cake.'
            >>> Metrics._clean_word_list
            ['here', 'is', 'some', 'odd', 'sample', 'text', ':', 'i', 'like',
            'to', 'eat', 'cake', '.']

        this method is called by Metrics.get_metrics to create a new instance
        of the metrics class and will not need to be used directly.
        """

        punctuation = (".", ",", '"', "!", "?", ":", "-")
        for punc in punctuation:
            space_punc = " " + punc
            text = text.replace(punc, space_punc)
        word_list = text.split()
        word_list = [w.lower() for w in word_list]
        return word_list

    @staticmethod
    def _get_percent_in(poem_word_list, data_word_list):
        """given 2 lists, returns percent of words from the 1st in the 2nd

            >>> x = ['this', 'would', 'come', 'from', 'a', 'poem']
            >>> y = ['this', 'would', 'come', 'from', 'word_lists.py']
            >>> Metrics._get_percent_in(x, y)
            0.6666666666666666

        this method is called by Metrics.get_metrics to create a new instance
        of the metrics class and will not need to be used directly.
        """

        total = len(poem_word_list)
        count = 0
        for word in poem_word_list:
            if word in data_word_list:
                count += 1
        return float(count)/float(total)

    @staticmethod
    def _get_percent_out(poem_word_list, data_word_list):
        """given 2 lists, returns percent of words from the 1st not in the 2nd

            >>> x = ['this', 'would', 'come', 'from', 'a', 'poem']
            >>> y = ['this', 'would', 'come', 'from', 'word_lists.py']
            >>> Metrics._get_percent_out(x, y)
            0.3333333333333333

        this method is called by Metrics.get_metrics to create a new instance
        of the metrics class and will not need to be used directly.
        """

        total = len(poem_word_list)
        count = 0
        for word in poem_word_list:
            if word not in data_word_list:
                count += 1
        return float(count)/float(total)

    @staticmethod
    def _get_alliteration_score(text):
        """given a text, returns alliteration score as a float

        Alliteration score is incremented every time multiple words in the
        same line start with the same letter. Final score is the alliteration
        count divided by the overall number of words in the poem
        """

        lines = text.splt("/n")
        allit_count = 0
        total = 0
        for line in lines:
            line = line.strip()
            words = [w for w in Poem._clean_word_list(line) if w.isalpha()]
            letters = []
            total += len(words)
            for word in words:
                let = word[0]
                if let not in letters:
                    letters.append(let)
                    count = line.count(let)
                    if count > 1:
                        allit_count += (count - 1)
                else:
                    continue

        return allit_count / float(total)

    @staticmethod
    def _get_consonance_score(text):
        pass

    @staticmethod
    def _get_assonance_score(text):
        pass

    @staticmethod
    def _get_rhyme_score(text):
        pass


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
