'use strict';

var _supertest = require('supertest');

var _supertest2 = _interopRequireDefault(_supertest);

var _assert = require('assert');

var _assert2 = _interopRequireDefault(_assert);

var _url = require('url');

var _listen = require('./helpers/listen');

var _listen2 = _interopRequireDefault(_listen);

var _fayeWebsocket = require('faye-websocket');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

describe('tiny-lr', function () {
  before((0, _listen2.default)());
  it('accepts ws clients', function (done) {
    var url = (0, _url.parse)(this.request.url);
    var server = this.app;

    var ws = this.ws = new _fayeWebsocket.Client('ws://' + url.host + '/livereload');

    ws.onopen = function (event) {
      var hello = {
        command: 'hello',
        protocols: ['http://livereload.com/protocols/official-7']
      };

      ws.send(JSON.stringify(hello));
    };

    ws.onmessage = function (event) {
      _assert2.default.deepEqual(event.data, JSON.stringify({
        command: 'hello',
        protocols: ['http://livereload.com/protocols/official-7'],
        serverName: 'tiny-lr'
      }));

      _assert2.default.ok(Object.keys(server.clients).length);
      done();
    };
  });

  it('properly cleans up established connection on exit', function (done) {
    var ws = this.ws;

    ws.onclose = done.bind(null, null);

    (0, _supertest2.default)(this.server).get('/kill').expect(200, function () {});
  });
});