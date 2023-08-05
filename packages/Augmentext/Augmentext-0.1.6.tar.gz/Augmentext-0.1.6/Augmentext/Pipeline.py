# Pipeline.py
# Main user-interface functionality is defined here.
# Author: Marcus D. Bloice <https://github.com/mdbloice> and contributors
# Licensed under the terms of the MIT Licence.

import string
import random
from textblob import TextBlob
import re

# Internal imports
from .Operations import ICDToText, ICDFromText, MeSH, ReplaceNumbers
from .Operations import ReplaceWordsWithNumbers, SNOMED, SwapWords
from .Operations import Misspeller, Operation
from .TextOperations import TextLoader

TYPES = ["character", "word", "sentence", "paragraph", "document", "corpus"]


class Pipeline(object):
    def __init__(self, path, extension='txt') -> None:

        super().__init__()

        self.textloader = TextLoader()
        self.textloader.load_from_directory(path, extension=extension)
        self.operations = []

    def sample(self, n, type="sentence"):
        """
        Sample *n* number of documents/words/sentences from the current
        pipeline, specified by the :attr:`type`.

        :param n:
        :param type:
        :return:
        """

        if len(self.operations) <= 0:
            raise Exception("Current pipeline does not have any operations.")

        if type == "sentence":
            pass
        elif type == "paragraph":
            pass
        else:
            raise Exception("Cannot understand '%s'. The 'type' parameter must be one of: %s." % (type, ', '.join(TYPES)))

        samples_generated = 0
        samples = []

        while samples_generated < n:
            r_document = random.randint(0, len(self.textloader.corpus.documents)-1)
            r_sentence = random.randint(0, len(self.textloader.corpus.documents[r_document].sentences)-1)

            text = self.textloader.corpus.documents[r_document].sentences[r_sentence]

            if len(self.operations) <= 0:
                raise Exception("Cannot sample without any operations.")
            else:
                for operation in self.operations:
                    if random.random() <= operation.probability:
                        text = operation.perform_operation(text)

            samples.append(text)
            samples_generated += 1

            # print("Sample " + str(samples_generated) + ":\n" + text + "\n---")
        return samples

    def generator(self, type):
        """
        Returns a generator which will sample indefinitely from the pipeline,
        as long as it is called.

        :param type:
        :return:
        """

        return 0

    def add_operation(self, operation):
        """
        Adds an operation to the current pipeline.

        Must be of type :class:`~Augmentext.Operations.Operation` in order
        to function correctly with the :class:`~Augmentext.Pipeline.Pipeline`.

        :param type: An :class:`~Augmentext.Operations.Operation` object.
        :return: None
        """

        # Check if the operation has inherited from the Operation class
        # as is required to work with the pipeline.
        # Because an object can have multiple parent classes, we check
        # if the any of the parent classes are of type Operation by checking
        # against everything in the __bases__ list.
        if Operation in operation.__class__.__bases__:
            if 0.0 < operation.probability <= 1.0:
                self.operations.append(operation)
            else:
                raise Exception("The probability parameter must be > 0 and <= 1")
        else:
            raise Exception("The operation must have a parent type Operation.")

    def _levenshtein_distance(self, s, t):
        """
        Calculate the Levenshtein distance between two strings.

        .. warning:: This implementation is a recursive method which is very
         slow.

        :param s: The first string
        :param t: The second string
        :return: The Levenshtein distance
        """

        # TODO: This is a recursive method found online. Change.
        if s == "":
            return len(t)
        if t == "":
            return len(s)
        if s[-1] == t[-1]:
            cost = 0
        else:
            cost = 1

        distance = min([self._levenshtein_distance(s[:-1], t) + 1,
                        self._levenshtein_distance(s, t[:-1]) + 1,
                        self._levenshtein_distance(s[:-1], t[:-1]) + cost])

        return distance

    def add_swap_word_list(self, swap_words):
        """
        Adds a swap word list, supplied as a dictionary, to the current
        pipeline that is used by various functions when randomly replacing
        words.

        :param swap_words: A dictionary of swap words to be used for functions
         such as :func:`swap_random_words`
        :return: None
        """

        if len(swap_words) != 0:
            self.swap_words = swap_words

        return 0

    def add_regular_expressions(self, regex_list):
        """
        Add a list of regex terms to use in replacement functions, such as unit
        converters (see for example :func:`convert_units`) or more general
        pattern matching functions.

        :param regex_list:
        :return: None
        """

        return 0

    def swap_random_words(self, probability):
        """
        Swap the order of two random words in a string.
        """
        self.operations.append(SwapWords(probability=probability))

    def swap_random_characters(self, probability):
        """
        Randomly swap two neighbouring characters within one word, chosen
        randomly.

        :param probability: Controls the probability that the operation
          will be performed when passed through the pipeline.
        :return: None
        """

        self.operations.append(SwapWords(probability=probability))

    def snomed_synonym_swap(self, probability):
        """
        Search a string for words and replace those found in SNOMED-CT with
        one of its synonyms.
        """

        self.operations.append(SNOMED(probability=probability))

    def icd_to_text(self, probability):
        """
        Search ICD for text strings, and replace them with ICD codes.
        """

        self.operations.append(ICDToText(probability=probability))

    def icd_from_text(self, probability):
        """
        Search strings for ICD codes, and replace them with text from ICD-10.
        """

        self.operations.append(ICDFromText(probability=probability))

    def misspell_random_word(self, probability, aggressive=True):
        """
        Misspell a random word in a text string.
        """
        self.operations.append(Misspeller(probability=probability, aggressive=aggressive))

    def auto_abbreviate(self, probability, words_per_sentence):
        """
        Abbreviates words according to heuristics.

        :param probability:
        :param words_per_sentence:
        :return: None
        """

        return 0

    def mesh_synonyms(self, probability):
        """
        Use MeSH to swap out words with synonyms.

        MeSH can be downloaded from here:

        https://www.nlm.nih.gov/databases/download/mesh.html

        Place your MeSH files in the following directory:

        ~/.augmentext/mesh/

        Augmentext requires the d2021.bin file for example.

        """
        self.operations.append(MeSH(probability=probability))

    def word2vec_synonyms(self, probability):

        pass


    def abbreviate(self, probability, abbreviation_list):
        """
        Abbreviate words according to the passed :attr:`abbreviation_list`.

        :param probability:
        :param abbreviation_list:
        :return:
        """

    def expand_abbreviations(self, probability):
        """
        Use a probabilistic model to expand abbreviations.

        See https://stackoverflow.com/q/43510778 for a discussion.

        :param probability:
        :return: None
        """

        return 0

    def convert_units(self, probability):
        """
        Convert units that match regex pattern matches. Regular expressions can
        be user-defined or use Augmentext defaults.

        :param probability:
        :return: None
        """

        return 0

    def to_upper(self, probability=1.0):
        """
        Convert all text to upper case.

        The :attr:`probability` parameter defaults to 1.0 for this function.

        :param probability:
        :return:
        """

        return 0

    def to_lower(self, probability=1.0):
        """
        Convert all text to lower case.

        The :attr:`probability` parameter defaults to 1.0 for this function.

        :param probability:
        :return:
        """

        return 0

    def convert_words_to_numbers(self, probability):
        """
        Replace written numbers, from 0 to 19 to digit numbers, e.g. will
        convert ZERO/NIL to 0, ONE to 1, FOURTEEN to 14, and so on.

        :param probability:
        :return:
        """

        return 0

    def convert_numbers_to_words(self, probability, replace_all_integers=False):
        """
        Replace **whole** numbers 0 to 19 with words.

        :param probability:
        :return:
        """

        test_str = "here is some text 3 with some numbers 5 in there 9."

        # Use re to find digits and replace them with nothing.
        return re.sub(r'\d+', '', test_str)

    def remove_units(self, probability, user_defined=None):
        """
        Remove the units from text, if found. This can help to make a model
        generalise better by making it more robust to missing units, for
        example.

        Will search for the following:

        mg
        dL
        etc.
        """

        if user_defined is None:
            print("Call with default list.")
        else:
            print("Call with user defined list.")

        pass

    def remove_numbers(self, probability, from_num, to_num):
        """
        Remove all numbers from a text.

        This can help a model to generalise better by making it more robust
        to missing values or data.

        """

        pass

    def remove_random_word(self, probability):
        """
        Remove a random word from a text as it is being passed through the
        pipeline.
        """
        pass

    def replace_numbers(self, probability):
        """
        Replace all numbers in the specified range (:attr:`from_number` to
        :attr:`to_number` inclusive) with a character defined by
        :attr:`replace_with`.

        :return: None
        """

        self.operations.append(ReplaceNumbers(probability=probability))

    def replace_written_numbers(self, probability):
        """
        Replace occurances of written text, such as "nine", "eighteen",
        "seventy-four" and so on with their numeric equivalents.

        By default, replaces the numbers zero to ninety-nine.
        """

        self.operations.append(ReplaceWordsWithNumbers(probability=probability))

    def remove_punctuation(self, probability, punctuation_stop_words=None):
        """
        Removes common punctuation from text that passes this function in a
        pipeline.

        :param probability:
        :return:
        """

        test_string = "Here, in this string (encoded) are some [5] common chars."

        test_string.translate(str.maketrans('', '', string.punctuation))

        return 0

    def strip_whitespace(self, probability=1.0):
        """
        Strips whitespace from text.

        :param probability:
        :return:
        """

        test_string = " some text    "

        return test_string.strip()

    def remove_stop_words(self, probability):
        """
        Removes stop words.

        Options to do this include NLTK or SciKit Learn::

            from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

        There are options for other languages.

        NTLK looks as follows::

            from nltk.tokenize import word_tokenize
            tokens = word_tokenize(input_str)
            result = [i for i in tokens if not i in stop_words]

        Which returns a list of words.

        :param probability:
        :return:
        """

        return 0

    def stem_words(self, probability):
        """
        Replaces words with their stem.

        The NLTK library allows this to be done easily::

            from nltk.stem import PorterStemmer
            from nltk.tokenize import word_tokenize
            stemmer= PorterStemmer()
            input_str="There are several types of stemming algorithms."
            input_str=word_tokenize(input_str)
            for word in input_str:
                print(stemmer.stem(word))

        The output is as follows::

            There are sever type of stem algorithm.

        Note:

        Stemming is a process of reducing words to their word stem,
        base or root form. The main two algorithms are Porter stemming
        algorithm (removes common morphological and inflexional endings from
        words) and Lancaster stemming algorithm (a more aggressive stemming
        algorithm).

        Stemming does not use lexical knowledge bases for this task! Use
        lemmatisation for this task.

        :param probability:
        :return:
        """

        return 0

    def lemmatise(self, probability):
        """
        Lemmatise the words in the current context.

        With NTLK this is done as follows::

            from nltk.stem import WordNetLemmatizer
            from nltk.tokenize import word_tokenize
            lemmatizer=WordNetLemmatizer()
            input_str="been had done languages cities mice"
            input_str=word_tokenize(input_str)
            for word in input_str:
                print(lemmatizer.lemmatize(word))

        This differs from stemming, as explained in the :func:`stem_words`
        function.

        :param probability:
        :return:
        """

        return 0

    def remove_frequent_words(self, probability):
        """
        Remove frequent words from text passing through this function in the
        pipeline.

        This will require a processing phase when first called.

        :param probability:
        :return:
        """

        # Compute frequent words for current corpus here
        # When learning phase is over continue with adding to pipeline.

        return 0

    def remove_rare_words(self, probability):
        """
        Remove rare words from any text passing through this function in the
        pipeline.

        This will require a processing learning phase when first called.

        :param probability:
        :return:
        """

        return 0

    def spell_correct(self, probability):
        """
        Automatically correct spelling for text passing through this function.

        Uses TextBlob for this functionality. This is rather slow from my
        testing so far.

        TextBlob offers some advanced techniques, and leverages NLTK. It has a
        number of text corpora that can be used as the basis for statistical
        spelling correction.

        Peter Norvig has a discussion on spell correct here:
        https://norvig.com/spell-correct.html

        :param probability:
        :return:
        """

        t = "apendix"
        t_corrected = TextBlob.correct(t)
        # Output is: TextBlob("appendix")

        return t_corrected.string


class Corpus(object):
    def __init__(self, documents, paragraphs, sentences, words, characters):
        """
        This class represents the Corpus data structure. All Operation
        classes in the :attr:`Augmentext.Operations` module accepts a `Corpus`
        object.

        A corpus is the top level definition of a bunch of text.

        - Corpus
        - Document
        - Paragraph
        - Sentence
        - Word
        - Character

        We must make it possible to import text and define these levels.

        """
        print("Init of Corpus class.")

        # Getters and setters will be handled internally by Python
        # member variable access.
        self.documents = documents
        self.paragraphs = paragraphs
        self.sentences = sentences
        self.words = words
        self.characters = characters

    def document_count(self):
        return len(self.documents)

    def paragraph_count(self):
        return len(self.paragraphs)

    def sentence_count(self):
        return len(self.sentences)

    def word_count(self):
        return len(self.words)

    def character_count(self):
        return len(self.characters)

    def summary(self):
        """
        Return a summary of the corpus. This may change if properties are
        altered by other methods, such as methods that remove stop words, or
        other data of this type.

        :return: A summary of the current corpus.
        """

        summary_text = "some text"

        return summary_text
