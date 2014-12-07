import unittest
import career

class Testcareer(unittest.TestCase):

    def setUp(self):
        self.dummyProfessions = ["Jagunco do sertao", "Menino do rio"]
        self.professions= ["software engineer","database administrator"]
        self.payabove="San francisco"
        self.paybelow="Alabama"
        
    def test_notfound(self):
        # make sure the shuffled sequence does not lose any elements
        for element in self.dummyProfessions:
            ret=career.getSalary(career.crawl(element, self.payabove))  
            self.assertEquals(ret["US"],'0')
            self.assertEquals(ret["city"],'0')

    def test_below(self):
           # make sure the shuffled sequence does not lose any elements
        for element in self.professions:
            ret=career.getSalary(career.crawl(element, self.paybelow))  
            assert (ret["US"] > 10000)
            assert (ret["city"] > 10000)


    def test_above(self):
           # make sure the shuffled sequence does not lose any elements
        for element in self.professions:
            ret=career.getSalary(career.crawl(element, self.payabove))  
            assert (ret["US"] > 10000)
            assert (ret["city"] > 10000)


if __name__ == '__main__':
    unittest.main()