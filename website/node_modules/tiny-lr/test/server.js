import request from 'supertest';
import assert from 'assert';
import listen from './helpers/listen';

function testRoutes ({ prefix = '' } = {}) {
  const buildUrl = url => prefix ? `/${prefix}${url}` : url;

  describe('GET /', function () {
    it('respond with nothing, but respond', function (done) {
      request(this.server)
        .get(buildUrl('/'))
        .expect('Content-Type', /json/)
        .expect(/\{"tinylr":"Welcome","version":"[\d].[\d].[\d]+"\}/)
        .expect(200, done);
    });

    it('unknown route respond with proper 404 and error message', function (done) {
      request(this.server)
        .get(buildUrl('/whatev'))
        .expect('Content-Type', /json/)
        .expect('{"error":"not_found","reason":"no such route"}')
        .expect(404, done);
    });
  });

  describe('GET /changed', function () {
    it('with no clients, no files', function (done) {
      request(this.server)
        .get(buildUrl('/changed'))
        .expect('Content-Type', /json/)
        .expect(/"clients":\[\]/)
        .expect(/"files":\[\]/)
        .expect(200, done);
    });

    it('with no clients, some files', function (done) {
      request(this.server)
        .get(buildUrl('/changed?files=gonna.css,test.css,it.css'))
        .expect('Content-Type', /json/)
        .expect('{"clients":[],"files":["gonna.css","test.css","it.css"]}')
        .expect(200, done);
    });
  });

  describe('POST /changed', function () {
    it('with no clients, no files', function (done) {
      request(this.server)
        .post(buildUrl('/changed'))
        .expect('Content-Type', /json/)
        .expect(/"clients":\[\]/)
        .expect(/"files":\[\]/)
        .expect(200, done);
    });

    it('with no clients, some files', function (done) {
      const data = { clients: [], files: ['cat.css', 'sed.css', 'ack.js'] };

      request(this.server)
        .post(buildUrl('/changed'))
        // .type('json')
        .send({ files: data.files })
        .expect('Content-Type', /json/)
        .expect(JSON.stringify(data))
        .expect(200, done);
    });
  });

  describe('POST /alert', function () {
    it('with no clients, no message', function (done) {
      const data = { clients: [] };
      request(this.server)
        .post(buildUrl('/alert'))
        .expect('Content-Type', /json/)
        .expect(JSON.stringify(data))
        .expect(200, done);
    });

    it('with no clients, some message', function (done) {
      const message = 'Hello Client!';
      const data = { clients: [], message: message };
      request(this.server)
        .post(buildUrl('/alert'))
        .send({ message: message })
        .expect('Content-Type', /json/)
        .expect(JSON.stringify(data))
        .expect(200, done);
    });
  });

  describe('GET /livereload.js', function () {
    it('respond with livereload script', function (done) {
      request(this.server)
        .get(buildUrl('/livereload.js'))
        .expect(/LiveReload/)
        .expect(200, done);
    });
  });

  describe('GET /kill', function () {
    it('shutdown the server', function (done) {
      const srv = this.server;
      request(srv)
        .get(buildUrl('/kill'))
        .expect(200, err => {
          if (err) return done(err);
          assert.ok(!srv._handle);
          done();
        });
    });
  });
}

describe('Server', () => {
  context('with no options', function () {
    before(listen());
    testRoutes();
  });

  context('with prefix option', function () {
    const options = {
      prefix: 'tiny-lr'
    };

    before(listen(options));
    testRoutes(options);
  });
});
