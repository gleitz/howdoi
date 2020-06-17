'use strict';

var _supertest = require('supertest');

var _supertest2 = _interopRequireDefault(_supertest);

var _assert = require('assert');

var _assert2 = _interopRequireDefault(_assert);

var _listen = require('./helpers/listen');

var _listen2 = _interopRequireDefault(_listen);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function testRoutes() {
  var _ref = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

  var _ref$prefix = _ref.prefix;
  var prefix = _ref$prefix === undefined ? '' : _ref$prefix;

  var buildUrl = function buildUrl(url) {
    return prefix ? '/' + prefix + url : url;
  };

  describe('GET /', function () {
    it('respond with nothing, but respond', function (done) {
      (0, _supertest2.default)(this.server).get(buildUrl('/')).expect('Content-Type', /json/).expect(/\{"tinylr":"Welcome","version":"[\d].[\d].[\d]+"\}/).expect(200, done);
    });

    it('unknown route respond with proper 404 and error message', function (done) {
      (0, _supertest2.default)(this.server).get(buildUrl('/whatev')).expect('Content-Type', /json/).expect('{"error":"not_found","reason":"no such route"}').expect(404, done);
    });
  });

  describe('GET /changed', function () {
    it('with no clients, no files', function (done) {
      (0, _supertest2.default)(this.server).get(buildUrl('/changed')).expect('Content-Type', /json/).expect(/"clients":\[\]/).expect(/"files":\[\]/).expect(200, done);
    });

    it('with no clients, some files', function (done) {
      (0, _supertest2.default)(this.server).get(buildUrl('/changed?files=gonna.css,test.css,it.css')).expect('Content-Type', /json/).expect('{"clients":[],"files":["gonna.css","test.css","it.css"]}').expect(200, done);
    });
  });

  describe('POST /changed', function () {
    it('with no clients, no files', function (done) {
      (0, _supertest2.default)(this.server).post(buildUrl('/changed')).expect('Content-Type', /json/).expect(/"clients":\[\]/).expect(/"files":\[\]/).expect(200, done);
    });

    it('with no clients, some files', function (done) {
      var data = { clients: [], files: ['cat.css', 'sed.css', 'ack.js'] };

      (0, _supertest2.default)(this.server).post(buildUrl('/changed'))
      // .type('json')
      .send({ files: data.files }).expect('Content-Type', /json/).expect(JSON.stringify(data)).expect(200, done);
    });
  });

  describe('POST /alert', function () {
    it('with no clients, no message', function (done) {
      var data = { clients: [] };
      (0, _supertest2.default)(this.server).post(buildUrl('/alert')).expect('Content-Type', /json/).expect(JSON.stringify(data)).expect(200, done);
    });

    it('with no clients, some message', function (done) {
      var message = 'Hello Client!';
      var data = { clients: [], message: message };
      (0, _supertest2.default)(this.server).post(buildUrl('/alert')).send({ message: message }).expect('Content-Type', /json/).expect(JSON.stringify(data)).expect(200, done);
    });
  });

  describe('GET /livereload.js', function () {
    it('respond with livereload script', function (done) {
      (0, _supertest2.default)(this.server).get(buildUrl('/livereload.js')).expect(/LiveReload/).expect(200, done);
    });
  });

  describe('GET /kill', function () {
    it('shutdown the server', function (done) {
      var srv = this.server;
      (0, _supertest2.default)(srv).get(buildUrl('/kill')).expect(200, function (err) {
        if (err) return done(err);
        _assert2.default.ok(!srv._handle);
        done();
      });
    });
  });
}

describe('Server', function () {
  context('with no options', function () {
    before((0, _listen2.default)());
    testRoutes();
  });

  context('with prefix option', function () {
    var options = {
      prefix: 'tiny-lr'
    };

    before((0, _listen2.default)(options));
    testRoutes(options);
  });
});