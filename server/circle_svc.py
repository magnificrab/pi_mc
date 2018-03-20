#import json
import os
import os.path
import sys
import threading
import time
from flask import Flask, json, jsonify, request, abort
"""
import twisted
from twisted.application import service
from twisted.web import server, static
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from autobahn.twisted.resource import WSGIRootResource
from twisted.python.threadpool import ThreadPool
"""
import pdb
import uuid
import structlog
from prometheus_client.twisted import MetricsResource
from prometheus_client import Summary, MetricsHandler
import socket
from http.server import HTTPServer
#import bjoern

#TODO: are all these imports really necessary?

logger = structlog.get_logger()  #twistd output not formatted
#logger = structlog.twisted.plainJSONStdOutLogger() #No msg()?
app = Flask(__name__)
s = Summary('request_latency_seconds', 'Description of summary')

metrics = {"pic": 0, "pic_err": 0, "single_pic": 0, "bulk_pic": 0}

@app.route('/pi/api/v0.0/documentation')
def documentation():
    #pdb.set_trace()
    abort(403)  #forbidden 
    #return 'documentation TBD'

"""
@app.before_first_request
def exit_gracefully_on_reactor_shutdown():
    reactor.addSystemEventTrigger('after', 'shutdown', os._exit, 0)

def suicide(graceful=False):
    print('halting w grace='.format(graceful))
    if graceful:
        exit_code = 0
    else:
        exit_code = -1
    reactor.addSystemEventTrigger('after', 'shutdown', os._exit, exit_code)  #TODO
    reactor.stop()
"""

@app.route('/pi/api/v0.0/admin/kill') #todo: post only fails?
def kill():
    staydead = request.args.get('staydead')
    if staydead is not None and staydead.lower() == 'true':
        print('graceful shutdown')
        suicide(graceful=True)
        return ('', 204)
    else:
        print('crash stop, restart expected')
        suicide()
        return ('', 204)

@app.route('/pi/api/v0.0/admin/stats')
def stats():
    #pdb.set_trace()
    log = logger.new(request_id=str(uuid.uuid4()),)
    #log.msg('running stats',func='stats')  #No msg with 
    log.info('running stats')
    return (jsonify(metrics), 200)

@app.route('/pi/api/v0.0/admin/status')
def status(): #TODO: how is this differnet from stats
    return ('', 200)

@app.route('/pi/api/v0.0/admin/selftest')
def selftest():
    '''actual functional test to confirm all dependencies are 
    completely working -- lacks timeout'''
    log = logger.new(request_id=str(uuid.uuid4()),)
    #log.msg('running selftest',func='selftest') #Twistd only
    log.info('running selftest',func='selftest')
    res = (pic(.7, .7) == True and pic(.8, .8) == False) #TODO: log esp failures
    return (str(res), 200)

@s.time()
def pic(x,y):
    #global metrics
    metrics['pic'] += 1

    if x is None or y is None:
        metrics['pic_err'] += 1
        abort(500)
    if x > 1 or y > 1:
        metrics['pic_err'] += 1
        abort(500)
    if x < 0 or y < 0:
        metrics['pic_err'] += 1
        abort(500)
    return x**2 + y**2 < 1

@app.route('/pi/api/v0.0/pi_in_circle', methods=['GET'])
def pi_in_circle():
    x = float(request.args.get('x')) if request.args.get('x') else None
    y = float(request.args.get('y')) if request.args.get('y') else None
       
    return jsonify('pi_in_circle {} {} {}'.format(x,y,pic(x,y)))

@app.route('/pi/api/v0.0/bulk_pic', methods=['POST'])
def bulk_pic():
    lpoints = json.loads(request.data)
    res = []
    for p in lpoints:
        res.append(pic(p['x'], p['y']))

    return jsonify(res)

def deleteme():
    print('del this f')

#TODO: add auto-restart
"""
def launch_twistd():
    #TODO: why is this here and not at top?
    from structlog.stdlib import LoggerFactory
    from structlog.threadlocal import wrap_dict
    structlog.configure(context_class=wrap_dict(dict), logger_factory=LoggerFactory())
    #structlog.configure(processors=[EventAdapter()], logger_factory=LoggerFactory())
    structlog.configure(
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.twisted.JSONRenderer()
        ], 
    context_class=dict,
    logger_factory=structlog.twisted.LoggerFactory()),
    wrapper_class=structlog.twisted.BoundLogger,
    cache_logger_on_first_use=True,
    twisted.python.log.startLogging(sys.stderr)

    thread_pool = ThreadPool(maxthreads=10)
    thread_pool.start()
    wsgir = WSGIResource(reactor, thread_pool, app)
    wsgirr = WSGIRootResource(wsgir, {})
    reactor.listenTCP(5000, Site(wsgirr))
    reactor.callWhenRunning(exit_gracefully_on_reactor_shutdown)
    logger.msg('lauching reactor', whom='world')

    prom_root = Resource()
    prom_root.putChild(b'metrics', MetricsResource())
    prom_factory = Site(prom_root)
    reactor.listenTCP(8000, prom_factory)

    reactor.run()
    #logger.msg('reactor down', whom='world')
    #sys.exit(0)
"""

class PrometheusEndpointServer(threading.Thread):
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        super(PrometheusEndpointServer, self).__init__(*args, **kwargs)

    def run(self):
        self.httpd.serve_forever()

def launch_gunicorn():
    from structlog.stdlib import LoggerFactory
    from structlog.threadlocal import wrap_dict
    structlog.configure(context_class=wrap_dict(dict), logger_factory=LoggerFactory())

    structlog.configure_once(
        #processors=chain,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    try:
        httpd = HTTPServer(('0.0.0.0', 8000), MetricsHandler)
    except (OSError, socket.error):
        return

    thread = PrometheusEndpointServer(httpd)
    thread.daemon = True
    thread.start()
    #log.info('Exporting Prometheus metrics on port 8000')

    app.run(host='0.0.0.0')

#def launch_bjoern():
    #bjoern.run(app, '0.0.0.0', 5000)

if __name__ == '__main__':
    #launch_twistd()
    launch_gunicorn()
    #launch_bjoern()
