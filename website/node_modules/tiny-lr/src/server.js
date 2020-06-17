'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

var _http = require('http');

var _http2 = _interopRequireDefault(_http);

var _https = require('https');

var _https2 = _interopRequireDefault(_https);

var _events = require('events');

var _events2 = _interopRequireDefault(_events);

var _url = require('url');

var _client = require('./client');

var _client2 = _interopRequireDefault(_client);

var _package = require('../package.json');

var _package2 = _interopRequireDefault(_package);

var _any = require('body/any');

var _any2 = _interopRequireDefault(_any);

var _qs = require('qs');

var _qs2 = _interopRequireDefault(_qs);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = require('debug')('tinylr:server');

var CONTENT_TYPE = 'content-type';
var FORM_TYPE = 'application/x-www-form-urlencoded';

function buildRootPath() {
  var prefix = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '/';

  var rootUrl = prefix;

  // Add trailing slash
  if (prefix[prefix.length - 1] !== '/') {
    rootUrl = rootUrl + '/';
  }

  // Add leading slash
  if (prefix[0] !== '/') {
    rootUrl = '/' + rootUrl;
  }

  return rootUrl;
}

var Server = function (_events$EventEmitter) {
  _inherits(Server, _events$EventEmitter);

  function Server() {
    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

    _classCallCheck(this, Server);

    var _this = _possibleConstructorReturn(this, (Server.__proto__ || Object.getPrototypeOf(Server)).call(this));

    _this.options = options;

    options.livereload = options.livereload || require.resolve('livereload-js/dist/livereload.js');

    // todo: change falsy check to allow 0 for random port
    options.port = parseInt(options.port || 35729, 10);

    if (options.errorListener) {
      _this.errorListener = options.errorListener;
    }

    _this.rootPath = buildRootPath(options.prefix);

    _this.clients = {};
    _this.configure(options.app);
    _this.routes(options.app);
    return _this;
  }

  _createClass(Server, [{
    key: 'routes',
    value: function routes() {
      if (!this.options.dashboard) {
        this.on('GET ' + this.rootPath, this.index.bind(this));
      }

      this.on('GET ' + this.rootPath + 'changed', this.changed.bind(this));
      this.on('POST ' + this.rootPath + 'changed', this.changed.bind(this));
      this.on('POST ' + this.rootPath + 'alert', this.alert.bind(this));
      this.on('GET ' + this.rootPath + 'livereload.js', this.livereload.bind(this));
      this.on('GET ' + this.rootPath + 'kill', this.close.bind(this));
    }
  }, {
    key: 'configure',
    value: function configure(app) {
      var _this2 = this;

      debug('Configuring %s', app ? 'connect / express application' : 'HTTP server');

      var handler = this.options.handler || this.handler;

      if (!app) {
        if (this.options.key && this.options.cert || this.options.pfx) {
          this.server = _https2.default.createServer(this.options, handler.bind(this));
        } else {
          this.server = _http2.default.createServer(handler.bind(this));
        }

        this.server.on('upgrade', this.websocketify.bind(this));
        this.server.on('error', this.error.bind(this));
        return this;
      }

      this.app = app;
      this.app.listen = function (port, done) {
        done = done || function () {};
        if (port !== _this2.options.port) {
          debug('Warn: LiveReload port is not standard (%d). You are listening on %d', _this2.options.port, port);
          debug('You\'ll need to rely on the LiveReload snippet');
          debug('> http://feedback.livereload.com/knowledgebase/articles/86180-how-do-i-add-the-script-tag-manually-');
        }

        var srv = _this2.server = _http2.default.createServer(app);
        srv.on('upgrade', _this2.websocketify.bind(_this2));
        srv.on('error', _this2.error.bind(_this2));
        srv.on('close', _this2.close.bind(_this2));
        return srv.listen(port, done);
      };

      return this;
    }
  }, {
    key: 'handler',
    value: function handler(req, res, next) {
      var _this3 = this;

      var middleware = typeof next === 'function';
      debug('LiveReload handler %s (middleware: %s)', req.url, middleware ? 'on' : 'off');

      next = next || this.defaultHandler.bind(this, res);
      req.headers[CONTENT_TYPE] = req.headers[CONTENT_TYPE] || FORM_TYPE;
      return (0, _any2.default)(req, res, function (err, body) {
        if (err) return next(err);
        req.body = body;

        if (!req.query) {
          req.query = req.url.indexOf('?') !== -1 ? _qs2.default.parse((0, _url.parse)(req.url).query) : {};
        }

        return _this3.handle(req, res, next);
      });
    }
  }, {
    key: 'index',
    value: function index(req, res) {
      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify({
        tinylr: 'Welcome',
        version: _package2.default.version
      }));

      res.end();
    }
  }, {
    key: 'handle',
    value: function handle(req, res, next) {
      var url = (0, _url.parse)(req.url);
      debug('Request:', req.method, url.href);
      var middleware = typeof next === 'function';

      // do the routing
      var route = req.method + ' ' + url.pathname;
      var respond = this.emit(route, req, res);
      if (respond) return;

      if (middleware) return next();

      // Only apply content-type on non middleware setup #70
      return this.notFound(res);
    }
  }, {
    key: 'defaultHandler',
    value: function defaultHandler(res, err) {
      if (!err) return this.notFound(res);

      this.error(err);
      res.setHeader('Content-Type', 'text/plain');
      res.statusCode = 500;
      res.end('Error: ' + err.stack);
    }
  }, {
    key: 'notFound',
    value: function notFound(res) {
      res.setHeader('Content-Type', 'application/json');
      res.writeHead(404);
      res.write(JSON.stringify({
        error: 'not_found',
        reason: 'no such route'
      }));
      res.end();
    }
  }, {
    key: 'websocketify',
    value: function websocketify(req, socket, head) {
      var _this4 = this;

      var client = new _client2.default(req, socket, head, this.options);
      this.clients[client.id] = client;

      // handle socket error to prevent possible app crash, such as ECONNRESET
      socket.on('error', function (e) {
        // ignore frequent ECONNRESET error (seems inevitable when refresh)
        if (e.code === 'ECONNRESET') return;
        _this4.error(e);
      });

      client.once('info', function (data) {
        debug('Create client %s (url: %s)', data.id, data.url);
        _this4.emit('MSG /create', data.id, data.url);
      });

      client.once('end', function () {
        debug('Destroy client %s (url: %s)', client.id, client.url);
        _this4.emit('MSG /destroy', client.id, client.url);
        delete _this4.clients[client.id];
      });
    }
  }, {
    key: 'listen',
    value: function listen(port, host, fn) {
      port = port || this.options.port;

      // Last used port for error display
      this.port = port;

      if (typeof host === 'function') {
        fn = host;
        host = undefined;
      }

      this.server.listen(port, host, fn);
    }
  }, {
    key: 'close',
    value: function close(req, res) {
      Object.keys(this.clients).forEach(function (id) {
        this.clients[id].close();
      }, this);

      if (this.server._handle) this.server.close(this.emit.bind(this, 'close'));

      if (res) res.end();
    }
  }, {
    key: 'error',
    value: function error(e) {
      if (this.errorListener) {
        this.errorListener(e);
        return;
      }

      console.error();
      if (typeof e === 'undefined') {
        console.error('... Uhoh. Got error %s ...', e);
      } else {
        console.error('... Uhoh. Got error %s ...', e.message);
        console.error(e.stack);

        if (e.code !== 'EADDRINUSE') return;
        console.error();
        console.error('You already have a server listening on %s', this.port);
        console.error('You should stop it and try again.');
        console.error();
      }
    }

    // Routes

  }, {
    key: 'livereload',
    value: function livereload(req, res) {
      res.setHeader('Content-Type', 'application/javascript');
      _fs2.default.createReadStream(this.options.livereload).pipe(res);
    }
  }, {
    key: 'changed',
    value: function changed(req, res) {
      var files = this.param('files', req);

      debug('Changed event (Files: %s)', files.join(' '));
      var clients = this.notifyClients(files);

      if (!res) return;

      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify({
        clients: clients,
        files: files
      }));

      res.end();
    }
  }, {
    key: 'alert',
    value: function alert(req, res) {
      var message = this.param('message', req);

      debug('Alert event (Message: %s)', message);
      var clients = this.alertClients(message);

      if (!res) return;

      res.setHeader('Content-Type', 'application/json');
      res.write(JSON.stringify({
        clients: clients,
        message: message
      }));

      res.end();
    }
  }, {
    key: 'notifyClients',
    value: function notifyClients(files) {
      var clients = Object.keys(this.clients).map(function (id) {
        var client = this.clients[id];
        debug('Reloading client %s (url: %s)', client.id, client.url);
        client.reload(files);
        return {
          id: client.id,
          url: client.url
        };
      }, this);

      return clients;
    }
  }, {
    key: 'alertClients',
    value: function alertClients(message) {
      var clients = Object.keys(this.clients).map(function (id) {
        var client = this.clients[id];
        debug('Alert client %s (url: %s)', client.id, client.url);
        client.alert(message);
        return {
          id: client.id,
          url: client.url
        };
      }, this);

      return clients;
    }

    // Lookup param from body / params / query.

  }, {
    key: 'param',
    value: function param(name, req) {
      var param = void 0;
      if (req.body && req.body[name]) param = req.body[name];else if (req.params && req.params[name]) param = req.params[name];else if (req.query && req.query[name]) param = req.query[name];

      // normalize files array
      if (name === 'files') {
        param = Array.isArray(param) ? param : typeof param === 'string' ? param.split(/[\s,]/) : [];
      }

      return param;
    }
  }]);

  return Server;
}(_events2.default.EventEmitter);

exports.default = Server;
module.exports = exports['default'];