import unittest
import Repository as RP


class RepoTester(unittest.TestCase):
    ''' 
    A test to establish if the Repository constructor
    generates a non-null object.

    @author Joshua Rosenthal
    '''
    repo = None
    
    def test_init(self):
        self.repo = RP.Repository()
        self.assertNotEqual(self.repo, None)
    
    '''
    A test to assess the validity of the connection
    between the repository and the database. A
    valid connection is demonstrated by a successful read.

    @author Joshua Rosenthal
    '''
    def test_connection(self):
        self.repo = RP.Repository()
        self.assertEqual(self.repo.TestConncetion(),True)
        t = self.repo.showTables()
        self.assertEqual(t,[('runAncestry',)])
        self.repo.tearDown()
        self.assertEqual(self.repo.TestConncetion(),False)

    
    '''
    A test of the insert and read functionality of the 
    Repository class.

    @author Joshua Rosenthal
    '''
    def test_insert_and_read(self): 
        self.repo = RP.Repository()
        self.repo.insert([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        t=self.repo.getRun(0)
        self.assertNotEqual(t, None)
    '''
    A test to show that the getStatesRanked method returns a non-null
    value. The testGetStatesRanked function is a modified version
    of getStatesRanked with a hard coded session ID since the original
    method is designed to work in the context of the solver and not
    in isolation as it is used here.
    
    @author Joshua Rosenthal
    '''
    def test_get_states_ranked(self):
        self.repo = RP.Repository()
        t = self.repo.testGetStatesRanked([0,0,0])
        self.assertNotEqual(t, []) #should nopt return empty set
    '''
    A test to assess the validity of the getMin and getMax functions
    for all inputs: 'A', 'E', 'F'.
    
    @author Joshua Rosenthal
    '''
    def test_min_and_max(self):
        self.repo = RP.Repository()
        minTestA = self.repo.getMin('A')
        minTestE =self.repo.getMin('E')
        minTestF =self.repo.getMin('F')
        maxTestA = self.repo.getMax('A')
        maxTestE =self.repo.getMax('E')
        maxTestF =self.repo.getMax('F')
        self.assertNotEqual(minTestA, None)
        self.assertNotEqual(minTestE, None)
        self.assertNotEqual(minTestF, None)
        self.assertNotEqual(maxTestA, None)
        self.assertNotEqual(maxTestE, None)
        self.assertNotEqual(maxTestF, None)
       
if __name__ == '__main__':
    unittest.main()
