"""Utilites for convering yivo -> ycode"""
import importlib.resources as pkg_resources
from . import tables

def read_nonphonetic():
    """Reads table of non-phonetic words

    The input file consists of two columns. The first is the phonetic yivo
    and the second is the ycode equivalent.

    The yivo and Hebrew ycode may include hyphens

    Returns
    =======
    yivo2hebrew: string -> string
        key: yivo word
        vall: corresponding ycode word
    """
    with pkg_resources.open_text(tables, 'nonphonetic_yivo2ycode.txt') as fin:
        lines = fin.readlines()
    lines = [line.rstrip() for line in lines]
    lines = [line.split('\t') for line in lines
             if line and not line.startswith(';;')]
    yivo2hebrew = {yivo.strip():hebrew.strip() for
                   (yivo, hebrew) in lines}
    return yivo2hebrew

def read_yivo2ycode_table():
    """Reads table for yivo to ycode transliteration

    Each line has either 2 or 3 columns
    If 2 columns, they are:
    (0) yivo_char - one character in a yivo string
    (1) ycode_chars - string of 1 or 2 characters that's the ycode equivalent

    If 3 columns, they are:
    (0) yivo_chars - 2 or 2 character sequence that an appear in a yivo string
    (1) ordinal of unicode char that won't appear in a ycode string
    (2) ycode equivalent of yivo_chars

    The idea is that the yivo_chars in the 3 column rows consist of
    characters that could be individually translated incorrectly, and so
    the subsequence is first converted to something else to get them out
    of the way, and then converted back after the single-character conversions.

    Returns
    =======
    yivo2ycode_1: dict string -> string
        key: yivo_char
        val: ycode_char
    yivo2ycode_2: list of 3-tuples (string, char, string)
        yivo_chars
        tmp character
        ycode_chars
    """
    with pkg_resources.open_text(tables, 'yivo-ycode.txt') as fin:
        lines = fin.readlines()

    lines = [line.rstrip() for line in lines]
    lines = [line.split('\t') for line in lines
             if line and not line.startswith(';;')]

    simple = [line for line in lines
              if len(line) == 2]
    complex_ = [line for line in lines
                if len(line) == 3]

    yivo_chars = [line[0].strip() for line in simple]
    ycode_chars = [line[1].strip() for line in simple]
    for yivo_char in yivo_chars:
        assert len(yivo_char) == 1, f'bad yivo_char {yivo_char}'
    yivo2ycode_1 = {yivo_char: ycode_char
                    for (yivo_char, ycode_char) in zip(yivo_chars, ycode_chars)
                    if len(yivo_char) == 1}

    yivo2ycode_2 = [(yivo_cluster, chr(int(tmp)), ycode_cluster)
                    for (yivo_cluster, tmp, ycode_cluster) in complex_]

    return (yivo2ycode_1, yivo2ycode_2)

class TransliteratorYivo:
    """Handles transliteration of yivo -> ycode"""
    def __init__(self):
        (self.yivo2ycode_1, self.yivo2ycode_2) = read_yivo2ycode_table()
        self.yivo2hebrew = read_nonphonetic()

    def yivo2ycode(self, yivo_text, use_nonphonetic=True):
        """Convert string in yivo transliteration to ycode

        (0) First removes ~ which is assumed to not occur in yivo
        #TODO: take care of this in calling code
        (1) checks for misc. special cases
        (2) check if Hebew word. This includes words that don't have
        a hyphen, or words that do have a hyphen and are in the Hebrew listing
        that way
        (3) splits on hyphen, and does calls yivo2ycode_single on the individual parts -
        or if no hyphen, just on the word
        """
        # (0)
        yivo_text = yivo_text.replace('~', '')
        # (1)
        if yivo_text in ('-', '--', '---', '----'):
            return yivo_text

        if yivo_text == '%EXCL%':
            return '!'

        # could do a more principled check for what surrounds the apostrophe
        # but easier to just check for particular cases
        if yivo_text == "s'iz":
            return "s'Ayz"
        if yivo_text == "s'i'":
            return "s'Ay'"
        if yivo_text == "i'":
            return "Ay'"

        # (2)
        if use_nonphonetic and yivo_text in self.yivo2hebrew:
            return self.yivo2hebrew[yivo_text]

        # (3)
        yivo_words = yivo_text.split("-")
        # some words seem to end in a hyphen, so there could be an empty word
        if len(yivo_words) == 1:
            ycode = self.yivo2ycode_single(yivo_text)
            return ycode
        ycode_words = [self.yivo2ycode_single(yivo_word)
                       for yivo_word in yivo_words
                       if yivo_word]
        ycode = "-".join(ycode_words)
        return ycode

    def yivo2ycode_single(self, yivo_text):
        """Convert text in yivo transliteration to ycode

        (0) checks if yivo_text in non-phonetic dict. If so, uses that
        (1) converts multi-character sequences to temporary values
        (2) converts single characters to ycode
        (3) converts temporary values to ycode
        (4) fix up final letter if it has a final form
        (5) add shtumer alef if necessary
        """
        # (0)
        if yivo_text in self.yivo2hebrew:
            return self.yivo2hebrew[yivo_text]

        # hack for internal i after oys, etc.
        if yivo_text.startswith('oysi'):
            yivo_text = 'oysAi' + yivo_text[4:]
        elif yivo_text.startswith('oysgei'):
            yivo_text = 'oysgeAi' + yivo_text[6:]
        

        # (1)
        for (yivo_cluster, tmp, ycode_cluster) in self.yivo2ycode_2:
            yivo_text = yivo_text.replace(yivo_cluster, tmp)

        # (2)
        ycode_text = ''
        for chr1 in yivo_text:
            if  chr1 in self.yivo2ycode_1:
                ycode_text += self.yivo2ycode_1[chr1]
            else:
                ycode_text += chr1

        # (3)
        for (yivo_cluster, tmp, ycode_cluster) in self.yivo2ycode_2:
            ycode_text = ycode_text.replace(tmp, ycode_cluster)

        # (4)
        chr1 = ycode_text[-1]
        if chr1 in 'xmnfq':
            chr1u = chr1.upper()
            ycode_text = ycode_text[:-1] + chr1u

        # (5)
        # going from yivo to ycode, the ambiguity around whether
        # y and v are vowels are consonants is resolved.
        # don't really need to check ycode0 but keeping it for clarity
        # WY is vov yud, so gets A before
        # Y is yud yud, so gets A before
        # keeping it for clarity for now
        ycode0 = ycode_text[0]
        yivo0 = yivo_text[0]
        if ((ycode0 == 'y' and yivo0 == 'i') or
            (ycode0 == 'v' and yivo0 == 'u') or
            ycode0 in 'WY'):
            ycode_text = 'A' + ycode_text

        return ycode_text
