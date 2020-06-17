'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _events = require('events');

var _events2 = _interopRequireDefault(_events);

var _fayeWebsocket = require('faye-websocket');

var _fayeWebsocket2 = _interopRequireDefault(_fayeWebsocket);

var _objectAssign = require('object-assign');

var _objectAssign2 = _interopRequireDefault(_objectAssign);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var debug = require('debug')('tinylr:client');

var idCounter = 0;

var Client = function (_events$EventEmitter) {
  _inherits(Client, _events$EventEmitter);

  function Client(req, socket, head) {
    var options = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : {};

    _classCallCheck(this, Client);

    var _this = _possibleConstructorReturn(this, (Client.__proto__ || Object.getPrototypeOf(Client)).call(this));

    _this.options = options;
    _this.ws = new _fayeWebsocket2.default(req, socket, head);
    _this.ws.onmessage = _this.message.bind(_this);
    _this.ws.onclose = _this.close.bind(_this);
    _this.id = _this.uniqueId('ws');
    return _this;
  }

  _createClass(Client, [{
    key: 'message',
    value: function message(event) {
      var data = this.data(event);
      if (this[data.command]) return this[data.command](data);
    }
  }, {
    key: 'close',
    value: function close(event) {
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }

      this.emit('end', event);
    }

    // Commands

  }, {
    key: 'hello',
    value: function hello() {
      this.send({
        command: 'hello',
        protocols: ['http://livereload.com/protocols/official-7'],
        serverName: 'tiny-lr'
      });
    }
  }, {
    key: 'info',
    value: function info(data) {
      if (data) {
        debug('Info', data);
        this.emit('info', (0, _objectAssign2.default)({}, data, { id: this.id }));
        this.plugins = data.plugins;
        this.url = data.url;
      }

      return (0, _objectAssign2.default)({}, data || {}, { id: this.id, url: this.url });
    }

    // Server commands

  }, {
    key: 'reload',
    value: function reload(files) {
      files.forEach(function (file) {
        this.send({
          command: 'reload',
          path: file,
          liveCSS: this.options.liveCSS !== false,
          reloadMissingCSS: this.options.reloadMissingCSS !== false,
          liveImg: this.options.liveImg !== false
        });
      }, this);
    }
  }, {
    key: 'alert',
    value: function alert(message) {
      this.send({
        command: 'alert',
        message: message
      });
    }

    // Utilities

  }, {
    key: 'data',
    value: function data(event) {
      var data = {};
      try {
        data = JSON.parse(event.data);
      } catch (e) {}
      return data;
    }
  }, {
    key: 'send',
    value: function send(data) {
      if (!this.ws) return;
      this.ws.send(JSON.stringify(data));
    }
  }, {
    key: 'uniqueId',
    value: function uniqueId(prefix) {
      var id = idCounter++;
      return prefix ? prefix + id : id;
    }
  }]);

  return Client;
}(_events2.default.EventEmitter);

exports.default = Client;
module.exports = exports['default'];