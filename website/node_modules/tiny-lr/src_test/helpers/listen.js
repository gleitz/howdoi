'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = listen;

var _ = require('../..');

var _supertest = require('supertest');

var _supertest2 = _interopRequireDefault(_supertest);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function listen(opts) {
  opts = opts || {};

  return function _listen(done) {
    var _this = this;

    this.app = new _.Server(opts);
    var srv = this.server = this.app.server;
    var ctx = this;
    this.server.listen(function (err) {
      if (err) return done(err);
      ctx.request = (0, _supertest2.default)(srv).get(_this.app.rootPath).expect(200, done);
    });
  };
};
module.exports = exports['default'];