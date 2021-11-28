import unicodedata
from yiddishycode.translit import Transliterator

def main():
    transliterator = Transliterator()
    x = 1
    for yivo_text in [
            'vos', 'shoyn', 'ingantsn', 'azoy', 'kontshn', 'yerushe',
            'oysgekratst', 'yerushe', 'nadn', 'avrom-yankev',
            'vuhin']:
        ycode_text = transliterator.yivo2ycode(yivo_text)
        print(f'{yivo_text} -> {ycode_text}')

if __name__ == '__main__':
    main()
