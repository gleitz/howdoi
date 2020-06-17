'use strict';

var _app = require('../examples/express/app');

var _app2 = _interopRequireDefault(_app);

var _supertest = require('supertest');

var _supertest2 = _interopRequireDefault(_supertest);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

describe('mocha spec examples', function () {
  describe('tinylr', function () {
    it('GET /', function (done) {
      (0, _supertest2.default)(_app2.default).get('/').expect('Content-Type', /text\/html/).expect(/Testing/).expect(200, done);
    });
  });
});