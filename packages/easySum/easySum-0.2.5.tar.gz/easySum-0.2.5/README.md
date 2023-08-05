# easySum
## LICENSE
This software is released under the MIT License, see LICENSE.txt.

## Install
```
pip install easySum
```

## Usage
```
from easySum import summarize_sentences

result = summarize_sentences(<要約したい文章>, sentences_count=<要約後の文章数(デフォルトは3)>, algorithm=<アルゴリズム(デフォルトはlexrank)>)

```
- アルゴリズムは以下から選択
  -  lex: LexRank
  -  tex: TextRank
  -  lsa: LSA
  -  kl: KL
  -  luhn: Luhn
  -  redu: Reduction
  -  sum: SumBasic

- 現在は日本語のみに対応. 英語対応は修正中.
