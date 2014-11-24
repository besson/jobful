from datetime import datetime
from splinter import Browser
import codecs
import pymongo
import sys

def getBrasilInformation(filetoopen):
    #
    # Load base .txt file into memory + build link to be crawled + get default local in US to find salary
    # File format to open: 
    #Data;Fonte;Cargos;Description in english;Junior (valor site);Pleno(valor site);Senior(valor site)
    #01/11/2014;Info;Administrador de banco de dados (DBA);Database Administrator;4393.01;5886.35;9381.49
    #
    ret = []
    
    
    with codecs.open (filetoopen,'rb',encoding='UTF-16') as fo:
        for line in  fo.readlines():
            v_temp =  line.split('\t')
            Doc = {}
            Doc['Professional'] = {}
            Doc['Professional']['Portuguese']= v_temp[2]
            Doc['Professional']['English'] = v_temp[3]
            Doc["SalaryBR"] = {}
            Doc["SalaryBR"]["Font"]=v_temp[1]
            Doc["SalaryBR"]["Data"]=datetime.strptime(v_temp[0],'%d/%m/%Y')
            Doc["SalaryBR"]["JR"]= float(v_temp[4]) * 12
            Doc["SalaryBR"]["PL"]= float(v_temp[5]) * 12
            Doc["SalaryBR"]["SR"]= float(v_temp[6]) * 12
            ret.append(Doc)
    
    return ret


def getUSSalaryCareer(profession): 
    # Objetive: Crawls the profession link from careerbuilder of one specific profession
    # Parameters: 
    #   profession: profession that I want crawl salary information
    #   Link: Ex.: http://salary.careerbuilder.com/business-analyst/San-Francisco/
    #
    
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
        strLink = "http://salary.careerbuilder.com/" + v_sen  + profession.replace("/"," ").strip() + "/San Francisco"

        browser = Browser('phantomjs')
        print strLink
        browser.visit(strLink)
        
        #look for salary-average tag 
        if  browser.is_element_present_by_css('div.salary-average', wait_time=15):
            attributes = browser.find_by_css("div.salary-ajax")
            # it should return one attribute, for "just in case"
            
            for attribute in attributes:
               # should create one object by link
               x = ExtractSal(profession, strLink, attribute) 
            
               ret["SalaryUS"]["Font"]= "CareerBuilder"
               ret["SalaryUS"]["Data"]= datetime.now()
 
            ret["SalaryUS"][sen] = x["salAverageUS"] 
               
        else:
              # to be improved: log error, probably site structure changed
              print "nao achou"        
        browser.quit()
    
    return ret

def getUSSalaryCareer(profession, defaultPlace): 

    
    ret = {}
    ret["SalaryUS"] = {}
    strLink = "http://salary.careerbuilder.com/"+ profession.replace("/"," ").strip() + "/" + defaultPlace.strip() + "/" 
    browser = Browser('phantomjs')
    print strLink
    browser.visit(strLink)
        
    #look for salary-average tag 
    if  browser.is_element_present_by_css('div.salary-average', wait_time=15):
        attributes = browser.find_by_css("div.salary-ajax")
        # it should return one attribute, for "just in case"
            
        for attribute in attributes:
            # should create one object by link
            x = ExtractSal(profession, strLink, attribute) 
        ret["SalaryUS"]["profession"]= profession
        ret["SalaryUS"]["location"]= defaultPlace
        ret["SalaryUS"]["Font"]= "CareerBuilder"
        ret["SalaryUS"]["Data"]= datetime.now()
        ret["SalaryUS"]['US'] = x["salAverageUS"] 
        ret["SalaryUS"][defaultPlace] = x["salAverageDefault"]
               
    else:
        # to be improved: log error, probably site structure changed
        print "nao achou"        
    browser.quit()
    
    return ret



def ExtractSal(profession, link, attribute):

    # Objective: create one object per link crawled
    # parameters: profession that I want collect information. Ex.: business-analyst
    #             link: link for that profession in careerbuilder http://salary.careerbuilder.com/business-analyst/San-Francisco/
    #             Attribute: attribute crawled. See example below   
    # Example of attribute got in :  
    # $42,268 This is 10% above the national average
    # Where does this data come from?
    # Salaries for jobs similar to "Computer Operator" in "San Francisco"
    # Computer User Support Specialists
    # First-Line Supervisors of Retail Sales Workers
    # Network and Computer Systems Administrators  
    ret = {}
    v_temp = attribute.value.split(' ') # split based on space
    # When there's no enough data, site shows only US average, v_temp == 1
    v_salAverageDefault = v_temp[0].replace(",","").replace("$","") #got first word that should be value in default location
    ret["salAverageDefault"] =  v_salAverageDefault
    # when there's no enough data, structure of information is different
    if (len(v_temp) > 10):
        v_percent =  v_temp[3].replace("%","")
        v_qualifier = v_temp[4]
        v_temp = attribute.value.split('\n')
        v_arrayRelac = []
        v_arrayRelac = v_temp[3:]
        if (v_qualifier == 'above'):
             salAverageUS = float(v_salAverageDefault) * (1-(float(v_percent)/100))
        elif (v_qualifier == 'below'):
             salAverageUS = float(v_salAverageDefault) * (1+(float(v_percent)/100))
        else:
             salAverageUS = 0
        ret["salAverageUS"] = salAverageUS
        ret["relac"] = v_arrayRelac
    else:
        ret["salAverageUS"] = v_salAverageDefault
        ret["relac"] = []   
    return ret

def PersistSalBR_US(doc):
    #
    # persist comparation table in mongoDb
    #
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db=connection.jobful
    tabSal = db.salBR_US


    #try:
    tabSal.insert(doc)   # first insert


    #except:
    #    print "Unexpected error:", sys.exc_info()[0]

def PersistJobsSal(doc):
    #
    # persist comparation table in mongoDb
    #
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db=connection.jobful
    tabSal = db.jobsSal


    #try:
    tabSal.insert(doc)   # first insert


    #except:
    #    print "Unexpected error:", sys.exc_info()[0]


def BrasilUSSalaryTable(filetoOpen, DefaultPlaceUS):
    # create salary table Brasil x US
    start = datetime.now()

    TabelaSalarial = []
    for item in TabelaSalarialBase: 
        ret = getUSSalaryCareer (item["Professional"]["English"], DefaultPlaceUS )
        itemcomplete = dict(list(item.items()) + list(ret.items()))
        PersistSalBR_US (itemcomplete)
        TabelaSalarial.append(itemcomplete)
        print itemcomplete
    end = datetime.now()
    print end-start

def USSalaryTable():
    # create a table with average US Salary based on jobs
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db=connection.jobful

    iter = db.jobs.aggregate([{"$group":{"_id":{"title":"$title","location":"$location"}, "n":{"$sum":"1"}}}]);
    for doc in iter['result']:
        print doc['_id']['title'];
        print doc['_id']['location'];
        item = getUSSalaryCareer(doc['_id']['title'], doc['_id']['location'])
        print item
        PersistJobsSal(item)


def main():
    if (sys.argv[1] == "jobs"):
        USSalaryTable()
    else:
        BrasilUSSalaryTable(sys.argv[1], sys.argv[2])

    
if __name__ == '__main__':
    main()

