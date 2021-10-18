import unicodedata
from yiddishycode.translit import Transliterator

def main():
    transliterator = Transliterator()    
    #with open('tests/test-words.txt', 'r', encoding='utf-8') as fin:
    with open('tests/words2.txt', 'r', encoding='utf-8') as fin:        
        lines = fin.readlines()
    words = [line.strip() for line in lines]
    for word in words:
        word = unicodedata.normalize('NFC', word)            
        #print(word)        
        ycode_text = transliterator.yiddish2ycode(word)
        yiddish_text = transliterator.ycode2yiddish(ycode_text)
        assert word == yiddish_text, 'something wrong'
        print(ycode_text)

if __name__ == '__main__':
    main()
        



