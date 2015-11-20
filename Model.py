from flask_sqlalchemy import SQLAlchemy
from unidecode import unidecode
from bs4 import BeautifulSoup
from math import sqrt
from word_lists import (COMMON_W, POEM_W, ABSTRACT, OBJECTS, MALE, FEMALE,
                        ACTIVE, PASSIVE, POSITIVE, NEGATIVE)
from requests import get
from sqlalchemy.orm import joinedload
from os import environ

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

    matches = db.relationship("Poem",
                              secondary="best_matches",
                              foreign_keys="BestMatch.primary_poem_id")

    matched_to = db.relationship("Poem",
                                 secondary="best_matches",
                                 foreign_keys="BestMatch.match_poem_id")

    @staticmethod
    def create_search_params():
        """returns dict w/list of dict w/ info for each poem to jsonify

        this is called by the server to create the search parameters for
        typeahead.
        """

        search_params = []
        poems = Poem.query.all()
        for poem in poems:
            info = {}
            info["id"] = poem.poem_id
            info["title"] = poem.title
            if poem.poet:
                info["author"] = poem.poet.name
            else:
                info["author"] = "anonymous"
            search_params.append(info)

        search = {"search": search_params}
        return search

    @staticmethod
    def _find_content(word_list, start_word, stop_word):
        """returns index of start_word, stop_word in word_list as [start, stop]

            >>> word_list = ["hello", "dog", "how", "are", "you"]
            >>> Poem._find_content(word_list, "dog", "you")
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

            >>> info = ['Subjects', 'Philosophy', 'Love', 'Living',\
                        'Poetic Terms', 'Free Verse', 'Metaphor', 'SUBJECT',\
                        'Men and Women']
            >>> start, stop = Poem._find_term(info, "poetic terms")
            >>> start
            5
            >>> stop
            7
            >>> info[start:stop]
            ['Free Verse', 'Metaphor']

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
    def _separate_punctuation(text):
        """given a list of strings, separates punctionation and returns list"""

        punctuation = [".", ",", ":", ";", "--", '"', "!", "?"]
        for punc in punctuation:
            if punc in text:
                text = text.replace(punc, " " + punc)

        return text

    @staticmethod
    def _clean_listobj(list_obj):
        """ given a beautiful soup list object, returns clean list of strings

            >>> class Fake(object):
            ...    def __init__(self, text):
            ...        self.text = text
            ...    def get_text(self):
            ...        return self.text
            >>>
            >>> a = Fake("here is \t\tsome fake text    ")
            >>> b = Fake("and some more.")
            >>> fake_list = [a, b]
            >>> Poem._clean_listobj(fake_list)
            ['here', 'is', 'some', 'fake', 'text', 'and', 'some', 'more', '.']

        This is called by parse and will never need to be used directly
        """

        new_list = []
        for item in list_obj:
            clean = item.get_text()
            clean = clean.replace("\r", '')
            clean = clean.replace("\t", '')
            clean = Poem._separate_punctuation(clean)
            rough_word_list = clean.split(" ")

            word_list = [w for w in rough_word_list if "\n" not in w]
            rough_word_breaks = [w for w in rough_word_list if "\n" in w]

            for word in rough_word_breaks:
                words = word.split("\n")
                word_list.extend(words)

            for word in word_list:
                word = word.strip().strip(",")
                if len(word) >= 1:
                    new_list.append(word)

        return new_list

    @staticmethod
    def _get_text(html_string):
        """ given an html string, will return a string of just the text

        >>> html_string = "<div>hello there <em>Patrick</em></div>"
        >>> Poem._get_text(html_string)
        'hello there Patrick'

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

        if isinstance(string, unicode):
            string = unidecode(string)

        return string

    @staticmethod
    def _find_author(soup_object, poem_id):
        """locates the author in soup obj and returns their name as a string

        This function is called by Poem.parse and will not need to be used
        directly.
        """

        author_info = soup_object.find("span", class_="author")
        if author_info:
            author = author_info.find("a")
            if author:
                author = author.text.strip()
            # some author names are stored in a <a> tag, others are stored as
            # text with "by" or "By" before them -- this way we can grab it
            # either way.
            else:
                author = author_info.text.strip()
                if author.startswith("By "):
                    author = author.lstrip("By ")
                elif author.startswith("by "):
                    author = author.lstrip("by ")

            # author names are often stored with multiple spaces btw first and
            # last name, which we don't want to keep.
            split_author = author.split(" ")
            author = " ".join([w for w in split_author if len(w) > 0])

        # if there is an issue in parsing, we want to know about it and be able
        # to investiage the issue -- this will print the issue information to
        # the console, but otherwise move forward with the parse function,
        # with author stored as None.

        else:
            print "\n\n\n AUTHOR_INFO ISSUE, POEM: {}\n\n\n".format(poem_id)
            author = None

        return author

    @staticmethod
    def _find_birth_year(soup_object, poem_id):
        """locates the author's birth year in soup obj, returns year as integer

        This function is called by Poem.parse and will not need to be used
        directly. Poem.parse feeds it the poem_id as well so that it can print
        an error message if there is any issue and site the specific poem.
        """
        rough_birth_year = soup_object.find("span", class_="birthyear")
        if rough_birth_year:
            birth_year = unidecode(rough_birth_year.text)

            # birth year can be formatted mutiple ways e.g. 'b. 1854',
            # '1854-1901', or '1954' -- we control for each format, and print
            # an error message if the birth year does not fit any of these
            # formats.

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
        """if poet does not exists in table, create's it -- returns poet_id

        this function calls Poem._find_author and Poem._find_birth_year to get
        necessary information to initialize Poet row. This function is in turn
        called by Poem.parse and will not need to be used directly.
        """

        author = Poem._find_author(soup_object, poem_id)

        if author:
            poet = Poet.query.filter(Poet.name == author).first()
            if not poet:
                birth_year = Poem._find_birth_year(soup_object, poem_id)
                poet = Poet(name=author, birth_year=birth_year)
                db.session.add(poet)
                db.session.commit()  # if the poet does not already exist we
                                     # have to commit it before we can get the
                                     # poet_id which is autocreated by the
                                     # database as the primary/foreign key that
                                     # links poems to their poets

            poet_id = poet.poet_id

        else:
            print "\n\n {}: ISSUE WITH POET_ID".format(poem_id)
            poet_id = None

        return poet_id

    @staticmethod
    def _get_copyright(soup_object):
        """ returns copyright information as string, given soup object

        This is unique to the html documents we're parsing, grabs the copyright
        information if it exists and returns it as a string. This is called by
        Poem.parse and will not need to be used directly.
        """

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
        """given context list, creates ties btw poem and the regions noted

        called by Poem._set_context which is in turn called by Poem.parse as
        part of initializing a new poem -- this will never need to be used
        directly.
        """

        regions = []
        for i in range(len(context)):
            if "REGION" in context[i]:
                regions = context[i+1].split(', ')
                break
            # Region information is stored as a string with ", " separating each
            # region, and follows "REGION" in all-caps in the list order.

        for region in regions:
            reg = Region.query.filter(Region.region == region).first()
            if not reg:
                reg = Region(region=region)
                db.session.add(reg)
                db.session.commit()  # if specific region does not already exist
                                     # we need to add it to the db and commit
                                     # before we can get the region_id, which is
                                     # the primary key created by the database

            region_id = reg.region_id

            # regions are bound to poems by entries in the PoemRegion table
            poem_region = PoemRegion(region_id=region_id, poem_id=poem_id)
            db.session.add(poem_region)
            db.session.commit()

    @staticmethod
    def _set_terms(context, poem_id):
        """given context list, creates ties btw poem and the poetic terms noted

        called by Poem._set_context which is in turn called by Poem.parse as
        part of initializing a new poem -- this will never need to be used
        directly.
        """

        poetic_terms = []
        if "Poetic Terms" in context:
            start, stop = Poem._find_term(context, "poetic terms")
            poetic_terms = [term.rstrip(', ') for term in context[start:stop]]
            # terms exist on their own index in the context list, but often have
            # commas and spaces at the end, which we need to strip.

        for poetic_term in poetic_terms:
            term = Term.query.filter(Term.term == poetic_term).first()
            if not term:
                term = Term(term=poetic_term)
                db.session.add(term)
                db.session.commit()  # if specific term does not already exist
                                     # we need to add it to the db and commit
                                     # before we can get the term_id, which is
                                     # the primary key created by the database

            term_id = term.term_id

            # terms are bound to poems by entries in the PoemTerm table
            poem_term = PoemTerm(term_id=term_id, poem_id=poem_id)
            db.session.add(poem_term)
            db.session.commit()

    @staticmethod
    def _set_subjects(context, poem_id):
        """given context list, creates ties btw poem and the poetic terms noted

        called by Poem._set_context which is in turn called by Poem.parse as
        part of initializing a new poem -- this will never need to be used
        directly.
        """

        subjects = []
        if "SUBJECT" in context:
            start, stop = Poem._find_term(context, "SUBJECT")
            subjects = [sub for sub in context[start:stop]]
            # subjects exist on their own index in the context list
            # they don't need to be cleaned.

        for subject in subjects:
            sub = Subject.query.filter(Subject.subject == subject).first()
            if not sub:
                sub = Subject(subject=subject)
                db.session.add(sub)
                db.session.commit()  # if specific subject doesn't already exist
                                     # we need to add it to the db and commit
                                     # before we can get the subject_id
                                     # (the primary key created by the database)

            sub_id = sub.subject_id

            # subjects are bound to poems by entries in the PoemSubject table
            poem_subject = PoemSubject(subject_id=sub_id, poem_id=poem_id)
            db.session.add(poem_subject)
            db.session.commit()

    @staticmethod
    def _set_context(soup_object, poem_id):
        """ creates subject, region, and poem connections for a given soup obj.

        calls Poem._clean_listobj to get clean list object from context, and
        then called Poem._set_regions, Poem._set_terms, and Poem._set_subjects
        to create ties between the poem and the term and subject. This function
        itself is called by Poem.parse as part of initializing a new poem in the
        Poem table, and will not need to be used directly.
        """

        rough_context = soup_object.find_all("p", class_="section")
        context = Poem._clean_listobj(rough_context)

        Poem._set_regions(context, poem_id)
        Poem._set_terms(context, poem_id)
        Poem._set_subjects(context, poem_id)

    @classmethod
    def parse(cls, file_name):
        """given a text file containing html content, creates Poem object

        This is the method that calls most of the other methods as part of
        parsing all the necessary information to create a new Poem, as well as
        handles the actual adding of the poem to the database.
        """

        # previously, we had scraped the pages for each individual poem and
        # stored their html content in a .text file in webscrape/Poem_Files
        # as poem_id.text
        file_path = "webscrape/Poem_Files/" + file_name
        poem_file = open(file_path).read()
        soup = BeautifulSoup(poem_file, "html5lib")

        poem_id = int(file_name.rstrip(".text"))
        url = "http://www.poetryfoundation.org/poem/" + str(poem_id)

        title_info = soup.find(id="poem-top")
        html_content = soup.find("div", class_="poem")

        if title_info and html_content:
            title = title_info.text.strip()

        elif html_content:
            # if there is a div called poem but not a div with id "poem-top"
            # then this is an unusual formatting and we want to print an error
            # message to examine the html further.

            print "\n\n\nTITLE ISSUE. POEM {}\n\n\n".format(poem_id)
            title = None

        else:
            # If there isn't a div with a class poem then the page is not the
            # page we are looking for -- several of the files scraped were in
            # fact for essays or interviews, though stored in the same place as
            # poems, so this is not an issue, but we don't want to move forward
            # if the file is not a poem.
            return

        poet_id = Poem._create_poet(soup, poem_id)

        formatted_text = unicode(html_content)

        try:
            text = html_content.text.replace('\t', ' ')
            text = text.replace('\r', '').strip()
            text = unidecode(text)

        except AttributeError:
            # a few poems had issues with .text and .get_text(), though the html
            # seemed otherwise fine, so I wrote my own function that accomplishes
            # the same purpose, to be used in these cases.
            text = Poem._get_text(formatted_text)

        copyright = Poem._get_copyright(soup)

        new_poem = Poem(poem_id=poem_id, poet_id=poet_id, title=title, url=url,
                        formatted_text=formatted_text, text=text,
                        copyright=copyright)

        db.session.add(new_poem)
        db.session.commit()  # we have to commit the new poem to the database
                             # before we can move forward, since PoemTerm,
                             # PoemSubject, and Poem Region all need to link to
                             # the poem_id.

        Poem._set_context(soup, poem_id)
        db.session.commit()


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

    metrics = db.relationship("Metrics",
                              secondary='poem_region',
                              backref='regions')

    @staticmethod
    def get_region_data(start_at, stop_before):
        regions = (db.session.query(Region)
                             .filter(Region.region_id >= start_at,
                                     Region.region_id < stop_before)
                             .options(joinedload('metrics').joinedload('regions'))
                             .all())

        return Metrics.get_context_graph_data(list_of_context_obj=regions,
                                              name_of_context="region",
                                              metrics_backref="regions")

    def get_graph_data(self, metrics):

        name = self.region

        iden = name.replace(".", "").replace("-", "")
        iden = iden.replace("/", "").replace(",", "").split(" ")

        if iden[0].lower() != "the":
            iden = iden[0]
        else:
            iden = iden[1]

        total = len(metrics)

        connected_data = Metrics.get_single_graph_data(metrics_list=metrics,
                                                       name_of_context="region",
                                                       name=name,
                                                       metrics_backref="regions")

        data = {"name": name,
                "total": total,
                "iden": iden,
                "others": connected_data}

        return data


