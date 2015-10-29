""" Models and database functions for poetry recommendation engine project"""

from flask_sqlalchemy import SQLAlchemy
from unidecode import unidecode
from bs4 import BeautifulSoup
from os import listdir
from sqlalchemy import func

db = SQLAlchemy()


class Poem(db.Model):
    """Poem Object"""

    __tablename__ = "poems"

    poem_id = db.Column(db.Integer, nullable=False, primary_key=True)
    poet_id = db.Column(db.Integer,
                        db.ForeignKey('poets.poet_id'))
    title = db.Column(db.Text, nullable=False)
    formatted_text = db.Column(db.Text)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text)
    copyright = db.Column(db.Text)

    # allowing url, formatted_text, and poet_id to be null allows
    # us to use the same model for user-submitted poetry
    poet = db.relationship('Poet', backref='poems')

    @staticmethod
    def _find_content(word_list, start_word, stop_word):
        """returns index of start_word, stop_word in word_list as [start, stop]

        >>> word_list = ["hello", "dog", "how", "are", "you"]
        >>> _find_content(word_list, "dog", "you")
        [1, 4]

        we can then use this to parse a list and receive the words starting
        at start_word and ending right before stop_word.

        This function is called by _parse, and will not need to be used directly
        """

        start = 0
        stop = len(word_list)
        for i in range(len(word_list)):
            # the .lower will control for capitalization differences in the
            # start_word and stop_word as entered compared to their presense
            # in word list. If a word exists mutltiple times and you want to target
            # a particular capitalization, you'd want to remove .lower() from
            # both sides of the if and elif here.
            if word_list[i].lower() == start_word.lower():
                start = i
            elif word_list[i].lower() == stop_word.lower():
                stop = i
                if start_word.lower() in [w.lower() for w in
                                          word_list[start: stop]]:
                    break
        return [start, stop]

    @staticmethod
    def _find_term(word_list, term_name):
        """returns index of term_name + 1 and index of next all-caps string

        This is unique for parsing our context list, in which a term is
        followed by values of that term up until another term is introduced,
        in all-caps

            >>> info = [u'Subjects', u'Men & Women', u'Philosophy', u'Love',
                        u'Living', u'Romantic Love', 'Classic Love',
                        u'Desire', u'Realistic and Complicated', u'The Mind',
                        u'Poetic Terms', u'Free Verse', u'Metaphor',
                        u'SUBJECT', u'Men and Women', u'Philosophy',
                        u'Arts and Sciences']
            >>> start, stop = Poem._find_term(info, 'poetic terms')
            >>> start
            11
            >>> stop
            13
            >>> info[start:stop]
            [u'Free Verse', u'Metaphor']

        This function is called by parse and will never need to be used directly
        """

        start = 0
        stop = len(word_list)
        for i in range(len(word_list)):
            if word_list[i].lower() == term_name.lower():
                start = i + 1
            elif start > 0 and i > start and word_list[i][0:3].isupper():
                stop = i
                break

        return [start, stop]

    @staticmethod
    def _clean_listobj(list_obj):
        """ given a beautiful soup list object, returns clean list of strings

        This is called by parse and will never need to be used directly
        """

        new_list = []
        for item in list_obj:
            clean = item.get_text()
            clean = clean.replace("\r", '')
            clean = clean.replace("\t", '')
            clean_split = clean.split("\n")
            for word in clean_split:
                word = word.strip().strip(",")
                if len(word) >= 1:
                    new_list.append(word)
        return new_list

    @staticmethod
    def _get_text(html_string):
        """ given an html string, will return a string of just the text

        >>> html_string = "<div>hello there <em>Patrick</em></div>"
        >>>Poem._get_text(html_string)
        u'hello there Patrick'

        BeautifulSoup's get_text and .text functions seem to malfunction
        on one or two poems. This is called by parse and will never need
        to be used directly.
        """

        text = []
        content = False
        for l in html_string:
            if l == "<":
                content = False
            elif l == ">":
                content = True
            if content and l != ">":
                text.append(l)
        string = "".join(text)
        string = string.strip()
        return unidecode(string)

    @staticmethod
    def _find_author(soup_object, poem_id):
        author_info = soup_object.find("span", class_="author")
        if author_info:
            author = author_info.find("a")
            if author:
                author = author.text.strip()
            else:
                author = author_info.text.strip()
                if author.startswith("By "):
                    author = author.lstrip("By ")
                elif author.startswith("by "):
                    author = author.lstrip("by ")

            split_author = author.split(" ")
            author = " ".join([w for w in split_author if len(w) > 0])

        else:
            print "\n\n\n AUTHOR_INFO ISSUE, POEM: {}\n\n\n".format(poem_id)
            author = None

        return author

    @staticmethod
    def _find_birth_year(soup_object, poem_id):
        rough_birth_year = soup_object.find("span", class_="birthyear")
        if rough_birth_year:
            birth_year = unidecode(rough_birth_year.text)
            if "-" in birth_year:
                birth_year = int(birth_year.split("-")[0])
            elif "b." in birth_year:
                birth_year = int(birth_year.lstrip("b. "))
            elif len(birth_year) == 4:
                try:
                    birth_year = int(birth_year)
                except:
                    print "\n\n {}: BIRTHYEAR STRANGE -- {}".format(poem_id,
                                                                    birth_year)
            elif birth_year:
                print "\n\n{}: ISSUE WITH BIRTHYEAR:{}\n\n".format(poem_id,
                                                                   birth_year)
                birth_year = None
        else:
            birth_year = None

        return birth_year

    @staticmethod
    def _create_poet(soup_object, poem_id):

        author = Poem._find_author(soup_object, poem_id)
        birth_year = Poem._find_birth_year(soup_object, poem_id)

        if author:
            poet = Poet.query.filter(Poet.name == author).first()
            if not poet:
                poet = Poet(name=author, birth_year=birth_year)
                db.session.add(poet)
                db.session.commit()

            poet_id = poet.poet_id

        else:
            print "\n\n {}: ISSUE WITH POET_ID".format(poem_id)
            poet_id = None

        return poet_id

    @staticmethod
    def _get_copyright(soup_object):

        credits = soup_object.find("div", "credit")
        if credits:
            credits = credits.get_text()
            credits = credits.strip()
            cwlist = credits.split(" ")
            start, stop = Poem._find_content(cwlist, "Copyright", "Reprinted")
            copyright = " ".join(cwlist[start:stop])
        else:
            copyright = None

        return copyright

    @staticmethod
    def _set_regions(context, poem_id):
        regions = []
        for i in range(len(context)):
            if "REGION" in context[i]:
                regions = context[i+1].split(', ')
                break

        for region in regions:
            reg = Region.query.filter(Region.region == region).first()
            if not reg:
                reg = Region(region=region)
                db.session.add(reg)
                db.session.commit()

            region_id = reg.region_id
            poem_region = PoemRegion(region_id=region_id,
                                     poem_id=poem_id)
            db.session.add(poem_region)
            db.session.commit()

    @staticmethod
    def _set_terms(context, poem_id):
        if "Poetic Terms" in context:
            start, stop = Poem._find_term(context, "poetic terms")
            poetic_terms = [term.rstrip(', ') for term in context[start:stop]]
        else:
            poetic_terms = []

        for poetic_term in poetic_terms:
            term = Term.query.filter(Term.term == poetic_term).first()
            if not term:
                term = Term(term=poetic_term)
                db.session.add(term)
                db.session.commit()

            term_id = term.term_id
            poem_term = PoemTerm(term_id=term_id, poem_id=poem_id)
            db.session.add(poem_term)
            db.session.commit()

    @staticmethod
    def _set_subjects(context, poem_id):
        if "SUBJECT" in context:
            start, stop = Poem._find_term(context, "SUBJECT")
            subjects = [sub for sub in context[start:stop]]
        else:
            subjects = []

        for subject in subjects:
            sub = Subject.query.filter(Subject.subject == subject).first()
            if not sub:
                sub = Subject(subject=subject)
                db.session.add(sub)
                db.session.commit()

            sub_id = sub.subject_id
            poem_subject = PoemSubject(subject_id=sub_id,
                                       poem_id=poem_id)
            db.session.add(poem_subject)
            db.session.commit()

    @staticmethod
    def _set_context(soup_object, poem_id):
        rough_context = soup_object.find_all("p", class_="section")
        context = Poem._clean_listobj(rough_context)

        Poem._set_regions(context, poem_id)
        Poem._set_terms(context, poem_id)
        Poem._set_subjects(context, poem_id)

    @classmethod
    def parse(cls, file_name):
        """given a text file containing html content, creates Poem object"""

        file_path = "webscrape/Poem_Files/" + file_name
        poem_file = open(file_path).read()
        soup = BeautifulSoup(poem_file, "html5lib")

        poem_id = int(file_name.rstrip(".text"))
        url = "http://www.poetryfoundation.org/poem/" + str(poem_id)

        title_info = soup.find(id="poem-top")
        if title_info:
            title = title_info.text.strip()
        elif soup.find("div", class_="poem"):
            print "\n\n\nTITLE ISSUE. POEM {}\n\n\n".format(poem_id)
            title = None
        else:
            #This isn't a poem object
            return

        poet_id = Poem._create_poet(soup, poem_id)

        html_content = soup.find("div", class_="poem")
        if not html_content:
            # This isn't a poem object
            return

        formatted_text = unicode(html_content)

        try:
            text = html_content.text.replace('\t', ' ')
            text = text.replace('\r', '').strip()
            text = unidecode(text)
        except AttributeError:
            text = Poem._get_text(formatted_text)

        copyright = Poem._get_copyright(soup)

        new_poem = Poem(poem_id=poem_id, poet_id=poet_id, title=title, url=url,
                        formatted_text=formatted_text, text=text,
                        copyright=copyright)

        db.session.add(new_poem)
        db.session.commit()
        Poem._set_context(soup, poem_id)


