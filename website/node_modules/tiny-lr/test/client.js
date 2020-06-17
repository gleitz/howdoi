
import request from 'supertest';
import assert from 'assert';
import {parse} from 'url';
import listen from './helpers/listen';
import {Client as WebSocket} from 'faye-websocket';

describe('tiny-lr', () => {
  before(listen());
  it('accepts ws clients', function (done) {
    const url = parse(this.request.url);
    const server = this.app;

    const ws = this.ws = new WebSocket('ws://' + url.host + '/livereload');

    ws.onopen = event => {
      const hello = {
        command: 'hello',
        protocols: ['http://livereload.com/protocols/official-7']
      };

      ws.send(JSON.stringify(hello));
    };

    ws.onmessage = event => {
      assert.deepEqual(event.data, JSON.stringify({
        command: 'hello',
        protocols: ['http://livereload.com/protocols/official-7'],
        serverName: 'tiny-lr'
      }));

      assert.ok(Object.keys(server.clients).length);
      done();
    };
  });

  it('properly cleans up established connection on exit', function (done) {
    const ws = this.ws;

    ws.onclose = done.bind(null, null);

    request(this.server)
      .get('/kill')
      .expect(200, () => {});
  });
});