class PoemRegion(db.Model):
    """ connects poem to region"""

    __tablename__ = "poem_region"

    pr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('metrics.poem_id'),
                        nullable=False)
    region_id = db.Column(db.Integer,
                          db.ForeignKey('regions.region_id'),
                          nullable=False)

    # poem = db.relationship("Poem", backref="poem_regions")
    metrics = db.relationship("Metrics", backref="poem_regions")
    region = db.relationship("Region", backref="poem_regions")


class Term(db.Model):
    """ Contains Poetic Terms as assigned by the Poetry Foundation"""

    __tablename__ = "terms"

    term_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    term = db.Column(db.Text, nullable=False)

    metrics = db.relationship("Metrics",
                              secondary='poem_terms',
                              backref="terms")

    @staticmethod
    def get_term_data(start_at, stop_before):
        terms = (db.session.query(Term)
                           .filter(Term.term_id >= start_at,
                                   Term.term_id < stop_before)
                           .options(joinedload('metrics').joinedload('terms'))
                           .all())

        return Metrics.get_context_graph_data(list_of_context_obj=terms,
                                              name_of_context="term",
                                              metrics_backref="terms")

    def get_graph_data(self, metrics):

        name = self.term

        iden = name.replace(".", "").replace("-", "").replace("/", "").replace(",", "").split(" ")
        if iden[0].lower() != "the":
            iden = iden[0]
        else:
            iden = iden[1]

        total = len(metrics)

        connected_data = Metrics.get_single_graph_data(metrics_list=metrics,
                                                       name_of_context="term",
                                                       name=name,
                                                       metrics_backref="terms")

        data = {"name": name,
                "total": total,
                "iden": iden,
                "others": connected_data}

        return data


class PoemTerm(db.Model):
    """ connects poem to poetic term"""

    __tablename__ = "poem_terms"

    pt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('metrics.poem_id'),
                        nullable=False)
    term_id = db.Column(db.Integer,
                        db.ForeignKey('terms.term_id'),
                        nullable=False)

    poem = db.relationship("Metrics", backref="poem_terms")
    term = db.relationship("Term", backref="poem_terms")


class Subject(db.Model):
    """ Contains poem subjects as assigned by The Poetry Foundation"""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject = db.Column(db.Text, nullable=False)

    metrics = db.relationship("Metrics",
                              secondary='poem_subjects',
                              backref="subjects")

    @staticmethod
    def get_subject_data(start_at, stop_before):
        subjects = (db.session.query(Subject)
                              .filter(Subject.subject_id >= start_at,
                                      Subject.subject_id < stop_before)
                              .options(joinedload('metrics').joinedload('subjects'))
                              .all())

        return Metrics.get_context_graph_data(list_of_context_obj=subjects,
                                              name_of_context="subject",
                                              metrics_backref="subjects")

    def get_graph_data(self, metrics):

        name = self.subject

        iden = name.replace(".", "").replace("-", "").replace("/", "").replace(",", "").split(" ")
        if iden[0].lower() != "the":
            iden = iden[0]
        else:
            iden = iden[1]

        total = len(metrics)

        connected_data = Metrics.get_single_graph_data(metrics_list=metrics,
                                                       name_of_context="subject",
                                                       name=name,
                                                       metrics_backref="subjects")

        data = {"name": name,
                "total": total,
                "iden": iden,
                "others": connected_data}
        return data


class PoemSubject(db.Model):
    """ connects poem to subject as noted by the Poetry Foundation """

    __tablename__ = "poem_subjects"

    ps_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    poem_id = db.Column(db.Integer,
                        db.ForeignKey('metrics.poem_id'),
                        nullable=False)
    subject_id = db.Column(db.Integer,
                           db.ForeignKey('subjects.subject_id'),
                           nullable=False)

    metrics = db.relationship("Metrics", backref="poem_subjects")
    subject = db.relationship("Subject", backref="poem_subjects")


