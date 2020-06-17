const port = process.env.LR_PORT || process.env.PORT || 35729;

process.env.DEBUG = process.env.DEBUG || 'tinylr*';
const debug = require('debug')('tinylr:server');

const app = require('./app');

debug('Starting server');
app.listen(port, function (err) {
  if (err) throw err;
  debug('listening on %d', port);
});
