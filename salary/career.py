from splinter import Browser
import sys

LINK = "http://salary.careerbuilder.com/"
WAIT_TIME = 15

def crawl(profession, defaultplace): 
    strLink = LINK  + profession.replace("/"," ").strip() + "/"+ defaultplace.strip() + "/"
    attribute = ""
    browser = Browser('phantomjs')

    browser.visit(strLink)
        
    if  browser.is_element_present_by_css('div.salary-average', WAIT_TIME):
        attributes = browser.find_by_css("div.salary-ajax")
        attribute = attributes[0].value
        browser.quit()
    else:
        print "log erro"
    return attribute

def getSalary(attribute):  
    Salary = {}
    atrData = attribute.split(' ') 

    Salary["city"] = atrData[0].replace(",","").replace("$","") #got first word that should be value in default location

    # check if found enough data
    if (len(atrData) > 10):
        percent =  atrData[3].replace("%","")
        qualifier = atrData[4]
        
        if (qualifier.lower() == 'above'):
             Salary["US"] = float(Salary["city"]) * (100 / (100 + float(percent)))
        elif (qualifier.lower() == 'below'):
             Salary["US"] = float(Salary["city"]) * (1+(float(percent)/100))
        else:
             Salary["US"] = 0
    else:
        Salary["US"] = Salary["city"]  
    return Salary

