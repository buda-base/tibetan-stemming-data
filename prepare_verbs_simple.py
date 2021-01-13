import json

dadragsyls = []
with open('input/dadrag_syllables.txt') as f:
    dadragsyls = f.read().split('\n')

with open('input/monlam_verbs.json') as json_file:
    data = json.load(json_file)

    for inflected, contexts in data.items():
        if len(contexts) == 0:
            continue

        possible = set()
        for context in contexts:
            if 'བྱ་ཚིག' in context.keys():
                possible.add(context['བྱ་ཚིག'])

        possible = list(possible)
        #if len(possible) == 1 and possible[0] != inflected:
        for p in possible:
            if p != inflected:
                print(p+","+inflected)