class Metrics(db.Model):
    """ contains the metrics (data as floats) for each poem """

    __tablename__ = "metrics"

    poem_id = db.Column(db.Integer,
                        db.ForeignKey('poems.poem_id'),
                        primary_key=True,
                        nullable=False)

    wl_mean = db.Column(db.Float)    # Macro Lexical Data: larger integer ( > 1)
    wl_median = db.Column(db.Float)  # Macro Lexical Data: larger integer ( > 1)
    wl_mode = db.Column(db.Float)    # Macro Lexical Data: larger integer ( > 1)
    wl_range = db.Column(db.Float)   # Macro Lexical Data: larger integer ( > 1)
    ll_mean = db.Column(db.Float)    # Macro Lexical Data: larger integer ( > 1)
    ll_median = db.Column(db.Float)  # Macro Lexical Data: larger integer ( > 1)
    ll_mode = db.Column(db.Float)    # Macro Lexical Data: larger integer ( > 1)
    ll_range = db.Column(db.Float)   # Macro Lexical Data: larger integer ( > 1)
    pl_char = db.Column(db.Float)    # Macro Lexical Data: larger integer ( > 1)
    pl_lines = db.Column(db.Float)   # Macro Lexical Data: larger integer ( > 1)
    pl_words = db.Column(db.Float)   # Macro Lexical Data: larger integer ( > 1)
    lex_div = db.Column(db.Float)       # Micro Lexical Data: (0 - 1) Percentage
    the_freq = db.Column(db.Float)      # Micro Lexical Data: (0 - 1) Percentage
    i_freq = db.Column(db.Float)        # Micro Lexical Data: (0 - 1) Percentage
    you_freq = db.Column(db.Float)      # Micro Lexical Data: (0 - 1) Percentage
    is_freq = db.Column(db.Float)       # Micro Lexical Data: (0 - 1) Percentage
    a_freq = db.Column(db.Float)        # Micro Lexical Data: (0 - 1) Percentage
    alliteration = db.Column(db.Float)  # Micro Lexical Data: (0 - 1) Percentage
    rhyme = db.Column(db.Float)         # Micro Lexical Data: (0 - 1) Percentage
    end_repeat = db.Column(db.Float)    # Micro Lexical Data: (0 - 1) Percentage
    common_percent = db.Column(db.Float)   # Sentiment Data: (0 - 1) Percentage
    poem_percent = db.Column(db.Float)     # Sentiment Data: (0 - 1) Percentage
    object_percent = db.Column(db.Float)   # Sentiment Data: (0 - 1) Percentage
    abs_percent = db.Column(db.Float)      # Sentiment Data: (0 - 1) Percentage
    male_percent = db.Column(db.Float)     # Sentiment Data: (0 - 1) Percentage
    female_percent = db.Column(db.Float)   # Sentiment Data: (0 - 1) Percentage
    positive = db.Column(db.Float)         # Sentiment Data: (0 - 1) Percentage
    negative = db.Column(db.Float)         # Sentiment Data: (0 - 1) Percentage
    active_percent = db.Column(db.Float)   # Sentiment Data: (0 - 1) Percentage
    passive_percent = db.Column(db.Float)  # Sentiment Data: (0 - 1) Percentage

    # upon analysis, this metrics were found to not be meaningful for our set:
    stanzas = db.Column(db.Float)          # larger integer ( > 1)
    sl_mean = db.Column(db.Float)          # larger integer ( > 1)
    sl_median = db.Column(db.Float)        # larger integer ( > 1)
    sl_mode = db.Column(db.Float)          # larger integer ( > 1)
    sl_range = db.Column(db.Float)         # larger integer ( > 1)

    poem = db.relationship('Poem', backref='metrics')

    def _get_ranges_dict(self):
        """returns a dict w/ initial acceptable ranges for a given metrics obj

        when finding matches, we want to first narrow down our query by four
        macro lexical catagories so that we aren't running our distance algorithm
        on over 10,000 poems each time -- this method get's the inital acceptable
        ranges which we will use to grab a subset of our poems.

            >>> x = Metrics(wl_range=6, ll_mean=50,ll_range=10, pl_lines=50)
            >>> ranges_dict = x._get_ranges_dict()
            >>> expected = {'llrange': {'max': 30,\
                                        'up_adj': 2,\
                                        'down_adj': 4,\
                                        'val': 10,\
                                        'min': -10},\
                            'mean_ll': {'max': 70,\
                                        'up_adj': 2.5,\
                                        'down_adj': 4,\
                                        'val': 50,\
                                        'min': 30},\
                            'plength': {'max': 60,\
                                        'up_adj': 1,\
                                        'down_adj': 2,\
                                        'val': 50,\
                                        'min': 40},\
                            'wlrange': {'max': 10,\
                                        'up_adj': 1,\
                                        'down_adj': 1,\
                                        'val': 6,\
                                        'min': 2}}
            >>> expected == range_dict
            True

        This method is called by Metrics.find_matches and won't need to be used
        directly.
        """

        wlr = self.wl_range
        llm = self.ll_mean
        llr = self.ll_range
        pll = self.pl_lines
        if pll > 80:
            pll_min = 45
            pll_max = pll + 10
        else:
            pll_min = pll - 10
            pll_max = pll + 10

        ranges = {'plength': {'val': pll,
                              'max': pll_max,
                              'min': pll_min,
                              'down_adj': 2,
                              'up_adj': 1},
                  'mean_ll': {'val': llm,
                              'max': llm + 20,
                              'min': llm - 20,
                              'down_adj': 4,
                              'up_adj': 2.5},
                  'llrange': {'val': llr,
                              'max': llr + 20,
                              'min': llr - 20,
                              'down_adj': 4,
                              'up_adj': 2},
                  'wlrange': {'val': wlr,
                              'max': wlr + 4,
                              'min': wlr - 4,
                              'down_adj': 1,
                              'up_adj': 1}}

        return ranges

    def _get_within_range(self, ranges):
        """returns a list of metrics objects fitting the parameters in ranges

        excludes current poem_id. In the case of a UserMetrics instance, poem_id
        will be Null, so this query will go through without any issues -- we
        drop the joined load in the case of a UserMetrics object to make the
        query faster, since we won't be grabbing context data (calling .subjects,
        .terms, or .regions) for UserMetrics objects (which have no context data)
        """

        if self.poem_id is None:
            o_met = (db.session.query(Metrics)
                       .filter(Metrics.poem_id != self.poem_id,
                               Metrics.pl_lines <= ranges["plength"]["max"],
                               Metrics.pl_lines >= ranges["plength"]["min"],
                               Metrics.ll_mean <= ranges["mean_ll"]["max"],
                               Metrics.ll_mean >= ranges["mean_ll"]["min"],
                               Metrics.ll_range >= ranges["llrange"]["min"],
                               Metrics.ll_range <= ranges["llrange"]["max"],
                               Metrics.wl_range >= ranges["wlrange"]["min"],
                               Metrics.wl_range <= ranges["wlrange"]["max"])
                       .all())
        else:
            o_met = (db.session.query(Metrics)
                       .filter(Metrics.poem_id != self.poem_id,
                               Metrics.pl_lines <= ranges["plength"]["max"],
                               Metrics.pl_lines >= ranges["plength"]["min"],
                               Metrics.ll_mean <= ranges["mean_ll"]["max"],
                               Metrics.ll_mean >= ranges["mean_ll"]["min"],
                               Metrics.ll_range >= ranges["llrange"]["min"],
                               Metrics.ll_range <= ranges["llrange"]["max"],
                               Metrics.wl_range >= ranges["wlrange"]["min"],
                               Metrics.wl_range <= ranges["wlrange"]["max"])
                       .options(joinedload('subjects'))
                       .options(joinedload('terms'))
                       .options(joinedload('regions'))
                       .all())

        return o_met

    @staticmethod
    def _increment_down(range_dict):
        """reduces ranges in dic to provide lower number of results

        given the ranges dictionary, modifies the 'min' and 'max' values for
        each attribute to provide a narrower range of accepted values.

        This method is called by Metrics.find_matches and won't need to be used
        directly.
        """

        # for each attribute, we don't want to set the maximum value below,
        # or the minimum value above, the value of the poem we're trying to
        # match, so we check that and adjust as necessary.
        for c in range_dict.values():
            if c['max'] - c['down_adj'] >= c['val']:
                c['max'] -= c['down_adj']
            else:
                c['max'] = c['val']

            if c['min'] + c['down_adj'] <= c['val']:
                c['min'] += c['down_adj']
            else:
                c['min'] = c['val']

    @staticmethod
    def _slim_metrics(ranges, other_metrics):
        """given ranges dict & list of metrics, returns new list fitting ranges

            >>> ranges = {"plength": {"min": 5, "max": 10},\
                          "mean_ll": {"min": 5, "max": 10},\
                          "llrange": {"min": 5, "max": 10},\
                          "wlrange": {"min": 5, "max": 10}}
            >>> met1 = Metric(pl_length=6, ll_mean=6, ll_range=6, wl_range=6)
            >>> met2 = Metrics(pl_length=12, ll_mean=6, ll_range=6, wl_range=6)
            >>> new_list = Metrics._slim_metrics(ranges, [met1, met2])
            >>> new_list == [met1]
            True

        this method is called by Metrics._get_other_metrics which is in turn
        called by Metrics.find_matches and will not need to be used directly.
        """

        new_metrics = []
        for metric in other_metrics:
            if all([metric.pl_lines <= ranges["plength"]['max'],
                    metric.pl_lines >= ranges["plength"]["min"],
                    metric.ll_mean <= ranges["mean_ll"]['max'],
                    metric.ll_mean >= ranges["mean_ll"]["min"],
                    metric.ll_range <= ranges["llrange"]["max"],
                    metric.ll_range >= ranges["llrange"]["min"],
                    metric.wl_range <= ranges["wlrange"]["max"],
                    metric.wl_range >= ranges["wlrange"]["min"]]):
                new_metrics.append(metric)

        return new_metrics

    @staticmethod
    def _increment_up(range_dict):
        """increases ranges to provide higher number of results

        given the ranges dictionary, modifies the 'min' and 'max' values for
        each attribute to provide a larger range of accepted values.

        This method is called by Metrics._get_other_metrics as part of
        Metrics.find_matches and won't need to be used directly.
        """
        for r in range_dict.values():
            r['max'] += r['up_adj']
            r['min'] -= r['up_adj']

    @staticmethod
    def _far_increment_up(range_dict, mult):
        """increases min/max in range_dict to provide higher number of results

        given the ranges dictionary, modifies the 'min' and 'max' values for
        each attribute to provide a larger range of accepted values. This method
        works the same as Metrics._increment_up but allows you to increase the
        amount that you are incrementing by a multiple of the 'up_adjustment'
        criteria. This is useful for poems with outlier values where you need
        to greatly increase the range of accepted values in order to have a
        sufficient number of poems to test.

        This method is called by Metrics._get_other_metrics as part of
        Metrics.find_matches and won't need to be used directly.
        """
        for r in range_dict.values():
            r['max'] += (r['up_adj'] * mult)
            r['min'] -= (r['up_adj'] * mult)

    def _get_other_metrics(self):
        """ returns list of 200-600 metrics obj w/similar macro attributes.

        For a given metrics object(self), we grab 200-600 other metrics objects
        within an accepted range for four macro attributes: word length range
        (wl_range), line length range (ll_range), mean line length (ll_m), and
        poem length by line (pl_lines). We set initial excepted ranges for all
        four attributes based on an analysis of the spread of the data -- query
        the database for metrics with those parameters, check the length, and
        then alter those parameters up or down as necessary until we have a list
        between 200-600 in length, or until we've tried 15 iterations, in which
        we move forward with what we have, to avoid the potential of a loop.

        this method is called by Metrics.find_matches and does not need to be
        used directly.
        """

        ranges = self._get_ranges_dict()

        o_met = self._get_within_range(ranges)

                          # For debugging, to see how many iterations we go
                          # through, and what the values were at each point

        i = 0   # we increment i to avoid being stuck in a loop

        past_length = 0
        length = len(o_met)

        print length      # for debugging, we want to see how many iterations a
                          # given poem requires.

        while length > 400 and i <= 15:

            self._increment_down(range_dict=ranges)
            o_met = Metrics._slim_metrics(ranges=ranges, other_metrics=o_met)

            past_length = length
            length = len(o_met)
            i += 1

            print length  # for debugging, we want to see how many iterations a
                          # given poem requires.

        # if it gets too low, we adjust back up
        while length < 100 and i <= 15:

            if all([length < 40, past_length < 40, i >= 14]):
                # this is for the extreme case where we've been incrementing
                # up for awhile and we still don't have enough results -- we
                # increase the ranges more drastically, and set i back so that
                # it can readjust a bit

                self._far_increment_up(range_dict=ranges, mult=20)
                i = 10

            elif all([length < 50, past_length < 50, i >= 9]):
                # this is for the cases slightly less extreme than the former
                # so that we grab a larger range if after 9 interations we're
                # still below 50, and have been below 50.

                self._far_increment_up(range_dict=ranges, mult=12)

            elif length < 50 and past_length < 50:
                # if that last two lengths were very low, we want to jump up a
                # bit higher than the normal increment up

                self._far_increment_up(range_dict=ranges, mult=6)

            else:
                self._increment_up(range_dict=ranges)

            o_met = self._get_within_range(ranges)

            past_length = length
            length = len(o_met)
            i += 1

            print length  # for debugging, we want to see how many iterations a
                          # given poem requires.

        return o_met

    def _remove_main_auth(self, sorted_matches):
        """is new_auth is True, returns a list without poems by self.poet

        if new_auth is False or if this is a UserMetrics instance, just returns
        sorted_matches as given.
        """

        if self.poem:
            new_matches = [tup for tup in sorted_matches
                           if tup[1] != self.poem.poet_id]
            return new_matches

        else:
            return sorted_matches

    def _remove_dupl_auths(self, sorted_matches):
        """if unique_auth is True, returns list w/best match for each poet_id

        if unique_auth is False, just returns sorted_matches as given.
        """

        final_matches = []
        used_poets = set()
        for match in sorted_matches:
            poet_id = match[1]
            if poet_id not in used_poets:
                final_matches.append(match)
                used_poets.add(poet_id)

        return final_matches

    @staticmethod
    def _recalculate_match(matches, sentwgt, micwgt, macwgt, conwgt):
        """reruns euc distance algorithm with altered weightings"""

        new_matches = []
        for poem_id, poet_id, euc_dist, euc_raw in matches:
            euc_squared = 0
            euc_squared += euc_raw["context"] * conwgt
            euc_squared += euc_raw["sentiment"] * sentwgt
            euc_squared += euc_raw["micro"] * micwgt
            euc_squared += euc_raw["macro"] * macwgt
            euc_distance = sqrt(euc_squared)
            new_matches.append((poem_id, poet_id, euc_distance))

        distance_idx = 2
        sorted_matches = sorted(new_matches, key=lambda tup: tup[distance_idx])

        return sorted_matches

    @staticmethod
    def select_five(results, matches_list, match_code):
        """"""
        for i in range(5):
            poem_id, poet_id, euc_distance = matches_list[i]
            if poem_id in results:
                results[poem_id]["methods"].append(match_code)
                results[poem_id]["euc_distance"].append(euc_distance)
                results[poem_id]["list_index"].append(i)
            else:
                results[poem_id] = {"poet_id": poet_id,
                                    "euc_distance": [euc_distance],
                                    "methods": [match_code],
                                    "list_index": [i]}
                return

    def vary_methods(self, unique_auth=True, new_auth=True):
        """retuns matches with different weights applied"""

        matches = self.find_matches(micwgt=1, sentwgt=1, conwgt=1, macwgt=1,
                                    limit=75, unique_auth=unique_auth,
                                    new_auth=new_auth)
        results = {}
        poem_id, poet_id, euc_distance, euc_raw = matches[0]

        results[poem_id] = {"poet_id": poet_id,
                            "euc_distance": [euc_distance],
                            "list_index": [0],
                            "methods": ["unwgt"]}

        stmic = Metrics._recalculate_match(matches=matches, sentwgt=1, micwgt=2,
                                           macwgt=1, conwgt=1)

        stmac = Metrics._recalculate_match(matches=matches, sentwgt=1, micwgt=1,
                                           macwgt=2, conwgt=1)

        stcon = Metrics._recalculate_match(matches=matches, sentwgt=1, micwgt=1,
                                           macwgt=1, conwgt=2)

        stsent = Metrics._recalculate_match(matches=matches, sentwgt=2, micwgt=1,
                                            macwgt=1, conwgt=1)
        Metrics.select_five(results=results, matches_list=stsent, match_code="stsent")
        Metrics.select_five(results=results, matches_list=stcon, match_code="stcon")
        Metrics.select_five(results=results, matches_list=stmac, match_code="stmac")
        Metrics.select_five(results=results, matches_list=stmic, match_code="stmic")

        return results

    def find_matches(self, micwgt=1, sentwgt=1, conwgt=1, macwgt=1, unique_auth=True, new_auth=True, limit=10):
        """returns a list with (poem_id, match percent) for limit other poems

        for a given metrics (self), will find the best matches and return a list
        of their information in tuples best match -> worst match , limited by
        the limit criteria.

        This method calles Metrics._get_other_metrics to get a narrower list
        of other metrics to check (controlled for macro attributes within a
        reasonable range from the poem's attributes).

        We give this method micwgt, sentwgt, conwgt, and macwgt, which are
        weighting factors that we can use to adjust the importance of different
        sorts of criteria (micro_lex attributes correspond to micwgt, macro_lex
        attributes correspond to macwgt, sentiment attributes correspond to
        sentwgt, and context attributes -- which are the Subjects, Terms, and
        Regions as decided by the Poetry Foundation -- correspond to conwgt).

        limit sets how many of the possible matches we should return,
        unique_auth sets whether to return only the best matched poem for each
        poet (only one per poet if True), and new_auth sets whether to exclude
        the author of the chosen poem from the results (no matches by the author
        of our matching poem if True).
        """

        other_metrics = self._get_other_metrics()

        sorted_matches = self._calc_matches(other_metrics=other_metrics,
                                            micwgt=micwgt,
                                            sentwgt=sentwgt,
                                            macwgt=macwgt,
                                            conwgt=conwgt)

        # if we turn new_auth off, we will receive poems in the results that
        # include poems by the author of our initial poem, otherwise we sort
        # those out by default. Checking for self.poem means that we can use
        # same method with the child class UserMetrics.
        if new_auth:
            sorted_matches = self._remove_main_auth(sorted_matches=sorted_matches)

        # if we turn unique_auth off, we will receive multiple matches by the
        # same author, otherwise, we sort out other matches by the same author
        # keeping only those that are the best fit.
        if unique_auth:
            final_matches = self._remove_dupl_auths(sorted_matches=sorted_matches)
        else:
            final_matches = sorted_matches

        # final_matches = [(180676, 310, 1.1730658920581396), (180649, 232, 1.1992932205497298), (181032, 283, 1.2108784028951076), (238448, 269, 1.2135422970758867), (2085, 196, 1.2359146103377696)]
        return final_matches[:limit]
        # return final_matches

    def _get_criteria(self, other_metric_obj, micro_lex, sentiment, word_list, context):
        """"""

        o_micro_lex = other_metric_obj._get_micro_lex_data()

        # We are adding the percentage of words from one poem in another
        # to our micro lexical data -- this requires making a temporary
        # micro_lex catagory for our main poem, since lists are mutable and
        # we want this percentage to be different for each poem we're
        # comparing

        temp_micro = [n for n in micro_lex]
        word_per, o_word_per = Metrics._get_word_compare(word_list=word_list,
                                                         other=other_metric_obj)

        temp_micro.extend([word_per, o_word_per])
        o_micro_lex.extend([1, 1])

        o_sentiment = other_metric_obj._get_sentiment_data()

        if self.poem:  # checking that this is not a UserMetrics class.
            # getting the percentage of context shared, the ideal values (1)
            self_context, o_context = self._create_context_lists(other_poem=other_metric_obj,
                                                                 context=context)
            # context = False
            # o_context = False
        else:
            self_context = False
            o_context = False

        macro, o_macro = self._get_macro_compare(other_metric_obj)

        return {"temp_micro": temp_micro, "o_micro_lex": o_micro_lex,
                "o_sentiment": o_sentiment, "sentiment": sentiment,
                "context": self_context, "o_context": o_context,
                "macro": macro, "o_macro": o_macro}

    def _get_euc_distance(self, comparison_dict, conwgt, micwgt, sentwgt, macwgt):
        """"""
        euc_squared = 0

        context = comparison_dict["context"]
        o_context = comparison_dict["o_context"]

        if context and o_context:
            con_raw = Metrics._get_euc_raw(context, o_context, conwgt)
            euc_squared += con_raw

            # if we don't have context data, we increase the weighting of the
            # other criteria.
        else:
            addwgt = conwgt / 3
            micwgt += addwgt
            sentwgt += addwgt
            macwgt += addwgt
            con_raw = 0

        mic_raw = Metrics._get_euc_raw(comparison_dict["temp_micro"],
                                       comparison_dict["o_micro_lex"],
                                       micwgt)
        euc_squared += mic_raw

        sent_raw = Metrics._get_euc_raw(comparison_dict["sentiment"],
                                        comparison_dict["o_sentiment"],
                                        sentwgt)
        euc_squared += sent_raw

        mac_raw = Metrics._get_euc_raw(comparison_dict["macro"],
                                       comparison_dict["o_macro"],
                                       macwgt)
        euc_squared += mac_raw

        euc_distance = sqrt(euc_squared)

        results = (euc_distance, {"context": con_raw, "macro": mac_raw,
                                  "micro": mic_raw, "sentiment": sent_raw})

        return results

    def _calc_matches(self, other_metrics, micwgt, sentwgt, conwgt, macwgt):
        """given self and other poem objects, returns list w/ match closeness

        this method is called by find_matches, so it won't need to be called
        directly. It in gathers all the necessary data and feeds it to
        Metrics._get_euc_raw, taking the square root of the end results to
        calculate the euclidean distance, and returning a list with tuples of
        (poem_id, poet_id, euclidean_distance), sorted by best to worst match.
        """

        micro_lex = self._get_micro_lex_data()
        sentiment = self._get_sentiment_data()
        context = self._get_context_data()

        if self.poem:
            raw_words = Metrics._clean_word_list(self.poem.text)
        else:
            raw_words = Metrics._clean_word_list(self.text)

        word_list = [w for w in raw_words if w.isalpha()]

        matches = []
        for o_metrics in other_metrics:

            compare_dict = self._get_criteria(other_metric_obj=o_metrics,
                                              micro_lex=micro_lex,
                                              sentiment=sentiment,
                                              word_list=word_list,
                                              context=context)

            euc_dist, euc_raw = self._get_euc_distance(comparison_dict=compare_dict,
                                                       conwgt=conwgt,
                                                       micwgt=micwgt,
                                                       sentwgt=sentwgt,
                                                       macwgt=macwgt)

            matches.append((o_metrics.poem_id,
                            o_metrics.poem.poet_id,
                            euc_dist,
                            euc_raw))

        # we sort by euclidian distance, smallest (i.e. best match to largest)
        distance_idx = 2
        sorted_matches = sorted(matches, key=lambda tup: tup[distance_idx])

        return sorted_matches

    @staticmethod
    def _get_euc_raw(list_one, list_two, weight):
        """ takes 2 lists of #s their weight(percent as 0.xx), returns float.

        The square root of this float is float (without the weight put in) would
        be the euclidean distance between the two objects (list1 and list 2). we
        weight this number to allow for different catagories to take priority in
        our final calculatuation, which will be the sqrt of the sum of all the
        floats this function returns. We'll be finding matching poems based on
        the smalled euclidean distance.

                >>> list_one =[5, 6, 7, 2]
                >>> list_two = [3, 2, 8, 1]
                >>> weight = 0.5
                >>> Metrics._get_euc_raw(list_one, list_two, weight)
                11.0

        All of our numbers, however, will be between 0 and 1:

                >>> list_one = [0.5, 0.23, 0.34]
                >>> list_two = [0.4, 0.35, 0.21]
                >>> weight = 0.60
                >>> Metrics._get_euc_raw(list_one, list_two, weight)
                0.024779999999999996

        This function is called within Metrics.find_matches and will not need
        to be used directly.
        """
        temp_total = 0.0
        for i in range(len(list_one)):
            temp_total += ((list_one[i] - list_two[i]) ** 2)

        return temp_total * weight

    @staticmethod
    def _get_word_compare(word_list, other):
        """returns the percentage of words from self in other

        called my Metrics._calc_matches_ which is in turn caled by
        Metrics.find_matches, and will not need to be called directly.
        """

        raw_other_words = Metrics._clean_word_list(other.poem.text)
        other_words = [w for w in raw_other_words if w.isalpha()]

        percent_shared_one = Metrics._get_percent_in(word_list, other_words)
        percent_shared_two = Metrics._get_percent_in(other_words, word_list)

        return (percent_shared_one, percent_shared_two)

    def _create_context_lists(self, other_poem, context):
        """Returns list w/ [percent shared context data], [ideal]

        ideal is just a list with 1 corresponding to each percentage in
        percent shared context data -- 1 is the ideal, because that is the
        result we would receive if they shared all the same data.
        """

        raw_context = self._get_context_compare(other=other_poem,
                                                self_context=context)
        context = []
        o_context = []

        if raw_context["sub_per"]:
            context.append(raw_context["sub_per"])
            o_context.append(1)
        if raw_context["term_per"]:
            context.append(raw_context["term_per"])
            o_context.append(1)
        if raw_context["reg_per"]:
            context.append(raw_context["reg_per"])
            o_context.append(1)

        return [context, o_context]

    def _get_context_compare(self, other, self_context):
        """"returns a dictionary containing percentage shared context data

        this method is called by Metrics._create_context_lists, which is in turn
        called by other methods as part of finding maching poems -- it will not
        need to be called directly.
        """

        other_context = other._get_context_data()

        reg_per = None
        term_per = None
        sub_per = None

        regions = self_context["regions"]
        other_regions = other_context["regions"]

        if regions and other_regions:
            reg_per = Metrics._get_percent_in(regions, other_regions)

        terms = self_context["terms"]
        other_terms = other_context["terms"]

        if terms and other_terms:
            term_per = Metrics._get_percent_in(terms, other_terms)

        subs = self_context["subjects"]
        other_subs = other_context["subjects"]

        if subs and other_subs:
            sub_per = Metrics._get_percent_in(subs, other_subs)

        return {"reg_per": reg_per, "term_per": term_per, "sub_per": sub_per}

    @staticmethod
    def difference_percent(x, y):
        """ returns the difference between x and y as a percentage of x.

            >>> Metrics.difference_percent(100, 110)
            0.1

            >>> Metrics.difference_percent(110, 100)
            0.09090909090909091

            >>> Metrics.difference_percent(10, 0)
            0


        this method is called by Metrics._get_macro_compare and will not need
        to be called directly.
        """

        if y == 0 or x == 0:
            return 0
        else:
            x = float(x)
            return abs(x - y) / x

    def _get_macro_compare(self, other):
        """"returns tuple with [closeness of macro data], [ideal]

        This function is called by Metrics._calc_matches_ and will not need to
        be called directly. Ideal is 1 for each item, since that is what
        we would receive if they had the same value.
        """

        self_macro = self._get_macro_lex_data()
        other_macro = other._get_macro_lex_data()

        macro_compare = map(Metrics.difference_percent, self_macro, other_macro)
        macro_compare.extend(map(Metrics.difference_percent, other_macro, self_macro))

        ideal = [0.0 for item in macro_compare]

        return (macro_compare, ideal)

    def _get_context_data(self):
        """Returns a list w/ nested lists w/ context data for a poem"""

        subjects = set(self.subjects)
        terms = set(self.terms)
        regions = set(self.regions)

        return {"regions": regions, "terms": terms,
                "subjects": subjects}

    def _get_macro_lex_data(self):
        """Returns a list of macro lexical data for a given poem

                >>> fake = Metrics(poem_id=0,\
                                   wl_mean=1,\
                                   wl_mode=2,\
                                   wl_range=4,\
                                   wl_mode=3,\
                                   ll_mean=5,\
                                   ll_mode=6,\
                                   ll_range=8,\
                                   pl_lines=10)
                >>>
                >>> fake._get_macro_lex_data()
                [1, 2, 4, 3, 5, 6, 8, 10]

        This function is called in Metrics.find_matches and will not need to be
        used directly."""

        macro_lex = [self.wl_mean, self.wl_mode, self.wl_range, self.ll_mean,
                     self.ll_mode, self.ll_range, self.pl_lines]

        return macro_lex

    def _get_micro_lex_data(self):
        """Returns a list of micro lexical data for a given poem

                >>> fake = Metrics(poem_id=0,\
                                   the_freq=1,\
                                   i_freq=2,\
                                   you_freq=3,\
                                   is_freq=4,\
                                   a_freq=5,\
                                   alliteration=6,\
                                   rhyme=7,\
                                   lex_div=8,
                                   end_repeat=9)
                >>>
                >>> fake._get_micro_lex_data()
                [1, 2, 3, 4, 5, 6, 7, 8, 9]

        This function is called in Metrics.find_matches and will not need to be
        used directly.
        """

        micro_lex = [self.the_freq, self.i_freq, self.you_freq, self.is_freq,
                     self.a_freq, self.alliteration, self.rhyme, self.lex_div,
                     self.end_repeat]

        return micro_lex

    def _get_sentiment_data(self):
        """Returns a list of sentiment data for a given poem

                >>> fake = Metrics(poem_id=0,\
                                   common_percent=1,\
                                   poem_percent=2,\
                                   object_percent=3,\
                                   abs_percent=4,\
                                   male_percent=5,\
                                   female_percent=6,\
                                   positive=7,\
                                   negative=8,\
                                   active_percent=9,\
                                   passive_percent=10)
                >>>
                >>> fake._get_sentiment_data()
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        This function is called in Metrics.find_matches and will not need to be
        used directly.
        """

        sentiment_data = [self.common_percent, self.poem_percent,
                          self.object_percent, self.abs_percent,
                          self.male_percent, self.female_percent,
                          self.positive, self.negative, self.active_percent,
                          self.passive_percent]
        return sentiment_data

    @classmethod
    def get_metrics(cls, poem_id):
        """given poem id, returns instance of Metrics class w/data calculated"""

        text_set = (db.session.query(Poem.text)
                      .filter(Poem.poem_id == poem_id).first())

        if not text_set:
            print "There is no poem at this ID"
            return None

        text = text_set[0]

        word_list = cls._clean_word_list(text)
        line_dict = cls._get_clean_line_data(text)

        wl_data = cls._get_wl_data(word_list)

        wl_mean = wl_data["wl_mean"]
        wl_median = wl_data["wl_median"]
        wl_mode = wl_data["wl_mode"]
        wl_range = wl_data["wl_range"]
        pl_words = wl_data["pl_words"]
        lex_div = wl_data["lex_div"]

        ll_data = cls._get_ll_data(line_dict)

        ll_mean = ll_data["ll_mean"]
        ll_median = ll_data["ll_median"]
        ll_mode = ll_data["ll_mode"]
        ll_range = ll_data["ll_range"]
        pl_lines = ll_data["pl_lines"]
        pl_char = ll_data["pl_char"]

        sl_data = cls._get_stanza_data(line_dict)

        stanzas = sl_data["stanzas"]
        sl_mean = sl_data["sl_mean"]
        sl_median = sl_data["sl_median"]
        sl_mode = sl_data["sl_mode"]
        sl_range = sl_data["sl_range"]

        freq_data = cls._get_freq_data(word_list)

        i_freq = freq_data["i_freq"]
        you_freq = freq_data["you_freq"]
        the_freq = freq_data["the_freq"]
        is_freq = freq_data["is_freq"]
        a_freq = freq_data["a_freq"]

        alliteration = cls._get_alliteration_score(line_dict)
        rhyme = cls._get_rhyme_score(line_dict)
        end_repeat = cls._get_end_rep_score(line_dict)

        common_percent = cls._get_percent_out(word_list, COMMON_W)
        poem_percent = cls._get_percent_out(word_list, POEM_W)
        object_percent = cls._get_percent_in(word_list, OBJECTS)
        abs_percent = cls._get_percent_in(word_list, ABSTRACT)
        male_percent = cls._get_percent_in(word_list, MALE)
        female_percent = cls._get_percent_in(word_list, FEMALE)
        active_percent = cls._get_percent_in(word_list, ACTIVE)
        passive_percent = cls._get_percent_in(word_list, PASSIVE)
        positive = cls._get_percent_in(word_list, POSITIVE)
        negative = cls._get_percent_in(word_list, NEGATIVE)

        data = cls(poem_id=poem_id, wl_mean=wl_mean, wl_median=wl_median,
                   wl_mode=wl_mode, wl_range=wl_range, ll_mean=ll_mean,
                   ll_median=ll_median, ll_mode=ll_mode, ll_range=ll_range,
                   pl_char=pl_char, pl_lines=pl_lines, pl_words=pl_words,
                   lex_div=lex_div, i_freq=i_freq, you_freq=you_freq,
                   the_freq=the_freq, is_freq=is_freq, a_freq=a_freq,
                   common_percent=common_percent, poem_percent=poem_percent,
                   object_percent=object_percent, abs_percent=abs_percent,
                   male_percent=male_percent, female_percent=female_percent,
                   active_percent=active_percent, stanzas=stanzas,
                   passive_percent=passive_percent, sl_range=sl_range,
                   positive=positive, negative=negative, sl_mode=sl_mode,
                   alliteration=alliteration, rhyme=rhyme, sl_mean=sl_mean,
                   sl_median=sl_median, end_repeat=end_repeat)

        return data

    @staticmethod
    def _get_wl_data(word_list):
        """given a list of words, returns float data about words as dict.

        Specifically, given the list of all the words in a poem, returns a dict
        with the mean word length (wl_mean), the median word length (wl_median),
        the mode word length (wl_mode), the range of word lengths (wl_range),
        the total number of words (num_words), and the lexical diversity
        (lex_div), which is the number of unique words in the poem divided
        by the total number of words.

            >>> word_list = ['This', 'is', 'a', 'sample', 'word', 'list', '.',\
                             'Imagine', 'this', 'list', 'is', 'more', 'poetic',\
                             'than', 'it', 'is', 'in', 'reality', ',', 'please',\
                             '.']
            >>> wl_data = Metrics._get_wl_data(word_list)
            >>> expected = {'wl_mode': 4.0, 'wl_range': 6, 'wl_median': 4,\
                            'pl_words': 21, 'wl_mean': 3,\
                            'lex_div': 0.8095238095238095}
            >>> wl_data == expected
            True

        This function is called by Poem.parse, and will not need to be used
        directly."""

        words = [word for word in word_list if word.isalpha]
        num_words = len(words)
        lengths = sorted([len(word) for word in words])

        wl_range = max(lengths) - min(lengths)
        wl_mean = sum(lengths) / num_words
        wl_median = Metrics._get_median(lengths)
        wl_mode = Metrics._get_mode(lengths)

        unique = set(word_list)
        lex_div = len(unique) / float(num_words)

        return {"wl_mean": wl_mean, "wl_median": wl_median, "wl_mode": wl_mode,
                "wl_range": wl_range, "pl_words": num_words, "lex_div": lex_div}

    @staticmethod
    def _get_clean_line_data(text):
        """takes string, returns dict w/["all_lines"]=all lines,"no_breaks"]=only lines w/ content

                >>> text = 'Here is some sample text!\\nIt can be difficult to'\
                           + ' think of good sample text...\\n\\n yellow dog boat?'
                >>> line_data = Metrics._get_clean_line_data(text)
                >>> results = {'all_lines': ['Here is some sample text!',\
                                             'It can be difficult to think of'\
                                             + ' good sample text...',\
                                             '',\
                                             'yellow dog boat?'],\
                               'no_breaks': ['Here is some sample text!',\
                                             'It can be difficult to think of'\
                                             + ' good sample text...',\
                                             'yellow dog boat?']}
                >>> line_data == results
                True

        This function is called within Metrics.get_metrics and will not need
        to be used directly.
        """

        line_list = text.split("\n")
        clean_lines = [l.strip() for l in line_list]
        just_lines = [line for line in clean_lines if len(line) > 0]

        return {"all_lines": clean_lines, "no_breaks": just_lines}

    @staticmethod
    def _get_median(list_of_numbers):
        """given a list of numbers, returns the median as a float

                >>> numbers = [5, 5, 10, 0]
                >>> Metrics._get_median(numbers)
                5

        if given an empty list, will return 0:
                >>> numbers = []
                >>> Metrics._get_median(numbers)
                0

        This function is called within Metrics._get_stanza_data,
        Metrics._get_ll_data, and Metrics._get_wl_data which are in turn called
        by Metrics.get_metrics -- it will not need to be used directly.
        """
        if list_of_numbers:
            length = len(list_of_numbers)
            list_of_numbers = sorted(list_of_numbers)
            if length == 2:
                median = sum(list_of_numbers) / 2
            elif length % 2 == 0:
                median = (list_of_numbers[length / 2]
                          + list_of_numbers[(length / 2) - 1]) / 2
            else:
                median = list_of_numbers[length / 2]
        else:
            median = 0

        return median

    @staticmethod
    def _get_mode(list_of_numbers):
        """Given a list of numbers, returns the mode as a float.

            >>> numbers = [1, 2, 6, 3, 2]
            >>> Metrics._get_mode(numbers)
            2.0

        If all number occur the same number of times, it will give the highest
        number in the list:

            >>> numbers = [1, 2, 3, 5]
            >>> Metrics._get_mode(numbers)
            5.0

        if two numbers occur equally frequently, it will give the highest of
        the two:

            >>> numbers = [1, 3, 1, 5, 2, 5]
            >>> Metrics._get_mode(numbers)
            5.0

        if fed an empty list, will return 0:

            >>> numbers = []
            >>> Metrics._get_mode(numbers)
            0.0

        This function is called within Metrics._get_stanza_data,
        Metrics._get_ll_data, and Metrics._get_wl_data which are in turn called
        by Metrics.get_metrics -- it will not need to be used directly.
        """
        if list_of_numbers:
            num_dict = {}
            for num in list_of_numbers:
                num_dict[num] = num_dict.get(num, 0) + 1

            mode_list = []
            maximum = max(num_dict.values())
            for num in num_dict:
                if num_dict[num] == maximum:
                    mode_list.append(float(num))

            mode = max(mode_list)
        else:
            mode = 0.0

        return mode

    @staticmethod
    def _get_stanza_data(line_dict):
        """returns dict w/ stanza data (floats) for string list as value for
        ["all_lines"] in line_data dict.

                >>> line_dict = {'all_lines': ['Here is some sample text!',\
                                               'It can be difficult to think\
                                               of good sample text...',\
                                               '',\
                                               'yellow dog boat?']}
                >>> stanza_data = Metrics._get_stanza_data(line_dict)
                >>> expected = {'sl_median': 1.0, 'sl_mean': 1.5,\
                                'stanzas': 2.0, 'sl_mode': 2.0, 'sl_range': 1.0}
                >>> stanza_data == expected
                True

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        all_lines = line_dict["all_lines"]
        stanzas = 0
        stanza_lengths = []
        stanza_length = 0
        for line in all_lines:
            if len(line) != 0:
                stanza_length += 1
            else:
                stanzas += 1
                stanza_lengths.append(stanza_length)
                stanza_length = 0
        if stanza_length > 0:
            stanza_lengths.append(stanza_length)
            stanzas += 1

        stanzas = float(stanzas)
        sl_mean = sum(stanza_lengths) / stanzas
        sl_range = float(max(stanza_lengths)) - min(stanza_lengths)
        sl_median = float(Metrics._get_median(stanza_lengths))
        sl_mode = float(Metrics._get_mode(stanza_lengths))

        return {"stanzas": stanzas, "sl_mean": sl_mean, "sl_median": sl_median,
                "sl_mode": sl_mode, "sl_range": sl_range}

    @staticmethod
    def _get_ll_data(line_dict):
        """returns dict w/ line data (floats) for string list as value for
        ["no_breaks"] in line_dict.

                >>> ldict = {'no_breaks': ['Here is some sample text!',\
                                           'It can be difficult to think of ' +\
                                           'good sample text...',\
                                           'yellow dog boat?']}
                >>> line_data = Metrics._get_ll_data(ldict)
                >>> expected = {'ll_median': 25.0, 'pl_lines': 3,\
                                'll_mode': 51.0, 'pl_char': 92.0,\
                                'll_mean': 30.666666666666668,\
                                'll_range': 35.0}
                >>> line_data == expected
                True

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        lengths = sorted([float(len(l)) for l in line_dict["no_breaks"]])

        num_lines = len(lengths)  # the same as len(line_data["no_breaks"])
        ll_range = (max(lengths)) - min(lengths)
        ll_mean = sum(lengths) / num_lines
        ll_median = Metrics._get_median(lengths)
        ll_mode = Metrics._get_mode(lengths)
        pl_char = sum(lengths)

        return {"ll_mean": ll_mean, "ll_median": ll_median, "ll_mode": ll_mode,
                "ll_range": ll_range, "pl_lines": num_lines, "pl_char": pl_char
                }

    @staticmethod
    def _get_freq_data(word_list):
        """returns a dict with fequency data for a given list of words

        i_freq is the number of times "i" occurs on it's own (i.e. not as part
            of another word) as a percentage of overall words in the poem.
        you_freq is the number of times "you" occurs on it's own as a percentage
            of overall words in the poem.
        the_freq, is_freq, and a_freq follow the same model, but for "the",
            "is", and "a" respectively.

            >>> x = ['this', 'is', 'a', 'sample', 'text', '.', 'normally',\
                     'this', 'would', 'come', 'from', 'a', 'poem', '.',\
                     'but', 'i', 'am', 'feeding', 'this', 'in', 'to',\
                     'test', 'the', 'function', '.']
            >>> freq_data = Metrics._get_freq_data(x)
            >>> expected = {"i_freq": 0.045454545454545456,\
                            "you_freq": 0.0,\
                            "the_freq": 0.045454545454545456,\
                            "is_freq": 0.045454545454545456,\
                            "a_freq": 0.09090909090909091}
            >>> freq_data == expected
            True

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

        return {"i_freq": i_freq, "you_freq": you_freq, "the_freq": the_freq,
                "is_freq": is_freq, "a_freq": a_freq}

    @staticmethod
    def _clean_word_list(text):
        """returns a list of lowercase words and puncuation for a given text

            >>> text = '\\t\\t\\t Here is some odd sample text: '\
                       + '\\n\\n I    like to eat cake.'
            >>> clean_list = Metrics._clean_word_list(text)
            >>> expected = ['here', 'is', 'some', 'odd', 'sample', 'text', ':',\
                            'i', 'like', 'to', 'eat', 'cake', '.']
            >>> clean_list == expected
            True

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
        data_word_list = set(data_word_list)

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
        data_word_list = set(data_word_list)
        for word in poem_word_list:
            if word not in data_word_list:
                count += 1
        return float(count)/float(total)

    @staticmethod
    def _get_alliteration_score(line_dict):
        """given a text, returns alliteration score as a float

        >>> ldict = {'no_breaks': ['Here is some sample text to savor!',\
                                   'I hope you have a healthy and happy day!']}
        >>> Metrics._get_alliteration_score(ldict)
        0.6428571428571429

        alternatively if we have not alliteration:

        >>> ldict = {'no_breaks': ['Here you will find sample text.',\
                                   'No alliteration present.']}
        >>> Metrics._get_alliteration_score(ldict)
        0.0

        Alliteration score is incremented every time multiple words in the
        same line start with the same letter. Final score is the alliteration
        count divided by the overall number of words in the poem
        """

        lines = line_dict["no_breaks"]
        allit_count = 0
        total = 0

        for line in lines:
            used_letters = []

            words = [w for w in Metrics._clean_word_list(line) if w.isalpha()]
            long_words = [w for w in words if len(w) > 1]

            first_letters = [w for w in words if len(w) == 1]
            first_letters = [w[0] for w in long_words if w[1] != "h"]
            first_letters.extend([w[0:2] for w in long_words if w[1] == "h"])

            total += len(first_letters)

            for let in first_letters:
                if let not in used_letters:
                    used_letters.append(let)
                    count = first_letters.count(let)
                    if count > 1:
                        allit_count += count

        return allit_count / float(total)

    @staticmethod
    def _backup_rhyme_list(word):
        """uses the Words API to get rhyming words

        this is a backup for Writer Mode, to be used if the rhymer server goes
        down or blocks scraping.

            >>> rhymes = Metrics._backup_rhyme_list("apple")
            >>> expected = set([u'funeral chapel', u'side chapel', u'mayapple',\
                                u'grapple', u'pineapple', u'dapple',\
                                u'scrapple', u'chapel'])
            >>> rhymes == expected
            True

        This method is called by _get_rhyme_list in the event of an error, and
        will not need to be used directly. It requires a the the api key
        to be loaded to the environment, or else will return an empty set.
        """
        print "GONE TO WORDS API"
        return set()

        # key = environ['WORDS_PRODUCTION_KEY']
        # url = 'https://wordsapiv1.p.mashape.com/words/' + word + '/rhymes?mashape-key=' + key
        # rhyme_data = get(url)

        # print "Using Words API"  # Prints to the server for debugging purposes

        # if rhyme_data.status_code == 200:
        #     results = rhyme_data.json()
        #     rhyming_words = []
        #     try:
        #         rhyming_words.extend(results["rhymes"]["verb"])
        #     except KeyError:
        #         pass
        #     try:
        #         rhyming_words.extend(results["rhymes"]["all"])
        #         # all does not actually include all rhyming words
        #     except KeyError:
        #         pass
        #     try:
        #         rhyming_words.extend(results["rhymes"]["noun"])
        #     except KeyError:
        #         pass

        #     return set(rhyming_words)
        # else:
        #     return set()

    @staticmethod
    def _get_rhyme_list(word):
        """ given word, returns set of rhyming words

        Scrapes rhyming words from www.rhymezone.com, controls for appropriate
        values and returns the set.

            >>> rhymes = Metrics._get_rhyme_list("orange")
            >>> results = set(['sponge', 'plunge', 'expunge', 'challenge',\
                               'muskellunge', 'lunge', 'lozenge', 'scavenge'])
            >>> rhymes == results
            True

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        word = word.strip()
        BEG_URL = 'http://www.rhymer.com/RhymingDictionary/'
        FIN_URL = '.html'
        url = BEG_URL + word + FIN_URL
        try:
            html_text = get(url).text
        except:
            return Metrics._backup_rhyme_list(word)

        soup = BeautifulSoup(html_text, "html.parser")
        words = soup.find_all("td")
        rough_word_list = [unidecode(w.text).strip() for w in words]
        word_list = [w for w in rough_word_list
                     if len(w) > 0 and '(' not in w and w != word]

        return set(word_list)

    @staticmethod
    def _get_end_words(line_dict):
        """given a string, returns all a list of words at the end of each line

            >>> ldict = {'no_breaks': ['hello how are you', 'I am fine thanks',\
                                       'are you fine too']}
            >>> end_words = Metrics._get_end_words(ldict)
            >>> end_words
            ['you', 'thanks', 'too']

        will cut off punction and return all words lowercase:

            >>> ldict = {'no_breaks': ['here is some sample TEXT!',\
                                       'it is GREAT?']}
            >>> Metrics._get_end_words(ldict)
            ['text', 'great']

        called by Metrics._get_rhyme_score, which in turn is called within
        Metrics.get_metrics, and will not need to be used directly.
        """
        lines = line_dict["no_breaks"]
        end_words = []
        for line in lines:
            words = Metrics._clean_word_list(line)
            words = [w.lower() for w in words if w.isalpha()]
            if words:
                last_word = words[-1]
                end_words.append(last_word)

        return [w.lower() for w in end_words]

    @staticmethod
    def _get_rhyme_score(line_dict):
        """given a text, returns rhyme score as an integer

                >>> ldict = {'no_breaks': ['Here is some sample text!',\
                                           'This is good sample Text?',\
                                           'Who know what will happen next?']}
                >>> Metrics._get_rhyme_score(ldict)
                0.6666666666666666

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        end_words = Metrics._get_end_words(line_dict)
        total = float(len(end_words))
        rhymes = []
        for word in end_words:
            other_words = set([w for w in end_words if w != word])
            rhyme_words = set(Metrics._get_rhyme_list(word))
            rhymes.extend(w for w in other_words if w in rhyme_words)

        rhymes = set(rhymes)
        return len(rhymes)/total

    @staticmethod
    def _get_end_rep_score(line_dict):
        """given a text, returns the unique line endings / total line endings

                >>> ldict = {'no_breaks': ['Here is some sample text!',\
                                           'This is good sample Text!',\
                                           'Who know what will happen next?']}
                >>> Metrics._get_end_rep_score(ldict)
                0.3333333333333333

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        end_words = Metrics._get_end_words(line_dict)
        end_length = len(end_words)
        repeats = end_length - len(set(end_words))
        return repeats / float(end_length)

    @staticmethod
    def _get_average_data(list_of_means, list_of_medians, list_of_modes, set_max=None):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        labels = []
        if set_max:
            for i in range(set_max):
                labels.append(float(i))
        else:
            for i in range(int(max(list_of_means) + 1)):
                labels.append(float(i))

        mean_count = []
        median_count = []
        mode_count = []

        for l in labels:
            mean_count.append(list_of_means.count(l))
            median_count.append(list_of_medians.count(l))
            mode_count.append(list_of_modes.count(l))

        data = {"labels": labels,
                "mean": mean_count,
                "median": median_count,
                "mode": mode_count}

        return data

    @staticmethod
    def _get_range_data(list_of_numbers, set_max=None):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        labels = []
        if set_max:
            for i in range(set_max):
                labels.append(float(i))
        else:
            for i in range(int(max(list_of_numbers) + 1)):
                labels.append(float(i))

        range_count = []

        for l in labels:
            range_count.append(list_of_numbers.count(l))

        data = {"labels": labels,
                "range": range_count}

        return data

    @staticmethod
    def _get_percent_data(first_list_of_nums, second_list_of_nums=None, third_list_of_nums=None, set_max=None):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        nums = [0.000, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.175, 0.200,
                0.225, 0.250, 0.275, 0.300, 0.325, 0.350, 0.375, 0.400, 0.425,
                0.450, 0.475, 0.500, 0.525, 0.550, 0.575, 0.600, 0.625, 0.650,
                0.675, 0.700, 0.725, 0.750, 0.775, 0.800, 0.825, 0.850, 0.875,
                0.900, 0.925, 0.950, 0.975, 1.000]
        if set_max:
            nums = [n for n in nums if n <= set_max]

        labels = []
        first_range_count = []
        second_range_count = []
        third_range_count = []

        for i in range(len(nums) - 1):
            num1 = nums[i]
            num2 = nums[i + 1]

            label = str(num1) + " -- " + str(num2)
            labels.append(label)

            count1 = [n for n in first_list_of_nums if n >= num1 and n < num2]
            first_range_count.append(len(count1))
            if second_list_of_nums:
                count2 = [n for n in second_list_of_nums if n >= num1 and n < num2]
                second_range_count.append(len(count2))
            if third_list_of_nums:
                count3 = [n for n in third_list_of_nums if n >= num1 and n < num2]
                third_range_count.append(len(count3))

        if all([first_range_count, second_range_count, third_range_count]):
            data = {"labels": labels,
                    "first": first_range_count,
                    "second": second_range_count,
                    "third": third_range_count}
        elif first_range_count and second_range_count:
            data = {"labels": labels,
                    "first": first_range_count,
                    "second": second_range_count}
        else:
            data = {"labels": labels,
                    "first": first_range_count}

        return data

    @staticmethod
    def _get_small_percent_data(first_list_of_nums, second_list_of_nums=None, third_list_of_nums=None, set_max=None):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        nums = [0.000, 0.010, 0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080,
                0.090, 0.100, 0.110, 0.120, 0.130, 0.140, 0.150, 0.160, 0.170,
                0.180, 0.190, 0.200, 0.210, 0.220, 0.230, 0.240, 0.250, 0.260,
                0.270, 0.280, 0.290, 0.300, 0.310, 0.320, 0.330, 0.340, 0.350,
                0.360, 0.370, 0.380, 0.390, 0.400, 0.410, 0.420, 0.430, 0.440,
                0.450, 0.460, 0.470, 0.480, 0.490, 0.500]

        if set_max:
            if set_max <= 0.2:
                nums = [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035,
                        0.040, 0.045, 0.050, 0.055, 0.060, 0.065, 0.070, 0.075,
                        0.080, 0.085, 0.090, 0.095, 0.100, 0.105, 0.110, 0.115,
                        0.120, 0.125, 0.130, 0.135, 0.140, 0.145, 0.150, 0.155,
                        0.160, 0.165, 0.170, 0.175, 0.180, 0.185, 0.190, 0.195,
                        0.200]

            nums = [n for n in nums if n <= set_max]

        labels = []
        first_range_count = []
        second_range_count = []
        third_range_count = []

        for i in range(len(nums) - 1):
            num1 = nums[i]
            num2 = nums[i + 1]

            label = str(num1) + " -- " + str(num2)
            labels.append(label)

            count1 = [n for n in first_list_of_nums if n >= num1 and n < num2]
            first_range_count.append(len(count1))
            if second_list_of_nums:
                count2 = [n for n in second_list_of_nums if n >= num1 and n < num2]
                second_range_count.append(len(count2))
            if third_list_of_nums:
                count3 = [n for n in third_list_of_nums if n >= num1 and n < num2]
                third_range_count.append(len(count3))

        if all([first_range_count, second_range_count, third_range_count]):
            data = {"labels": labels,
                    "first": first_range_count,
                    "second": second_range_count,
                    "third": third_range_count}
        elif first_range_count and second_range_count:
            data = {"labels": labels,
                    "first": first_range_count,
                    "second": second_range_count}
        else:
            data = {"labels": labels,
                    "first": first_range_count}

        return data

    @staticmethod
    def get_obj_abs_data(metrics_obj_list):
        obj = [m.object_percent for m in metrics_obj_list]
        abst = [m.abs_percent for m in metrics_obj_list]

        return Metrics._get_small_percent_data(first_list_of_nums=obj,
                                               second_list_of_nums=abst,
                                               set_max=0.3)

    @staticmethod
    def get_common_data(metrics_obj_list):
        standard = [m.common_percent for m in metrics_obj_list]
        specific = [m.poem_percent for m in metrics_obj_list]

        return Metrics._get_percent_data(first_list_of_nums=standard,
                                         second_list_of_nums=specific)

    @staticmethod
    def get_gender_data(metrics_obj_list):
        male = [m.male_percent for m in metrics_obj_list]
        female = [m.female_percent for m in metrics_obj_list]

        return Metrics._get_small_percent_data(first_list_of_nums=male,
                                               second_list_of_nums=female,
                                               set_max=0.2)

    @staticmethod
    def get_active_data(metrics_obj_list):
        active = [m.active_percent for m in metrics_obj_list]
        passive = [m.passive_percent for m in metrics_obj_list]

        return Metrics._get_small_percent_data(first_list_of_nums=active,
                                               second_list_of_nums=passive,
                                               set_max=0.3)

    @staticmethod
    def get_pos_neg_data(metrics_obj_list):
        pos = [m.positive for m in metrics_obj_list]
        neg = [m.negative for m in metrics_obj_list]

        return Metrics._get_small_percent_data(first_list_of_nums=pos,
                                               second_list_of_nums=neg,
                                               set_max=0.3)

    @staticmethod
    def get_rhyme_rep_data(metrics_obj_list):
        rhyme = [m.rhyme for m in metrics_obj_list]
        end_repeat = [m.end_repeat for m in metrics_obj_list]

        return Metrics._get_percent_data(first_list_of_nums=rhyme,
                                         second_list_of_nums=end_repeat)

    @staticmethod
    def get_lex_data(metrics_obj_list):
        lex_div = [m.lex_div for m in metrics_obj_list]

        return Metrics._get_percent_data(first_list_of_nums=lex_div)

    @staticmethod
    def get_filler_data(metrics_obj_list):
        the_freq = [m.the_freq for m in metrics_obj_list]
        a_freq = [m.a_freq for m in metrics_obj_list]
        is_freq = [m.is_freq for m in metrics_obj_list]

        return Metrics._get_small_percent_data(first_list_of_nums=the_freq,
                                               second_list_of_nums=a_freq,
                                               third_list_of_nums=is_freq,
                                               set_max=0.3)

    @staticmethod
    def get_narrator_data(metrics_obj_list):
        i_freq = [m.i_freq for m in metrics_obj_list]
        you_freq = [m.you_freq for m in metrics_obj_list]

        return Metrics._get_small_percent_data(i_freq, you_freq, set_max=0.3)

    @staticmethod
    def get_alliteration_data(metrics_obj_list):
        alliteration = [m.alliteration for m in metrics_obj_list]

        return Metrics._get_percent_data(alliteration)

    @staticmethod
    def get_wl_average_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        wl_mean = [m.wl_mean for m in metrics_obj_list]
        wl_median = [m.wl_median for m in metrics_obj_list]
        wl_mode = [m.wl_median for m in metrics_obj_list]

        return Metrics._get_average_data(list_of_means=wl_mean,
                                         list_of_medians=wl_median,
                                         list_of_modes=wl_mode, set_max=8)

    @staticmethod
    def get_wl_range_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        wl_range = [m.wl_range for m in metrics_obj_list]

        return Metrics._get_range_data(list_of_numbers=wl_range, set_max=26)

    @staticmethod
    def get_pl_words_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        pl_words = [m.pl_words for m in metrics_obj_list]

        return Metrics._get_grouped_range(list_of_numbers=pl_words,
                                          set_max=2000, range_num=25)

    @staticmethod
    def get_pl_lines_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        pl_lines = [m.pl_lines for m in metrics_obj_list]

        return Metrics._get_range_data(list_of_numbers=pl_lines, set_max=101)

    @staticmethod
    def _get_grouped_range(list_of_numbers, set_max, range_num):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        labels = []
        range_count = []
        for i in range(0, set_max - range_num, range_num):

            label = str(i) + " -- " + str(i + range_num)
            labels.append(label)
            range_list = [n for n in list_of_numbers
                          if n >= i and n < (i + range_num)]
            range_count.append(len(range_list))

        data = {"labels": labels,
                "range": range_count}

        return data

    @staticmethod
    def get_pl_char_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        pl_char = [m.pl_char for m in metrics_obj_list]

        return Metrics._get_grouped_range(list_of_numbers=pl_char,
                                          set_max=3000, range_num=40)

    @staticmethod
    def get_ll_average_data(metrics_obj_list):
        """returns a dict w/ lists of of line length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        ll_mean = [m.ll_mean for m in metrics_obj_list]
        ll_median = [m.ll_median for m in metrics_obj_list]
        ll_mode = [m.ll_median for m in metrics_obj_list]

        return Metrics._get_average_data(list_of_means=ll_mean,
                                         list_of_medians=ll_median,
                                         list_of_modes=ll_mode, set_max=86)

    @staticmethod
    def get_ll_range_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        ll_range = [m.ll_range for m in metrics_obj_list]

        return Metrics._get_range_data(list_of_numbers=ll_range, set_max=101)

    @staticmethod
    def get_stanza_length_data(metrics_obj_list):
        """returns a dict w/ lists of of line length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """

        sl_mean = [m.sl_mean for m in metrics_obj_list]
        sl_median = [m.sl_median for m in metrics_obj_list]
        sl_mode = [m.sl_median for m in metrics_obj_list]

        return Metrics._get_average_data(list_of_means=sl_mean,
                                         list_of_medians=sl_median,
                                         list_of_modes=sl_mode,
                                         set_max=66)

    @staticmethod
    def get_stanza_range_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        sl_range = [m.sl_range for m in metrics_obj_list]

        return Metrics._get_range_data(list_of_numbers=sl_range, set_max=51)

    @staticmethod
    def get_stanza_num_data(metrics_obj_list):
        """returns a dict w/ lists of of word length average data

        called by server.py and fed through to Chart.js to make a graph of
        the spread of our wl_mean, wl_median, and wl_mode values.
        """
        stanzas = [m.stanzas for m in metrics_obj_list]

        return Metrics._get_range_data(list_of_numbers=stanzas, set_max=76)

    @staticmethod
    def get_single_graph_data(metrics_list, name_of_context, name, metrics_backref):
        """"""

        connected_items = {}

        for met in metrics_list:
            others = getattr(met, metrics_backref)
            if len(others) > 1:
                for o in others:
                    context_name = getattr(o, name_of_context)
                    if context_name != name:
                        connected_items[context_name] = connected_items.get(context_name, 0) + 1
            else:
                only = "Only " + name
                connected_items[only] = connected_items.get(only, 0) + 1

        return connected_items.items()

    @staticmethod
    def get_context_graph_data(list_of_context_obj, name_of_context, metrics_backref):
        """"""
        final_data = []

        for item in list_of_context_obj:
            name = getattr(item, name_of_context)

            iden = name.replace(".", "").replace("-", "").replace("/", "").replace(",", "").split(" ")
            if iden[0].lower() != "the":
                iden = iden[0]
            else:
                iden = iden[1]

            metrics = item.metrics
            total = len(metrics)

            connected_items = {}

            for met in metrics:
                others = getattr(met, metrics_backref)
                if len(others) > 1:
                    for o in others:
                        context_name = getattr(o, name_of_context)
                        if context_name != name:
                            connected_items[context_name] = connected_items.get(context_name, 0) + 1
                else:
                    only = "Only " + name
                    connected_items[only] = connected_items.get(only, 0) + 1

            data = {"name": name,
                    "total": total,
                    "iden": iden,
                    "others": connected_items.items()}

            final_data.append(data)

        return final_data


