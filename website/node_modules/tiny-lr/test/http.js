import app from '../examples/express/app';
import request from 'supertest';

describe('mocha spec examples', () => {
  describe('tinylr', () => {
    it('GET /', done => {
      request(app)
        .get('/')
        .expect('Content-Type', /text\/html/)
        .expect(/Testing/)
        .expect(200, done);
    });
  });
});
