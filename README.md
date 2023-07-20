# yiddishycode

A Python library for a bidirectional encoding of Yiddish text in ascii

Seth Kulick (skulick@ldc.upenn.edu)

## Purpose
 It can sometimes be convient in computational work to abstact away from issues of non-ascii characters and bidirectional reprsentation, as was the case when developing the part-of-speech tagger for Yiddish discussed [here](https://arxiv.org/abs/2204.01175).  This library will convert the Unicode for Yiddish text to an ascii representation and back again, without any loss.  

While there are well-established romanizations of Yiddish text that is written with the Hebrew alphabet, such encodings are not bidirectional.  For example, 'alts' may be 'אַלץ' or '‪אַלטס'.  In addition, the conversion to a standard romanization for computational work is not always appropriate - e.g. if the text contains OCR or other types of errors, and the goal is to work with existing text as it is, not in a cleaned-up version.   

## Installation 
While this will eventually be made into a proper pypi package, for now it can be installed using a standard pip install:

```
git clone
cd yiddishycode
pip install .
```
## Example

```
from yiddishycode.translit import Transliterator
translit = Transliterator()
asc = translit.yiddish2ycode('⁧מחבר')⁩
```

## Usage notes
This code will only work with Yiddish script in the NFC or NFD normalization.  




## Citation

If you'd like to cite `yiddishycode` in a publication, you can include a link to this source:
https://github.com/skulick/yiddishycode

## Inspiration

The idea for this library was influenced by the [Buckwalter transliteration for Arabic](https://en.wikipedia.org/wiki/Buckwalter_transliteration).



