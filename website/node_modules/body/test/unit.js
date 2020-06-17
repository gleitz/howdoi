var after = require('after');
var body = require('../index.js');
var hammock = require('hammock');
var test = require('tape');

test('caching works', function t(assert) {
    var request = hammock.Request({
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        url: '/somewhere'
    });
    var response = hammock.Response();

    var done = after(2, assert.end.bind(assert));

    body(request, response, { cache: true }, function onBody(err, body) {
        assert.equal(body, 'thisbody', 'raw body has been set');
        assert.pass('body is parsed');
        done();
    });

    request.on('end', function() {
        body(request, response, { cache: true }, function onBody(err, body) {
            assert.equal(body, 'thisbody', 'cached body is provided');
            assert.pass('body is parsed');
            done();
        });
    });

    request.end('thisbody');
});

test('parallel caching works', function t(assert) {
    var request = hammock.Request({
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        url: '/somewhere'
    });
    request.end('thisbody');
    var response = hammock.Response();

    var done = after(5, function() {
        process.nextTick(function() {
            assert.equal(request.listeners('rawBody').length, 0, 'rawBody listeners cleared');
            assert.end();
        });
    });

    for (var i = 0; i < 5; ++i) {
        body(request, response, { cache: true }, function onBody(err, body) {
            assert.equal(body, 'thisbody', 'raw body has been set');
            assert.pass('body is parsed');
            done();
        });
    }
});
