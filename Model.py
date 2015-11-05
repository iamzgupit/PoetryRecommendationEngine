from flask_sqlalchemy import SQLAlchemy
from unidecode import unidecode
from bs4 import BeautifulSoup
from word_lists import (COMMON_W, POEM_W, ABSTRACT, OBJECTS, MALE, FEMALE,
                        ACTIVE, PASSIVE, POSITIVE, NEGATIVE)
from requests import get

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

#FIXME: NO DOCTEST
    @staticmethod
    def create_search_params():
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

            >>> class Fake(object):
            ...    __init___(self, text):
            ...        self.text = text
            >>>
            >>> a = Fake("here \r is \t\t some fake text    ")
            >>> b = Fake("and some more.")
            >>> fake_list = [a, b]
            >>> Metrics._clean_listobj(fake_list)
            ['this', 'is', 'some', 'fake', 'text', 'and', 'some', 'more', '.']

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
        >>> Poem._get_text(html_string)
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
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

#FIXME: NO DOCTEST
    @staticmethod
    def _set_context(soup_object, poem_id):
        rough_context = soup_object.find_all("p", class_="section")
        context = Poem._clean_listobj(rough_context)

        Poem._set_regions(context, poem_id)
        Poem._set_terms(context, poem_id)
        Poem._set_subjects(context, poem_id)

#FIXME: NO DOCTEST
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
    pl_char = db.Column(db.Float)
    pl_lines = db.Column(db.Float)
    pl_words = db.Column(db.Float)
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
    end_repeat = db.Column(db.Float) # NEEDS TO BE INTEGRATED
    rhyme = db.Column(db.Float)
    stanzas = db.Column(db.Float)
    sl_mean = db.Column(db.Float)
    sl_median = db.Column(db.Float)
    sl_mode = db.Column(db.Float)
    sl_range = db.Column(db.Float)

    poem = db.relationship('Poem', backref='metrics')

#FIXME INCOMPLETE AND NO DOCTEST
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

#FIXME NO DOCTEST
    def get_context_data(self):
        """Returns a list with nested lists with context data for a poem"""

        poem = self.poem
        subjects = [sub.subject for sub in poem.subjects]
        terms = [term.term for term in poem.terms]
        regions = [region.region for region in poem.regions]
        poet_birth = poem.poet.birth_year

        return [poet_birth, regions, terms, subjects]

#FIXME NO DOCTEST
    def get_macro_lex_data(self):
        """Returns a list of macro lexical data for a poem"""

        macro_lex = [self.wl_mean, self.wl_median, self.wl_mode,
                     self.wl_range, self.ll_mean, self.ll_median,
                     self.ll_mode, self.ll_range, self.pl_char,
                     self.pl_lines, self.pl_words, self.lex_div]
        return macro_lex

#FIXME NO DOCTEST
    def get_micro_lex_data(self):
        """Returns a list of micro lexical data for a poem"""

        micro_lex = [self.the_freq, self.i_freq, self.you_freq, self.end_repeat,
                     self.is_freq, self.a_freq, self.alliteration, self.rhyme,
                     self.end_repeat]

        return micro_lex

#FIXME NO DOCTEST
    def get_sentiment_data(self):
        """Returns a list of sentiment data for a poem"""

        sentiment_data = [self.common_percent, self.poem_percent,
                          self.object_percent, self.abs_percent,
                          self.male_percent, self.female_percent,
                          self.positive, self.negative, self.active_percent,
                          self.passive_percent]
        return sentiment_data

