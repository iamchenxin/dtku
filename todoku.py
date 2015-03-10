__author__ = 'z9764'
import json
import re
import codecs


mHlv=["======","=====","====","===","=="]

mlistlv=["  * ","    * ","      * "]

mOrderlv=["  - ","    - ","      - "]

def test_key(dict,key):
    if key in dict.keys():
        if dict[key]:
            return True
    return False

class cDokuConvert:

    def __init__(self):
        self.data=""
        self.name=""
        self.mh_lv=0
        pass

    def mH(self,thestr,lv_int):
        "{0} {1} {2}\n".format(mHlv[lv_int],thestr,mHlv[lv_int])
        return "{0} {1} {2}\n".format(mHlv[lv_int],thestr,mHlv[lv_int])

    def oV(self,thestr):
        return "<wrap vo>{0}</wrap>".format(thestr)

    def bExample(self,ex_array,list_lv):
        tmpstr=""
        for ex in ex_array:
            tmpstr+= "{0} {1}\n".format(mlistlv[list_lv],ex.strip())
        return tmpstr

    def bSynonyms(self,bsyn,list_lv):
        tmp_str=""
        tmp_str+= "{0} __Synonyms__ : {1}\n".format(mlistlv[list_lv],bsyn.strip())
        return tmp_str


    def bSubsence(self,subs_array):
        tmpstr=""
        for subs in subs_array:
            if test_key(subs,"meaning"):
                tmpstr+="{0} {1}\n".format(mOrderlv[0],subs["meaning"])
                if test_key(subs,"example"):
                    tmpstr+=self.bExample(subs["example"],1)
                if test_key(subs,"synonyms"):
                    tmpstr+=self.bSynonyms(subs["synonyms"],1)
        return tmpstr



    def header(self,lhead):
        tmp_str=""
        tmp_str+=self.mH(self.name,0)
        if "lin" in lhead.keys():
            if lhead["lin"]:
                tmp_str+="  * Line breaks : ''{0}'' \n".format( lhead["lin"])
        if "syl" in lhead.keys():
            if lhead["syl"]:
                tmp_str+="  * Syllabification : ''{0}'' \n".format( lhead["syl"])
        if "syl" in lhead.keys():
            if lhead["syl"]:
                tmp_str+="  * Pronuncaition : {0} ''{1}'' \n".format( self.oV(self.name),lhead["pro"])
        if "rank" in lhead.keys():
            if lhead["rank"]:
                tmp_str+="  * Rank : {0} \n".format( lhead["rank"])
        tmp_str+="\n"
        return tmp_str




    def definition(self,ldefs):
        tmp_str=""
        self.mh_lv=0
        tmp_str+=self.mH("Definition",self.mh_lv)

        for ldef in ldefs:

            if test_key(ldef,"partOfSpeech"):
                self.mh_lv+=1
                tmp_str+=self.mH( ldef["partOfSpeech"],self.mh_lv )
                if test_key(ldef,"sense"):
                    count = 0
                    for lsense in ldef["sense"]:
                        count+=1
                        if test_key(lsense,"meaning"):
                            self.mh_lv+=1
                            tmp_str+=self.mH("{0}. {1}".format(str(count),lsense["meaning"]),self.mh_lv )
                            self.mh_lv-=1
                        if test_key(lsense,"example"):
                            tmp_str+=self.bExample(lsense["example"],0)
                        if test_key(lsense,"synonyms"):
                            self.mh_lv+=2
                            tmp_str+=self.mH("Synonyms",self.mh_lv)
                            tmp_str+="{0}\\\\\n".format(lsense["synonyms"].strip())
                            self.mh_lv-=2
                        if test_key(lsense,"subsense"):
                            self.mh_lv+=2
                            tmp_str+=self.mH("Subsense",self.mh_lv)
                            tmp_str+=self.bSubsence(lsense["subsense"])
                            self.mh_lv-=2
                self.mh_lv-=1
        return tmp_str

    def bPhrases(self,lphra_array):
        tmp_str=""
        for lphra in lphra_array:
            if test_key(lphra,"words"):
                self.mh_lv+=2
                tmp_str+=self.mH(lphra["words"].strip(),self.mh_lv )
                if test_key(lphra,"definition"):
                    ldef = lphra["definition"]
                    if test_key(ldef,"meaning"):
                        tmp_str+="{0}\n".format(ldef["meaning"].strip() )
                    if test_key(ldef,"example"):
                        tmp_str+=self.bExample(ldef["example"],0)
                self.mh_lv-=2
        return tmp_str


    def build_all(self,js_data,name):
        whole_txt=""
        self.name=name
        # word
        whole_txt+=self.header(js_data["word"])

        # definition
        whole_txt+=self.definition(js_data["definition"])

        # origin
        if test_key(js_data,"Origin"):
            whole_txt+=self.mH("Origin",0)
            whole_txt+=js_data["Origin"].strip()
            whole_txt+="\n"
        # Phrases

        if test_key(js_data,"Phrases"):
            self.mh_lv=0
            whole_txt+=self.mH("Phrases",self.mh_lv)
            whole_txt+=self.bPhrases(js_data["Phrases"])

        # some thing wrong in "Phrasal verbs"
        # so i search it
        for jn,jv in js_data.items():
            if re.search(r"(.*)Phrasal verbs(.*)",jn):
                pverbName= jn
                if js_data[pverbName]:
                    self.mh_lv=0
                    whole_txt+=self.mH("Phrasal verbs",self.mh_lv)
                    whole_txt+=self.bPhrases(js_data[pverbName])

        if test_key(js_data,"Derivatives"):
            self.mh_lv=0
            whole_txt+=self.mH("Derivatives",self.mh_lv)
            for deri in js_data["Derivatives"]:
                whole_txt+=deri["words"]+","
            whole_txt+="\n"

        if test_key(js_data,"See"):
            self.mh_lv=0
            whole_txt+=self.mH("See also",self.mh_lv)
            for see in js_data["See"]:
                whole_txt+=see+","
            whole_txt+="\n"

        if test_key(js_data,"rhyme"):
            self.mh_lv=0
            whole_txt+=self.mH("Rhyme",self.mh_lv)
            whole_txt+=js_data["rhyme"]+"\n"

        return whole_txt



def test1(filename):
    cd =cDokuConvert()

    ff=codecs.open(filename,"r",'utf-8')
    js_data= json.load(ff)

    mc = re.search(r"[\w\-_]*",filename)
    name =mc.group(0)
    print(name)
    txt = cd.build_all(js_data,name)

    df = codecs.open(name+".txt","w",'utf-8')
    df.write(txt)
    df.close()

test1("play.json")