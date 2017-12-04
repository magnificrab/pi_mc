import os
import os.path
import signal
import subprocess
import unittest
import pi_test
import pdb

def kill_circle_svc():
    #TODO: dynamic file name also location of pid file is wrong
    #TODO: handle case where pidfile exists but process is gone
    #pid_fn ='/home/robert/pi_mc/server/twistd.pid'
    #if not os.path.exists(pid_fn):
        #return
    #with open(pid_fn,'r') as pidfile:
        #for line in pidfile:
            #pid = int(line)
    #print('killing pid: ', pid)
    #os.kill(pid, signal.SIGKILL)
    #os.unlink(pid_fn)
    pass

def start_circle_svc():
    #TODO: make less directory sensitive
    #os.chdir('/home/robert/pi_mc/server')
    #subprocess.call(['python','svc_wrapper.py','circle_svc.py'])
    #subprocess.call(['docker','start','circle_svc'])
    pass

def confirm_circle_svc_available():
    if not pi_test.admin_status():
        raise ValueError('Server does not return code 200, exiting')
    

class IntegrationFunctional(unittest.TestCase):
    def setUp(self):
        confirm_circle_svc_available()
    def tearDown(self):
        pass
    def test_bulk_10_1000(self):
        res = pi_test.bulk_pi_coord()
        print('test_bulk 10x1000:',res)
        self.assertAlmostEqual(3.14,res,delta=.25)
    def test_bulk_1_1000000(self):
        res = pi_test.bulk_pi_coord(calls=1,reqpc=1000000)
        print('test_bulk 1x1000000:',res)
        self.assertAlmostEqual(3.14,res,delta=.25)
    def test_45_degree(self):
        pass

class IntegrationAdministrative(unittest.TestCase):
    def setUp(self):
        confirm_circle_svc_available()
    def tearDown(self):
        pass
    def test_stats1(self):
        self.assertTrue(pi_test.admin_stats())
    def test_stats2(self):
        self.assertTrue(pi_test.admin_stats())
        res = pi_test.bulk_pi_coord(calls=1,reqpc=100)
        self.assertTrue(pi_test.admin_stats(100))
    def test_forbidden_docs(self):
        self.assertTrue(pi_test.admin_forbidden())
    def test_kill(self):
        #self.assertTrue(pi_test.admin_kill())
        pass

if __name__ == '__main__':
    unittest.main()
        
