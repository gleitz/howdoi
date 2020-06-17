'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _server = require('./server');

var _server2 = _interopRequireDefault(_server);

var _client = require('./client');

var _client2 = _interopRequireDefault(_client);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var debug = require('debug')('tinylr');

// Need to keep track of LR servers when notifying
var servers = [];

exports.default = tinylr;

// Expose Server / Client objects

tinylr.Server = _server2.default;
tinylr.Client = _client2.default;

// and the middleware helpers
tinylr.middleware = middleware;
tinylr.changed = changed;

// Main entry point
function tinylr(opts) {
  var srv = new _server2.default(opts);
  servers.push(srv);
  return srv;
}

// A facade to Server#handle
function middleware(opts) {
  var srv = new _server2.default(opts);
  servers.push(srv);
  return function tinylr(req, res, next) {
    srv.handler(req, res, next);
  };
}

// Changed helper, helps with notifying the server of a file change
function changed(done) {
  var files = [].slice.call(arguments);
  if (typeof files[files.length - 1] === 'function') done = files.pop();
  done = typeof done === 'function' ? done : function () {};
  debug('Notifying %d servers - Files: ', servers.length, files);
  servers.forEach(function (srv) {
    var params = { params: { files: files } };
    srv && srv.changed(params);
  });
  done();
}
module.exports = exports['default'];