const path    = require('path');
const express = require('express');
const tinylr  = require('../..');
const debug   = require('debug')('tinylr:server');
const gaze    = require('gaze');

process.env.DEBUG = process.env.DEBUG || 'tinylr*';

var app = module.exports = express();

function logger (fmt) {
  fmt = fmt || '%s - %s';

  return function logger (req, res, next) {
    debug(fmt, req.method, req.url);
    next();
  };
}

(function watch (em) {
  em = em || new (require('events').EventEmitter)();

  gaze(path.join(__dirname, 'styles/site.css'), function () {
    this.on('changed', function (filepath) {
      tinylr.changed(filepath);
    });
  });

  return watch;
})();

app
  .use(logger())
  .use('/', express.static(path.join(__dirname)))
  .use(tinylr.middleware({ app: app }));