class Poet(db.Model):
    """ contains individual poets and their birthyear """

    __tablename__ = "poets"

    poet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    birth_year = db.Column(db.Integer)


class Region(db.Model):
    """ contains regions as assigned by the Poetry Foundation"""

    __tablename__ = "regions"

    region_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    region = db.Column(db.Text, nullable=False)

    poems = db.relationship("Poem",
                            secondary='poem_region',
                            backref='regions')


class PoemRegion(db.Model):
    """ connects poem to region"""

    __tablename__ = "poem_region"

    pr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        nullable=False)
    region_id = db.Column(db.Integer,
                          db.ForeignKey('regions.region_id'),
                          nullable=False)

    poem = db.relationship("Poem", backref="poem_regions")
    region = db.relationship("Region", backref="poem_regions")


class Term(db.Model):
    """ Contains Poetic Terms as assigned by the Poetry Foundation"""

    __tablename__ = "terms"

    term_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    term = db.Column(db.Text, nullable=False)

    poems = db.relationship("Poem",
                            secondary='poem_terms',
                            backref="terms")


class PoemTerm(db.Model):
    """ connects poem to poetic term"""

    __tablename__ = "poem_terms"

    pt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        nullable=False)
    term_id = db.Column(db.Integer,
                        db.ForeignKey('terms.term_id'),
                        nullable=False)

    poem = db.relationship("Poem", backref="poem_terms")
    term = db.relationship("Term", backref="poem_terms")


