import importlib.resources as pkg_resources
from . import tables

COMBINATIONS = [
    # b + a + dagesh = B + a
    # normalization puts these in the wrong order
    # needs to go before b+dagesh so that the inverse
    # transformation will do this first
    ('ba@', 'Ba'),
    ('bo@', 'Bo'),

    # beys with dagesh = B
    ('b@', 'B'),
    # beys with rafe = ~
    ('b^', '~'),

    # vov with dagesh = U
    ('v@', 'U'),
    # double vov with dagesh = Z
    # not really a letter
    ('V@', 'Z'),

    # khof with dagesh = L (kof)
    ('k@', 'L'),
    # khof with rafe = Q  (unknown character)
    ('k^', 'Q'),

    # bare_fey with dagesh = p
    ('&@', 'p'),
    # bare_fey with rafe = fey
    ('&^', 'f'),

    # sof with dagesh = G (sof)
    ('T@', 'G'),
    ]

def read_trans_table():
    """Reads tables and makes 1-1 translation lists"""
    with pkg_resources.open_text(tables, 'ycode-table-ascii.txt') as fin:
        lines1 = fin.readlines()
    with pkg_resources.open_text(tables, 'ycode-table.txt') as fin:
        lines2 = fin.readlines()
    lines = lines1 + lines2
    
    lines = [line.rstrip().split('\t') for line in lines
             if not line.startswith(';;')]

    ycode_chars = [line[0].strip() for line in lines]
    for one in ycode_chars:
        assert len(one) == 1, f'{one} has len != 1'

    yiddish_ords = [int(line[1].strip()) for line in lines]
    yiddish_chars = [chr(one) for one in yiddish_ords]

    return (ycode_chars, yiddish_chars)


class Transliterator:
    def __init__(self):
        (ycode_chars, yiddish_chars) = read_trans_table()
        yiddish_str = ''.join(yiddish_chars)
        ycode_str = ''.join(ycode_chars)
        self.trans_yiddish2ycode = str.maketrans(
            yiddish_str, ycode_str)
        self.trans_ycode2yiddish = str.maketrans(
            ycode_str, yiddish_str)

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
