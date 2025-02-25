import json
import random
with open("mood.json",'r') as file:
    emotions=json.load(file)

def sentence_generator(n=10):
    all_sentences = emotions["positive"] + emotions["negative"] + emotions["neutral"]
    return random.sample(all_sentences, min(n, len(all_sentences)))
    # breaking it down
    #random.sample(list,<number of items to be selected at random>)
    #min(n,len(sentence)): ensure if n(user input)> sentence present -> pass all the sentence since it will be lesser


