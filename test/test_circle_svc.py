import ast
import unittest
import flask
import io
import json
import circle_svc
from circle_svc import app

class CircleSvc1(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_45_degrees_direct(self):
        self.assertTrue(circle_svc.pic(0,0))
        self.assertTrue(circle_svc.pic(.1,.1))
        self.assertTrue(circle_svc.pic(.2,.2))
        self.assertTrue(circle_svc.pic(.3,.3))
        self.assertTrue(circle_svc.pic(.4,.4))
        self.assertTrue(circle_svc.pic(.5,.5))
        self.assertTrue(circle_svc.pic(.6,.6))
        self.assertTrue(circle_svc.pic(.7,.7))
        self.assertFalse(circle_svc.pic(.8,.8))
        self.assertFalse(circle_svc.pic(.9,.9))

    def test_45_degrees_via_server(self):
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=0&y=0', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.1&y=.1', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.2&y=.2', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.3&y=.3', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.4&y=.4', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.5&y=.5', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.6&y=.6', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.7&y=.7', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "True")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.8&y=.8', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "False")
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.9&y=.9', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True).strip().strip('\"').split(' ')[3], "False")

    def test_none_as_input(self):
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.9', follow_redirects=True)
        self.assertEqual(res.status_code, 500)
        res = self.app.get('/pi/api/v0.0/pi_in_circle?y=.9', follow_redirects=True)
        self.assertEqual(res.status_code, 500)
        res = self.app.get('/pi/api/v0.0/pi_in_circle', follow_redirects=True)
        self.assertEqual(res.status_code, 500)

    def test_reject_negatives(self):
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=.1&y=-.9', follow_redirects=True)
        self.assertEqual(res.status_code, 500)
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=-.1&y=.9', follow_redirects=True)
        self.assertEqual(res.status_code, 500)
        res = self.app.get('/pi/api/v0.0/pi_in_circle?x=-.1&y=-.9', follow_redirects=True)
        self.assertEqual(res.status_code, 500)

    def test_bulk_45_degree(self):
        req_data = []
        req_data.append({'x': 0, 'y': 0})
        req_data.append({'x': .1, 'y': .1})
        req_data.append({'x': .2, 'y': .2})
        req_data.append({'x': .3, 'y': .3})
        req_data.append({'x': .4, 'y': .4})
        req_data.append({'x': .5, 'y': .5})
        req_data.append({'x': .6, 'y': .6})
        req_data.append({'x': .7, 'y': .7})
        testd = io.StringIO(json.dumps(req_data))
        res = self.app.post('/pi/api/v0.0/bulk_pic', data=testd, follow_redirects=True)
        self.assertTrue(all(map(lambda s: s.strip()=='true', res.get_data(as_text=True).strip()[1:-2].split(','))))

        req_data = []
        req_data.append({'x': .8, 'y': .8})
        req_data.append({'x': .9, 'y': .9})
        testd = io.StringIO(json.dumps(req_data))
        res2 = self.app.post('/pi/api/v0.0/bulk_pic', data=testd, follow_redirects=True)
        #TODO: this doesn't work but something like this might be nicer than ugly code below print(ast.literal_eval(res2.get_data(as_text=True).replace('\n','')))
        self.assertTrue(all(map(lambda s: s.strip()=='false', res2.get_data(as_text=True).strip()[1:-2].split(','))))

    #TODO: check non-supported request types i.e. post when get is expected etc
    #TODO: performance tests

    def test_forbidden_docs(self):
        res = self.app.get('/pi/api/v0.0/documentation', follow_redirects=True)
        self.assertEqual(res.status_code, 403)

    def test_admin_kill(self):
        #res = self.app.post('/pi/api/v0.0/admin/kill', follow_redirects=True)
        #self.assertEqual(res.status_code, 204)

        pass #TODO: won't work since reactor isn't really running

if __name__ == '__main__':
    unittest.main()