class BestMatch(db.Model):
    """ records instance of best match selected by user """

    __tablename__ = "best_matches"

    pm_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    primary_poem_id = db.Column(db.Integer,
                                db.ForeignKey('poems.poem_id'))
    match_poem_id = db.Column(db.Integer,
                              db.ForeignKey('poems.poem_id'),
                              nullable=False)
    euc_distance = db.Column(db.Float,
                             nullable=False)
    page_order = db.Column(db.Integer)
    match_index = db.Column(db.Integer)
    method_code = db.Column(db.String(10),
                            db.ForeignKey('methods.method_code'),
                            nullable=False)

    poem = db.relationship("Poem", backref="best_matches", foreign_keys="BestMatch.primary_poem_id")
    match = db.relationship("Poem", backref="best_matched_for", foreign_keys="BestMatch.match_poem_id")
    method = db.relationship("Method", backref="best_matches")


class Method(db.Model):
    """variations on the algorithm weighing the catagories differently"""

    __tablename__ = "methods"

    method_code = db.Column(db.String(10), primary_key=True, nullable=False)
    description = db.Column(db.Text)
    macro = db.Column(db.Float, nullable=False)
    micro = db.Column(db.Float, nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    context = db.Column(db.Float)


class UserMetrics(Metrics):

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.poem_id = None
        self.poet_id = None
        self.get_metrics()

    def get_metrics(self):
        """calculates metrics data and stores it on the UserMetrics instance"""

        word_list = Metrics._clean_word_list(self.text)
        line_dict = Metrics._get_clean_line_data(self.text)

        wl_data = Metrics._get_wl_data(word_list)

        self.wl_mean = wl_data["wl_mean"]
        self.wl_median = wl_data["wl_median"]
        self.wl_mode = wl_data["wl_mode"]
        self.wl_range = wl_data["wl_range"]
        self.lex_div = wl_data["lex_div"]
        self.pl_words = wl_data["pl_words"]

        ll_data = Metrics._get_ll_data(line_dict)

        self.ll_mean = ll_data["ll_mean"]
        self.ll_median = ll_data["ll_median"]
        self.ll_mode = ll_data["ll_mode"]
        self.ll_range = ll_data["ll_range"]
        self.pl_lines = ll_data["pl_lines"]
        self.pl_char = ll_data["pl_char"]

        freq_data = Metrics._get_freq_data(word_list)

        self.i_freq = freq_data["i_freq"]
        self.you_freq = freq_data["you_freq"]
        self.the_freq = freq_data["the_freq"]
        self.is_freq = freq_data["is_freq"]
        self.a_freq = freq_data["a_freq"]

        sl_data = Metrics._get_stanza_data(line_dict)

        self.stanzas = sl_data["stanzas"]
        self.sl_mean = sl_data["sl_mean"]
        self.sl_median = sl_data["sl_median"]
        self.sl_mode = sl_data["sl_mode"]
        self.sl_range = sl_data["sl_range"]

        self.alliteration = Metrics._get_alliteration_score(line_dict)
        self.rhyme = Metrics._get_rhyme_score(line_dict)
        self.end_repeat = Metrics._get_end_rep_score(line_dict)

        self.common_percent = Metrics._get_percent_out(word_list, COMMON_W)
        self.poem_percent = Metrics._get_percent_out(word_list, POEM_W)
        self.object_percent = Metrics._get_percent_in(word_list, OBJECTS)
        self.abs_percent = Metrics._get_percent_in(word_list, ABSTRACT)
        self.male_percent = Metrics._get_percent_in(word_list, MALE)
        self.female_percent = Metrics._get_percent_in(word_list, FEMALE)
        self.active_percent = Metrics._get_percent_in(word_list, ACTIVE)
        self.passive_percent = Metrics._get_percent_in(word_list, PASSIVE)
        self.positive = Metrics._get_percent_in(word_list, POSITIVE)
        self.negative = Metrics._get_percent_in(word_list, NEGATIVE)


#HELPER FUNCTIONS
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poetry.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print "Connected to DB."
