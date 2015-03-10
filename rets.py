__author__ = 'z9764'
import re

jn = '"sdasdaPhrasal verbs"dasdas!@12as '
tt=re.search(r"(.*)Phrasal verbs(.*)",jn)

print(tt)

filename="hello_world.json"
mc = re.search(r"[\w\-_]*",filename)

print(mc)