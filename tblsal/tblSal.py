import datetime
import sys
from splinter import Browser
import codecs
import pymongo


def getBaseInformation(filetoopen):
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
            Doc["SalaryBR"]["Data"]=v_temp[0]
            Doc["SalaryBR"]["JR"]= v_temp[4]
            Doc["SalaryBR"]["PL"]= v_temp[5]
            Doc["SalaryBR"]["SR"]= v_temp[6]
            ret.append(Doc)
    
    return ret


def getUSSalaryCareer(profession, defaultPlace): 
    # Objetive: Crawls the profession link from careerbuilder of one specific profession
    # Parameters: 
    #   profession: profession that I want crawl salary information
    #   Link: Ex.: http://salary.careerbuilder.com/business-analyst/San-Francisco/
    #
    
    seniority  = ["JR","PL", "SR" ] 
    ret = {}

    for sen in seniority:
        if (sen=='PL'):
           v_sen = ""
        else:
           v_sen = sen + " "
        strLink = "http://salary.careerbuilder.com/" + v_sen  + profession.replace("/"," ").strip() + "/" + defaultPlace 
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
            if (sen == 'JR'): 
               ret["SalaryUS"] = {}   
               ret["SalaryUS"]['JR'] = {}
               ret["SalaryUS"]['PL'] = {}
               ret["SalaryUS"]['SR'] = {}
               ret["SalaryUS"]["Font"]= "CareerBuilder"
               ret["SalaryUS"]["Data"]= datetime.datetime.now()
               ret["SalaryUS"]["relac"] = x["relac"]
                    
            ret["SalaryUS"][sen][defaultPlace] = x["salAverageDefault"]
            ret["SalaryUS"][sen]["AverageUS"]  = x["salAverageUS"] 
            ret["SalaryUS"][sen]["link"]= strLink
               
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
    print "###"
    print attribute.value; 
    print "###"
    v_temp = attribute.value.split(' ') # split based on space
    print len (v_temp)
    # When there's no enough data, site shows only US average, v_temp == 1
    v_salAverageDefault = v_temp[0].replace(",","").replace("$","") #got first word that should be value in default location
    ret["salAverageDefault"] =  v_salAverageDefault
    if (len(v_temp) > 1):
        #print v_temp
        v_percent =  v_temp[3].replace("%","")
        v_qualifier = v_temp[4]
        v_temp = attribute.value.split('\n')
        v_arrayRelac = []
        v_arrayRelac = v_temp[3:]
        if (v_qualifier == 'above'):
             salAverageUS = float(v_salAverageDefault) * (1-(float(v_percent)/100))
        elif (v_qualifier == 'below'):
             salAverageUS = float(v_salAverageDefault) * (1+(float(v_percent)/100))
        ret["salAverageUS"] = salAverageUS
        ret["relac"] = v_arrayRelac
    else:
        ret["salAverageUS"] = 0
        ret["relac"] = []   
    return ret

def Persist(doc):
    # get a handle to the school database
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db=connection.jobful
    tabSal = db.TabSal


    #try:
    tabSal.insert(doc)   # first insert


    #except:
    #    print "Unexpected error:", sys.exc_info()[0]


def main():
    start = datetime.datetime.now()
    # argv1 - salary table in Brazil
    # argv2 - default place to check value in US
    TabelaSalarialBase = getBaseInformation(sys.argv[1])
    TabelaSalarial = []
    DefaultPlaceUS = sys.argv[2]
    for item in TabelaSalarialBase: 
        ret = getUSSalaryCareer (item["Professional"]["English"], DefaultPlaceUS )
        itemcomplete = dict(list(item.items()) + list(ret.items()))
        Persist (itemcomplete)
        TabelaSalarial.append(itemcomplete)
    end = datetime.datetime.now()
    print end-start
    
if __name__ == '__main__':
    main()