class Subject(db.Model):
    """ Contains poem subjects as assigned by The Poetry Foundation"""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject = db.Column(db.Text, nullable=False)

    poems = db.relationship("Poem",
                            secondary='poem_subjects',
                            backref="subjects")


class PoemSubject(db.Model):
    """ connects poem to subject as noted by the Poetry Foundation """

    __tablename__ = "poem_subjects"

    ps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        nullable=False)
    subject_id = db.Column(db.Integer,
                           db.ForeignKey('subjects.subject_id'),
                           nullable=False)

    poem = db.relationship("Poem", backref="poem_subjects")
    subject = db.relationship("Subject", backref="poem_subjects")


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

    # Will add more metrics
    poem = db.relationship('Poem', backref='metrics')
    #include functions to return major_lex, minor_lex and sentiment data

    @classmethod
    def get_metrics(poem_id):

        text = (db.session.query(Poem.text)
                          .filter(Poem.poem_id == poem_id).one())[0]

        wl_data = Metrics._get_wl_data(text)
        wl_mean, wl_median, wl_mode, wl_range, pl_words, lex_div = wl_data

        ll_data = Metrics._get_ll_data(text)
        ll_mean, ll_median, ll_mode, ll_range, pl_lines, pl_char = ll_data

        data = Metrics(poem_id=poem_id, wl_mean=wl_mean, wl_median=wl_median,
                       wl_mode=wl_mode, wl_range=wl_range, ll_mean=ll_mean,
                       ll_median=ll_median, ll_mode=ll_mode, ll_range=ll_range,
                       pl_char=pl_char, pl_lines=pl_lines, pl_words=pl_words,
                       lex_div=lex_div)

        db.session.add(data)

    @staticmethod
    def _get_wl_data(text):
        word_list = text.split(" ")
        lengths = sorted([len(w) for w in word_list])
        num_words = len(word_list)

        wl_range = max(lengths) - min(lengths)
        wl_mean = sum(lengths) / num_words
        if num_words % 2 == 0:
            wl_median = (lengths[num_words/2] + lengths[(num_words/2) + 1])/2
        else:
            wl_median = lengths[num_words/2]

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


