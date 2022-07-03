#import re
#
#with open("news_keywords.txt", "r") as f:
#    for line in f.readlines():
#        line = line.split()
#        del line[0]
#        r = re.compile("[а-яА-Я]+")
#        ru_words = [w for w in filter(r.match, line)]
#        word = " ".join(ru_words)
#        print(word)

import math

a = 4
a = math.sqrt(a)
print(a)
