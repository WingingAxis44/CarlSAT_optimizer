import unittest
import Wrapper, Repository

class UnitTester(unittest.TestCase):
    # def test_stateFile(self):
    #     self.assertEqual(Wrapper)
        
    
    # def test_stateFileMatcher(self):
    #     self.assertEquals(Repository.getStateMatch(10,10,10), "statefile2") 
        
    def test_stringHandling(self):
        with open("out.txt") as f:
            cost = eval(str(f.readline(), 'utf-8').split()[1])
            time = eval(str(f.readline(), 'utf-8').split()[3])
            
            


    # def test_WrapperIO(self):
    #     self.assertEquals(Wrapper.runCarlSAT([1,2,3,4,5,6,test0.test],56.7))

    # def test_CostCalculator(self):
    #     pass
    
    # def test_Iterator(self):
    #     pass
        
    # def test_CostCalculator(self):
    #     pass