#FIXME NO DOCTEST
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

            >>> word_list = ['This', 'is', 'a', 'sample', 'word', 'list', '.',
                             'Imagine', 'this', 'list', 'is', 'more', 'poetic',
                             'than', 'it', 'is', 'in', 'reality', ',', 'please',
                             '.']
            >>> wl_data = Poem._get_wl_data(word_list)
            >>> expected = {"wl_mean": 3, "wl_median": 4, "wl_mode": 4,
                            "wl_range": 6, "pl_words": 21,
                            "lex_div": 0.8333333333333334}
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

                >>> text = "Here is some sample text! \n It can be difficult to\
                 think of good sample text...\n\n yellow dog boat?"
                >>> line_data = Metrics._get_clean_line_data(text)
                >>> results = {'all_lines': ['Here is some sample text!',
                                             'It can be difficult to think of \
                                             good sample text...',
                                             '',
                                             'yellow dog boat?'],
                               'no_breaks': ['Here is some sample text!',
                                             'It can be difficult to think of \
                                             good sample text...',
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
            2

        If all number occur the same number of times, it will give the highest
        number in the list:

            >>> numbers = [1, 2, 3, 5]
            >> Metrics._get_mode(numbers)
            5

        if two numbers occur equally frequently, it will give the highest of
        the two:

            >>> numbers = [1, 3, 1, 5, 2, 5]
            >>> Metrics._get_mode(numbers)
            5

        if fed an empty list, will return 0:

            >>> numbers = []
            >>> Metrics._get_mode(numbers)
            0

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
            mode = 0

        return mode

    @staticmethod
    def _get_stanza_data(line_dict):
        """returns dict w/ stanza data (floats) for string list as value for
        ["all_lines"] in line_data dict.

                >>> line_dict = {'all_lines': ['Here is some sample text!',
                                               'It can be difficult to think \
                                               of good sample text...',
                                               '',
                                               'yellow dog boat?']}
                >>> stanza_data = Metrics._get_stanza_data(line_dict)
                >>> expected = {'sl_median': 1.0, 'sl_mean': 1.5,
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

                >>> line_dict = {'no_breaks': ['Here is some sample text!',
                                              'It can be difficult to think of \
                                              good sample text...',
                                              'yellow dog boat?']}
                >>> line_data = Metrics._get_ll_data(line_dict)
                >>> expected = {'ll_median': 25.0, 'pl_lines': 3,
                                'll_mode': 51.0, 'pl_char': 92.0,
                                'll_mean': 30.666666666666668,
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

            >>> x = ['this', 'is', 'a', 'sample', 'text', '.', 'normally',
                     'this', 'would', 'come', 'from', 'a', 'poem', '.',
                     'but', 'i', 'am', 'feeding', 'this', 'in', 'to',
                     'test', 'the', 'function', '.']
            >>> freq_data = Metrics._get_freq_data(x)
            >>> expected = {"i_freq": 0.045454545454545456,
            ...             "you_freq": 0.0,
            ...             "the_freq": 0.045454545454545456,
            ...             "is_freq": 0.045454545454545456,
            ...             "a_freq": 0.09090909090909091}
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
    def _get_alliteration_score(line_dict):
        """given a text, returns alliteration score as a float

        >>> text = "Here is some sample text to savor! \n I hope you have a \
                    healthy and happy day!"
        >>> Metrics._get_alliteration_score(text)
        0.6428571428571429

        alternatively if we have not alliteration:

        >>> text = "Here you will find sample text. \n No alliteration present."
        >>> Metrics._get_alliteration_score(text)
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
    def _get_rhyme_list(word):
        """ given word, returns set of rhyming words

        Scrapes rhyming words from www.rhymezone.com, controls for appropriate
        values and returns the set.

            >>> rhymes = Metrics._get_rhyme_list("tester")
            >>> results = set(['fester', 'fresher', 'leicester', 'professor',
                               'semester', 'taster', 'nester', 'mister',
                               'connector', 'lessor', 'molester', 'pester',
                               'better', 'checker', 'ester', 'sequester',
                               'nestor', 'ever', 'dresser', 'pepper', 'esther',
                               'bold', 'refresher', 'fiesta', 'jester', 'testa',
                               'pressure', 'western', 'letter', 'trimester',
                               'investor', 'feather', 'nectar', 'director',
                               'polyester', 'buster', 'wrecker', 'sylvester',
                               'wester', 'lesser', 'chester', 'enter',
                               'webster', 'protector', 'temper', 'gesture'])
            >>> rhymes == results
            True

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        word = word.strip()
        BEG_URL = "http://www.rhymezone.com/r/rhyme.cgi?Word="
        FIN_URL = "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
        url = BEG_URL + word + FIN_URL
        html_text = get(url).text
        soup = BeautifulSoup(html_text, "html.parser")
        words = soup.find_all("b")
        rough_word_list = [unidecode(w.text).strip() for w in words]
        word_list = [w for w in rough_word_list
                     if "[" not in w
                     and len(w) < 10
                     and w != word]

        return set(word_list)

    @staticmethod
    def _get_end_words(line_dict):
        """given a string, returns all a list of words at the end of each line

            >>> text = "hello how are you \n\nI am fine thanks\nare you fine too"
            >>> end_words = Metrics._get_end_words(text)
            >>> end_words
            ['you', 'thanks', 'too']

        will cut off punction and return all words lowercase:

            >>> text = "here is some more sample Text! \n\n it is GREAT?"
            >>> end_words = Metrics._get_end_words(text)
            >>> end_words
            ['text', 'great']

        called by Metrics._get_rhyme_score, which in turn is called within
        Metrics.get_metrics, and will not need to be used directly.
        """
        lines = line_dict["no_breaks"]
        end_words = []
        for line in lines:
            words = Metrics._clean_word_list(line)
            words = [w.lower() for w in words if w.isalpha]
            if words:
                last_word = words[-1]
                end_words.append(last_word)

        return [w.lower() for w in end_words]

    @staticmethod
    def _get_rhyme_score(line_dict):
        """given a text, returns rhyme score as an integer
                >>> text = "Here is some sample text!\n\n \
                            This is good sample Text!\n\nWho know what \
                            will happen next?"
                >>> Metrics._get_end_rhyme_score(text)
                0.6666666666666666
        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        end_words = Metrics._get_end_words(line_dict)
        total = float(len(end_words))
        rhymes = 0
        for word in end_words:
            other_words = [w for w in end_words if w != word]
            rhyme_words = Metrics._get_rhyme_list(word)
            for word in other_words:
                if word in rhyme_words:
                    rhymes += 1

        return rhymes/total

    @staticmethod
    def _get_end_rep_score(line_dict):
        """given a text, returns the unique line endings / total line endings

                >>> text = "Here is some sample text!\n\n \
                            This is good sample Text!\n\nWho know what \
                            will happen next?"
                >>> Metrics._get_end_rep_score(text)
                0.6666666666666666

        This function is called by Metrics.get_metrics and will not need to be
        used directly.
        """

        end_words = Metrics._get_end_words(line_dict)
        unique = set(end_words)
        return len(unique) / float(len(end_words))


#FIXME: HOW DO I DEFINE THIS RELATIONSHIP SINCE IT LINKS TO POEMS TWICE
class PoemMatch(db.Model):
    """ connects poem to its matches """

    __tablename__ = "poem_matches"

    pm_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    primary_poem_id = db.Column(db.Integer,
                                db.ForeignKey('poems.poem_id'),
                                nullable=False)
    match_poem_id = db.Column(db.Integer,
                              db.ForeignKey('poems.poem_id'),
                              nullable=False)
    match_percent = db.Column(db.Float,
                              nullable=False)

    # poem = db.relationship("Poem", backref="matches")
    # matches = db.relationship("Poem", backref="matched_to")


#HELPER FUNCTIONS
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poetry.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__" or __name__ == "__console__":
    from server import app

    connect_to_db(app)
    print "Connected to DB."