#HELPER FUNCTIONS
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poetry.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


def load_poems(start):
    """Seeds the database with poems from the Poem_Files folder"""
    poems = listdir("webscrape/Poem_Files")

    for poem in poems:
        Poem.parse(poem)


def delete_link_tables(delete_id):
    poem_subs = (PoemSubject.query.filter(PoemSubject.poem_id
                                          == delete_id).all())
    for poem_sub in poem_subs:
        print """Deleting PS ID: {},
                 P: {}, S: {}""".format(poem_sub.ps_id,
                                        poem_sub.poem_id,
                                        poem_sub.subject_id)
        db.session.delete(poem_sub)

    poem_terms = PoemTerm.query.filter(PoemTerm.poem_id
                                       == delete_id).all()
    for poem_term in poem_terms:
        print """Deleting PT ID: {},
                 P: {}, T: {}""".format(poem_term.pt_id,
                                        poem_term.poem_id,
                                        poem_term.term_id)
        db.session.delete(poem_term)

    poem_regions = PoemRegion.query.filter(PoemRegion.poem_id
                                           == delete_id).all()
    for poem_reg in poem_regions:
        print """Deleting PR ID: {},
                 P: {}, R: {}""".format(poem_reg.pr_id,
                                        poem_reg.poem_id,
                                        poem_reg.region_id)
        db.session.delete(poem_reg)


def clean_database():
    duplicates = (db.session.query(Poem.title, Poem.poet_id)
                            .group_by(Poem.title, Poem.poet_id)
                            .having(func.count(Poem.poem_id) > 1).all())
    for title, poet_id in duplicates:
        poems = Poem.query.filter(Poem.title == title,
                                  Poem.poet_id == poet_id).all()
        if len(poems) > 1:
            for i in range(0, (len(poems) - 1)):
                model = poems[-1]
                test = poems[i]
                model_id = model.poem_id
                model_title = model.title.encode("utf-8")
                print "USING POEM {} AS MODEL FOR {}".format(model_id,
                                                             model_title)
                if (model.text == test.text
                        and model.subjects == test.subjects
                        and model.terms == test.terms
                        and model.regions == test.regions):

                    delete_id = test.poem_id
                    print "deleting poem: {}".format(delete_id)

                    delete_link_tables(delete_id)

                    db.session.commit()
                    db.session.delete(test)
                else:
                    print "Poem {} is different!".format(test.poem_id)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
