from TransLiter.jp_list import *
import pykakasi
import pandas as pd

def kanji_to_hiragana(text):
    kks = pykakasi.kakasi()
    hiragana_text = ''
    for result in kks.convert(text):
        if result['hira']:
            hiragana_text += result['hira']
        else:
            hiragana_text += result['orig']
    return hiragana_text

def jp(text):
    text = kanji_to_hiragana(text)
    hiragana_to_english.update(katakana_to_english)
    transliterated_text = ""
    i = 0
    while i < len(text):
        if i < len(text) - 1 and text[i+1] in ['ッ', 'っ']:
            transliterated_text += hiragana_to_english[text[i]][0]
            i += 1
        elif i < len(text) - 1 and text[i+1] in ['ゃ', 'ゅ', 'ょ']:
            transliterated_text += hiragana_to_english[text[i]+text[i+1]]
            i += 1
        else:
            transliterated_text += hiragana_to_english.get(text[i], text[i])
        i += 1
    return transliterated_text

def transliter_jp():
    while True:
        input_text = input("Please enter Japanese text: ")
        print(jp(input_text))
        if input_text == "": 
            break

def txt_jp(file):
    f = open(file, 'r')
    f2 = open("output_jp.txt", 'w')
    result = ""
    while True:
        line = f.readline()
        result += line + jp(line)
        if not line: 
            break
    print(result)
    f2.write(result)
    f.close()
    f2.close()

def csv_jp(file):
    data = pd.DataFrame(columns=['Original Text', 'Transliterated Text'])
    f = open(file, 'r')
    lines = f.readlines()
    
    index_list = list(range(len(lines)))
    sentence_list = []
    transliter_list = []
    for sentence in lines:
        st = sentence.strip()
        tr = jp(st)
        sentence_list.append(st)
        transliter_list.append(tr)

    data = pd.DataFrame({'Original Text': sentence_list, 'Transliterated Text': transliter_list}, index=index_list)
    data.to_csv("output_jp.csv")
    print(data)
    f.close()