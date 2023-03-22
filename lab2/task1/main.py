import re
from typing import List, Tuple, Dict, Any

text = None

with open('text1.txt',"r") as f:
    text = ''.join(f.readlines())

def preprocess_text(text: str) -> str:
    text = ' '.join(text.split("\n"))
    text = text.replace("\t", ' ')
    allowed = []
    good = True
    for symbol in text:
        if symbol == ' ':
            if good:
                good = False
                allowed.append(symbol)
        else:
            good = True
            allowed.append(symbol)
    return ''.join(allowed)

def find_all_unbreakable(text: str) -> str:
    REG = r'(?P<reg>(?P<type>Mr|Mrs|No|pp|St|no|Jr|Bros|Sr|etc|vs|esp|Fig|fig|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Okt|Nov|Dec|Ph\.D|PhD|al|cf|Inc|Ms|Gen|Sen|Prof|Dr|Corp|Co|Adj|Adm|Adv|Asst|Bart|Bldg|Brig|Bros|Capt|Cmdr|Col|Comdr|Con|Corp|Cpl|DR|Dr|Drs|Ens|Gen|Gov|Hon|Hr|Hosp|Insp|Lt|MM|MR|MRS|MS|Maj|Messrs|Mlle|Mme|Mr|Mrs|Ms|Msgr|Op|Ord|Pfc|Ph|Prof|Pvt|Rep|Reps|Res|Rev|Rt|Sen|Sens|Sfc|Sgt|Sr|St|Supt|Surg)\.\s*(?P<word>\w+))'
    
    all_unbreakable = []
    while res := re.search(REG, text):
        all_unbreakable.append((res.group('reg'), res.start('reg'), res.end('reg')))
        text = text[:res.start("reg")] + text[res.end("reg"):]
    
    return text

def divide_all_sentences(text: str) -> List[Tuple[str, str]]:
    REG = r"(?P<sentence>(?P<word>((?P<reg>(?P<type>Mr|Mrs|No|pp|St|no|Jr|Bros|Sr|etc|vs|esp|Fig|fig|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Okt|Nov|Dec|Ph\.D|PhD|al|cf|Inc|Ms|Gen|Sen|Prof|Dr|Corp|Co|Adj|Adm|Adv|Asst|Bart|Bldg|Brig|Bros|Capt|Cmdr|Col|Comdr|Con|Corp|Cpl|DR|Dr|Drs|Ens|Gen|Gov|Hon|Hr|Hosp|Insp|Lt|MM|MR|MRS|MS|Maj|Messrs|Mlle|Mme|Mr|Mrs|Ms|Msgr|Op|Ord|Pfc|Ph|Prof|Pvt|Rep|Reps|Res|Rev|Rt|Sen|Sens|Sfc|Sgt|Sr|St|Supt|Surg)\.\s*(?P<subword>\w+))|([\w0-9,'\-\"\"]+))\s*)+(?P<sign>(\.|\;|\!|\?|\.\.\.))\s*)"
    sentences = []
    while res := re.search(REG, text):
        sentences.append(((res.group("sentence")), res.group("sign")))
        text = text[:res.start("sentence")]+text[res.end("sentence"):]
    
    return sentences

def check_not_number(x: str) -> bool:
    return not x.isdigit()

def get_top_n_grams(grams: Dict[str, int]) -> List[Tuple[str, int]]:
    sorted_grams = sorted(grams.items(), key=lambda x: x[1], reverse=True)
    return sorted_grams

def count_stats(sentences: List[Tuple[str, str]], n: int = 4, k: int = 10) -> Dict[str, Any]:
    REG = r'[\w+\'0-9]+'
    top_n_grams = {}
    non_declarative = 0
    total_sentences = len(sentences)
    total_letters = 0
    total_words = 0
    total_letters = 0
    for sentence, sign in sentences:
        if sign == '?' or sign == '!': 
            non_declarative += 1
        words = re.findall(REG, sentence)
        words = list(filter(check_not_number, words))
        print(words)
        for word in words:
            total_letters += len(word)
            for i in range(len(word)-n+1):
                l = word[i: i+n]
                top_n_grams[l] = top_n_grams.get(l, 0) + 1 
        total_words += len(words)
    
    top_k = get_top_n_grams(top_n_grams)[:k]

    average_letters = total_letters / total_sentences
    average_word_len = total_words / total_letters
    return {
        'total_sentences' : total_sentences,
        'non_declarative' : non_declarative,
        'average_letters' : average_letters,
        'average_word_len' : average_word_len,
        'top_n_grams': top_k
    }    

text = preprocess_text(text)
new_text = preprocess_text(find_all_unbreakable(text))
# print(new_text)

print("Sentences:",*divide_all_sentences(text), sep="\n")

for k,v in count_stats(divide_all_sentences(text)).items():
    print(f'{k}: {v}')
