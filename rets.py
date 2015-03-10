__author__ = 'z9764'
import re
from pathlib import Path

jn = '"sdasdaPhrasal verbs"dasdas!@12as '
tt=re.search(r"(.*)Phrasal verbs(.*)",jn)

print(tt)

filename="hello_world.json"
mc = re.search(r"[\w\-_]*",filename)

print(mc)

sc="i go to play a boll"
sss="play a"
regr= r"\b{0}\b".format(sss)
th="<wrap vo>{0}</wrap>".format(sss)

rtt=re.sub(regr,th,sc)
print(rtt)
aaa = 1
aal=[1,2,3]

print(type(aaa))
print(type(aal) is list )

pit = Path("./hel").iterdir()
rp = Path("./hel").resolve()
ss= rp.joinpath("ddd.txt")
print(ss)


for pp in pit:
    print(pp.resolve())
    myd = re.findall(r"\w+",str(pp))
    mlen=myd.__len__()
    print(mlen)
    print(pp)
    print(myd[mlen-2])