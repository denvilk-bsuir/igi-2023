from utils import (
    preprocess_text,
    divide_all_sentences,
    count_stats
)

text = None
with open('data/text.txt', "r") as f:
    text = ''.join(f.readlines())
text = preprocess_text(text)

print("Sentences:\n", *divide_all_sentences(text), sep="\n")
print("\n\nStatistics of the text:\n")
for k, v in count_stats(divide_all_sentences(text)).items():
    if k == 'top_n_grams':
        print("Top n grams:")
        for word, count in v:
            print(f"\t{word}: {count}")
    else:
        print(f'{k}: {v}')
