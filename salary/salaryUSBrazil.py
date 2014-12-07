from datetime import datetime
import codecs
import pymongo
import sys
import career
import imp
mongo_connector = imp.load_source('x', '../jobful/utils/mongo_connector.py')

db=mongo_connector.get_db()

def getProfessionJRSRPL(profession): 
    seniority  = ["JR","PL", "SR" ] 
    ret = {}
    ret["SalaryUS"] = {}
    for sen in seniority:
        if (sen=='PL'):
           v_sen = ""
        elif(sen=='JR'):
           v_sen = "Junior "
        else:
           v_sen = "Senior "
        # Always get US average
        
    return ret

def persist(doc):
    tabSal = db.salBR_US
    tabSal.insert(doc)  


def getBrasilSalary():
    ret = []
    FILETOOPEN = "tblSalarial.txt"
    
    with codecs.open (FILETOOPEN,'rb',encoding='UTF-16') as fo:
        for line in  fo.readlines():
            v_temp =  line.split('\t')
            Doc = {}
            Doc['Professional'] = {}
            Doc['Professional']['Portuguese']= v_temp[2]
            Doc['Professional']['English'] = v_temp[3]
            Doc["BR"] = {}
            Doc["BR"]["Font"]=v_temp[1]
            Doc["BR"]["Data"]=datetime.strptime(v_temp[0],'%d/%m/%Y')
            Doc["BR"]["JR"]= float(v_temp[4]) * 12
            Doc["BR"]["PL"]= float(v_temp[5]) * 12
            Doc["BR"]["SR"]= float(v_temp[6]) * 12
            ret.append(Doc)
    
    return ret

def getUSSalary(professional):

    DEFAULT_PLACE = "SAN FRANCISCO"
    ret = {}
    ret["US"] = {}
    ret["US"]["Data"] = datetime.now()
    ret["US"]["Font"] = "CareerBuilder"
    ret["US"]["JR"] = career.getSalary(career.crawl("TRAINEE " + professional, DEFAULT_PLACE ))["US"]
    ret["US"]["PL"] = career.getSalary(career.crawl(professional, DEFAULT_PLACE ))["US"]
    ret["US"]["SR"] = career.getSalary(career.crawl("SENIOR " + professional, DEFAULT_PLACE ))["US"]
    return ret

def BrasilUSSalaryTable():
    # create salary table Brasil x US
   
    start = datetime.now()
    SalaryBrasil = getBrasilSalary()
    for item in SalaryBrasil: 
        try:
           ret = getUSSalary(item["Professional"]["English"])
           itemcomplete = dict(list(item.items()) + list(ret.items()))
           persist (itemcomplete)
        except:
            print itemcomplete
            print "Unexpected error:", sys.exc_info()[0] 
            continue
    end = datetime.now()
    print end-start



def main():
    BrasilUSSalaryTable()

    
if __name__ == '__main__':
    main()

