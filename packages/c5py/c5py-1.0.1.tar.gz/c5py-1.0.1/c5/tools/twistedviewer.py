import sys

from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor, endpoints
from twisted.web.util import redirectTo
from twisted.python.url import URL
from twisted.python import log
from twisted.web.resource import Resource
from ..config import STUDIES_FOLDER

# compatibility (Python 2/3) wrapper for unicode function
try:
    type(unicode)
except NameError:
    unicode = str


class Redirect(Resource):
    def __init__(self, target=u'', port=8080, params=[]):
        super(Redirect, self).__init__()
        self.target = target
        self.params = params
        self.port = port

    def render_GET(self, request):
        request.args = self.params
        url = URL(scheme=u'http', host=u'localhost', path=self.target.split('/'),
                  port=self.port, query=self.params)
        return redirectTo(url.asText().encode('utf-8'), request)


class ContentHandler(Resource):

    def __init__(self, app, stage1, stage2):
        self.stage1 = stage1
        self.stage2 = File(stage2)

    def getChildWithDefault(self, path, request):
        path = unicode(path)
        print("GET SUBPATH:", path)
        print("RQ", request.args)
        if 'stage1' in path:
            tid = int(request.args[b'tid'][-1])
            s1f = File("{0}/{1}/trial{2}".format(
                self.stage1, STUDIES_FOLDER[tid // 100 - 1], tid))
            print(s1f.path)
            return s1f
        if 'stage2' in path:
            print(self.stage2.path)
            return self.stage2

    def render_GET(self, request):
        return ""


class Handler(Resource):
    def __init__(self, app, stage1, stage2, port, params=[]):
        self.app = File(app)
        self.js = File(app + '/js')
        self.css = File(app + '/css')
        self.content = ContentHandler(app, stage1, stage2)
        self.redirect = Redirect(target=u'player', port=port, params=params)

    def getChildWithDefault(self, path, request):
        path = unicode(path)
        print("GET PATH:", path)
        if 'data' in path:
            return self.content
        if 'js' in path:
            print(self.js.path)
            return self.js
        if 'css' in path:
            print(self.css.path)
            return self.css
        if 'player' in path:
            return self.app
        return self.redirect


def serve_app(args):
    log.startLogging(sys.stdout)
    log.msg("Will serve from:", args.serve_path)
    log.msg("Expect sensor data at:", args.stage1)
    log.msg("Expect derived data at:", args.stage2)
    log.msg("Trial ID is:", args.tid)
    resource = Handler(app=args.serve_path, stage1=args.stage1, stage2=args.stage2, port=args.port,
                       params=[(u'tid', unicode(args.tid))])
    factory = Site(resource)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, args.port)
    endpoint.listen(factory)
    return reactor
