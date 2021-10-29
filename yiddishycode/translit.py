import importlib.resources as pkg_resources
from . import tables

COMBINATIONS = [
    # b + a + dagesh = B + a
    # normalization puts these in the wrong order
    # needs to go before b+dagesh so that the inverse
    # transformation will do this first
    ('ba@', 'Ba'),
    ('bo@', 'Bo'),

    # dagesh
    ('b@', 'B'),
    ('v@', 'U'),
    ('&@', 'p'),
    ('x@', 'K'),
    ('S@', 'T'),
    ('V@', 'Z'),

    # rafe
    ('b^', '~'),
    ('&^', 'f'),
    ('x^', 'R'),

    # sin dot
    ('$#', 'C')
    ]

def read_trans_table():
    """Reads tables and makes 1-1 translation lists"""
    with pkg_resources.open_text(tables, 'ycode-table-ascii.txt') as fin:
        lines1 = fin.readlines()
    with pkg_resources.open_text(tables, 'ycode-table.txt') as fin:
        lines2 = fin.readlines()
    lines = lines1 + lines2
    lines = [line.rstrip() for line in lines]
    lines = [line.split('\t') for line in lines
             if line and not line.startswith(';;')]

    ycode_chars = [line[0].strip() for line in lines]
    for one in ycode_chars:
        assert len(one) == 1, f'{one} has len != 1'

    yiddish_ords = [int(line[1].strip()) for line in lines]
    yiddish_chars = [chr(one) for one in yiddish_ords]

    return (ycode_chars, yiddish_chars)

def read_yivo2ycode_table():
    with pkg_resources.open_text(tables, 'yivo-ycode.txt') as fin:
        lines = fin.readlines()

    lines = [line.rstrip() for line in lines]
    lines = [line.split('\t') for line in lines
             if line and not line.startswith(';;')]

    yivo_chars = [line[0].strip() for line in lines]
    ycode_chars = [line[1].strip() for line in lines]
    yivo2ycode_1 = {yivo_char: ycode_char
                    for (yivo_char, ycode_char) in zip(yivo_chars, ycode_chars)
                    if len(yivo_char) == 1}
    yivo2ycode_2 = {yivo_char: ycode_char
                  for (yivo_char, ycode_char) in zip(yivo_chars, ycode_chars)
                  if len(yivo_char) == 2}
    return (yivo2ycode_1, yivo2ycode_2)


class Transliterator:
    def __init__(self):
        (ycode_chars, yiddish_chars) = read_trans_table()
        yiddish_str = ''.join(yiddish_chars)
        ycode_str = ''.join(ycode_chars)
        self.trans_yiddish2ycode = str.maketrans(
            yiddish_str, ycode_str)
        self.trans_ycode2yiddish = str.maketrans(
            ycode_str, yiddish_str)
        (self.yivo2ycode_1, self.yivo2ycode_2) = read_yivo2ycode_table()


    def yiddish2ycode(self, yiddish_text):
        """Convert Yiddish unicode to ascii ycode"""
        ycode_text = yiddish_text.translate(
            self.trans_yiddish2ycode)
        for (from_s, to_s) in COMBINATIONS:
            ycode_text = ycode_text.replace(from_s, to_s)
        return ycode_text

    def ycode2yiddish(self, ycode_text):
        """Convert ascii ycode to Yiddish unicode"""
        for (from_s, to_s) in COMBINATIONS:
            ycode_text = ycode_text.replace(to_s, from_s)
        yiddish_text = ycode_text.translate(
            self.trans_ycode2yiddish)
        return yiddish_text

    def yivo2ycode(self, yivo_text):
        """Convert text in yivo transliteration to ycode

        It iterates through string looking for two-letter combinations
        first, and if not then mapping the current letter.  

        This could be made more efficient by first mapping two-letter
        combinations throughout the string and then mapping remaining letters.
        A problem with this is that there is then confusion arises
        with whether letters are already mapped.  e.g. if ay is mapped to
        Ya, then the a shouldn't get mapped again.  

        After the mapping is done, final letters are fixed up, and
        the leading shtumer alef is added if necessary.  This is added in the
        cases of:
        W vov yud
        Y double yud
        or if starts with vowel i or u. We don't know this just by looking
        at the first character, since 'y' can be vowel or consonant
        however if it's v then it was a u

        TODO: use translate
        """
        yivo_text = yivo_text.replace('_', '')
        ycode_text = ''
        yivo_x = 0
        while yivo_x < len(yivo_text) - 1:
            chr1 = yivo_text[yivo_x]
            chr2 = yivo_text[yivo_x+1]
            chr12 = chr1 + chr2
            if chr12 in self.yivo2ycode_2:
                ycode_text += self.yivo2ycode_2[chr12]
                yivo_x += 2
            elif chr1 in self.yivo2ycode_1:
                ycode_text += self.yivo2ycode_1[chr1]
                yivo_x += 1
            else:
                print(f'unknown character {chr1}')
                ycode_text += chr1
                yivo_x += 1
                
        if yivo_x < len(yivo_text):
            chr1 = yivo_text[yivo_x]
            if chr1 in self.yivo2ycode_1:
                ycode_text += self.yivo2ycode_1[chr1]
                yivo_x += 1
            else:
                print(f'unknown character {chr1} {yivo_x}')
                ycode_text += chr1
                yivo_x += 1

        # fix up final letter
        chr1 = ycode_text[-1]
        if chr1 in 'xmnfq':
            chr1u = chr1.upper()
            ycode_text = ycode_text[:-1] + chr1u

        # add shtumer alef if necessary
        if ycode_text[0] in 'yYv' or yivo_text[0] == 'i':
            ycode_text = 'A' + ycode_text
        return ycode_text
