# Feature extraction module which may be used for simple operations such as
# extracting the number of words in the corpus, generating sparse matrices,
# and so on.

# Python 2/3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

# Imports
from textblob import TextBlob


class GenerateSparseMatrix(object):
    def __init__(self):
        pass

    def generate(self):
        """
        Returns a sparse matrix for the current corpus.

        :return: The sparse matrix.
        """
        return 0


def average_word_length(corpus):
    """
    Return the average word length for the corpus passed.
    :return:
    """

    corpus.length

    return 0


def text_contains_number(corpus):

    return 0


def text_begins_with_capital_letter(corpus):

    return 0


def number_of_words(corpus):

    return 0


def number_of_characters(corpus):

    return 0


def number_of_stopwords(corpus):

    return 0


def number_of_special_characters(corpus):

    return 0


def number_of_numerical_items(corpus):

    return 0


def translate_word(corpus):
    """
    Use TextBlob to translate words that are detected as not belonging to the
    corpus language into the corpus language.

    .. code::

        from textblob import TextBlob
        text = TextBlob("appendix")
        translated = text.translate(from_lang='en', to="de")
        # Returns: TextBlob("Blinddarm")

    TextBlob can be used to detect the language of the entire document:

    .. code::

        text.detect_language()
        # Returns: 'en'

    Many languages are supported, e.g. Arabic:

    .. code::

        text.translate(from_lang='en', to="ar")
        # Returns: TextBlob("الملحق")

    Which outputs الملحق

    :param corpus: The corpus to translate.
    :return: The translated corpus.
    """

    text_snippet = "appendix"
    from_language = text_snippet.detect_language()  # Returns 'en'
    translated = text_snippet.translate(from_lang=from_language, to="de")  # Returns TextBlob("Blinddarm")

    return translated.string


def n_grams(corpus):

    return 0


def term_frequency(corpus):
    """
    Term frequency is simply the ratio of the count of a word present in a sentence, to the length of the sentence.

    Therefore, we can generalize term frequency as:

    .. math::

        \\text{TF} = \\frac{t_N}{n}

    TF = (Number of times term T appears in the particular row) / (number of terms in that row)

    :param corpus:
    :return:
    """
    return 0


def inverse_document_frequency(corpus):
    """
    The inverse document frequency, IDF, of a word is the log of the ratio
    of the total number of rows to the number of rows in which that word is
    present.

    The inverse document frequency is defined as:

    .. math::

        \\text{IDF} = log\\Big(\\frac{N}{n}\\Big)

    Where :math:`N` is the number of rows and :math:`n` is the number of rows
    where the word is present.

    :param corpus: The corpus to analyse.
    :return: The inverse document frequency.
    """
    return 0


def term_frequency_inverse_document_frequency(corpus):
    """
    The Term Frequency-Inverse Document Frequency (TF-IDF) is the TF times the
    IDF:

    .. math::

        \\text{TF-IDF} = \\text{TF(t,d)} \\times \\text{IDF}(t)

    :param corpus:
    :return:
    """
    return 0


def bag_of_words(corpus):
    """
    Bag of words can be calculated using SciKit Learn's `CountVectorizer`:

    .. code::

        from sklearn.feature_extraction.text import CountVectorizer
        BOW = CountVectorizer(max_features=1000, lowercase=True, ngram_range=(1,1),analyzer = "word")
        BOW.fit_transform(train['tweet'])

    :param corpus: The corpus of text to analyse.
    :return: The bag of words.
    """
    return 0


def sentiment_analysis(corpus):

    return 0


def word_embedding(corpus):

    return 0
