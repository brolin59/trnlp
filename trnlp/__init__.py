from trnlp.word_processing import *
from trnlp.helpers import *
from trnlp.Morphological.MorphologicalLR import ClsEkBul as Ceb
from trnlp.Statistic.TextStatistic import Statistic as Stat
from trnlp.Tokenization.SentenceTokenization import token, word_tokenize, tr_word_tokenize, sentence_token_wsign, \
    sentence_token
from trnlp.file_processing import *


def deascii(str_grp: str):
    from trnlp.Asciidecoder.Asciidecoder import Deasciifier
    return Deasciifier(str_grp).convert_to_turkish()


def find_suffix(word: str):
    return Ceb(word).result


def find_stems(word: str):
    return Ceb(word).stems


def unknown_words(str_grp: str):
    return tr_word_tokenize(str_grp)[1]


def view_statistic(str_grp: str):
    return Stat(str_grp).text_statistic()


def ntow(number: str):
    from trnlp.helpers import number_to_word
    return number_to_word(number)


def wton(word: str):
    from trnlp.helpers import word_to_number
    return word_to_number(word)
