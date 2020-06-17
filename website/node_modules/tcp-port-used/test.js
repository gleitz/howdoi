'use strict';
var assert = require('assert');
var tcpPortUsed = require('./index');
var net = require('net');
//var debug = require('debug')('tcp-port-used-test');

var server;

function freePort(cb) {
    if (!server) {
        return cb(new Error('Port not in use'));
    }

    server.close();
    server.unref();
    server = undefined;
    cb();
}

function bindPort(port, cb) {
    if (server) {
        return cb(new Error('Free the server port, first.'));
    }

    server = net.createServer();
    server.listen(port);

    function errEventCb(err) {
        server.close();
        if (cb) {
            rmListeners();
            cb(err);
        }
        server = undefined;
    }

    function listenEventCb() {
        if (cb) {
            rmListeners();
            cb();
        }
    }

    function rmListeners() {
        server.removeListener('error', errEventCb);
        server.removeListener('listening', listenEventCb);
    }

    server.on('error', errEventCb);
    server.on('listening', listenEventCb);
}

describe('check arguments', function() {
    it('should not accept negative port numbers in an obj', function(done) {
        tcpPortUsed.check({ port: -20, host: '127.0.0.1' })
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: -20');
            done();
        });
    });

    it('should not accept negative port numbers', function(done) {
        tcpPortUsed.check(-20, '127.0.0.1')
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: -20');
            done();
        });
    });

    it('should not accept invalid types for port numbers in an obj', function(done) {
        tcpPortUsed.check({port:'hello', host:'127.0.0.1'})
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: \'hello\'');
            done();
        });
    });

    it('should not accept invalid types for port numbers', function(done) {
        tcpPortUsed.check('hello', '127.0.0.1')
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: \'hello\'');
            done();
        });
    });

    it('should require an argument for a port number in an obj', function(done) {
        tcpPortUsed.check({})
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: undefined');
            done();
        });
    });

    it('should require an argument for a port number', function(done) {
        tcpPortUsed.check()
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: undefined');
            done();
        });
    });

    it('should not accept port number > 65535 in an obj', function(done) {
        tcpPortUsed.check({port: 65536})
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: 65536');
            done();
        });
    });


    it('should not accept port number > 65535', function(done) {
        tcpPortUsed.check(65536)
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: 65536');
            done();
        });
    });

    it('should not accept port number < 0 in an obj', function(done) {
        tcpPortUsed.check({port: -1})
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: -1');
            done();
        });
    });

    it('should not accept port number < 0', function(done) {
        tcpPortUsed.check(-1)
        .then(function() {
            done(new Error('check unexpectedly succeeded'));
        }, function(err) {
            assert.ok(err && err.message === 'invalid port: -1');
            done();
        });
    });
});

describe('check functionality for unused port', function() {
    before(function(done) {
        bindPort(44202, function(err) {
            done(err);
        });
    });

    it('should return true for a used port with default host value in an obj', function(done) {
        tcpPortUsed.check({port: 44202})
        .then(function(inUse) {
            assert.ok(inUse === true);
            done();
        }, function(err) {
            done(err);
        });
    });


    it('should return true for a used port with default host value', function(done) {
        tcpPortUsed.check(44202)
        .then(function(inUse) {
            assert.ok(inUse === true);
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should return true for a used port with default host value using arg obj', function(done) {
        tcpPortUsed.check({ port: 44202 })
        .then(function(inUse) {
            assert.ok(inUse === true);
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should return true for a used port with given host value using arg obj', function(done) {
        tcpPortUsed.check({port: 44202, host: '127.0.0.1'})
        .then(function(inUse) {
            assert.ok(inUse === true);
            done();
        }, function(err) {
            assert.ok(false);
            done(err);
        });
    });


    it('should return true for a used port with given host value', function(done) {
        tcpPortUsed.check(44202, '127.0.0.1')
        .then(function(inUse) {
            assert.ok(inUse === true);
            done();
        }, function(err) {
            assert.ok(false);
            done(err);
        });
    });

    it('should return false for an unused port and default host using arg object', function(done) {
        tcpPortUsed.check({port: 44201})
        .then(function(inUse) {
            assert.ok(inUse === false);
            done();
        }, function(err) {
            done(err);
        });
    });


    it('should return false for an unused port and default host', function(done) {
        tcpPortUsed.check(44201)
        .then(function(inUse) {
            assert.ok(inUse === false);
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should return false for an unused port and given default host using arg object', function(done) {
        tcpPortUsed.check({port: 44201, host: '127.0.0.1'})
        .then(function(inUse) {
            assert.ok(inUse === false);
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should return false for an unused port and given default host', function(done) {
        tcpPortUsed.check(44201, '127.0.0.1')
        .then(function(inUse) {
            assert.ok(inUse === false);
            done();
        }, function(err) {
            done(err);
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

describe('waitUntilFreeOnHost', function() {
    this.slow(3000);
    this.timeout(3000);

    before(function(cb) {
        bindPort(44203, function(err) {
            cb(err);
        });
    });

    it('should reject promise for used port number after timeout using an arg obj', function(done) {
        tcpPortUsed.waitUntilFreeOnHost({port:44203, host:'127.0.0.1', retryTimeMs:500, timeOutMs:1000})
        .then(function() {
            done(new Error('waitUntilFreeOnHost unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise for used port number after timeout', function(done) {
        tcpPortUsed.waitUntilFreeOnHost(44203, '127.0.0.1', 500, 1000)
        .then(function() {
            done(new Error('waitUntilFreeOnHost unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should fufill promise for free port number using an arg object', function(done) {
        tcpPortUsed.waitUntilFreeOnHost({port:44205, host:'127.0.0.1', retryTimeMs:500, timeOutM:4000})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });


    it('should fufill promise for free port number', function(done) {
        tcpPortUsed.waitUntilFreeOnHost(44205, '127.0.0.1', 500, 4000)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should fufill promise for free port number and default retry and timeout using an arg obj', function(done) {
        tcpPortUsed.waitUntilFreeOnHost({port:44205})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });


    it('should fufill promise for free port number and default retry and timeout', function(done) {
        tcpPortUsed.waitUntilFreeOnHost(44205)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should reject promise for invalid port number using an arg obj', function(done) {
        tcpPortUsed.waitUntilFreeOnHost({})
        .then(function() {
            done(new Error('waitUntilFreeOnHost unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'invalid port: undefined') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise for invalid port number', function(done) {
        tcpPortUsed.waitUntilFreeOnHost()
        .then(function() {
            done(new Error('waitUntilFreeOnHost unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'invalid port: undefined') {
                done();
            } else {
                done(err);
            }
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

describe('waitUntilUsedOnHost', function() {
    this.timeout(5000);
    this.slow(5000);

    before(function() {
        setTimeout(function() {
            bindPort(44204);
        }, 2000);
    });

    it('should wait until the port is listening using an arg object', function(done) {
        tcpPortUsed.waitUntilUsedOnHost({port:44204, host:'127.0.0.1', retryTimeMs:500, timeOutMs:4000})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should wait until the port is listening', function(done) {
        tcpPortUsed.waitUntilUsedOnHost(44204, '127.0.0.1', 500, 4000)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should reject promise when given an invalid port using an arg object', function(done) {
        tcpPortUsed.waitUntilUsedOnHost({port:'hello', host:'127.0.0.1', retryTimeMs:500, timeOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise when given an invalid port', function(done) {
        tcpPortUsed.waitUntilUsedOnHost('hello', '127.0.0.1', 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should timeout when no port is listening using an arg obj', function(done) {
        tcpPortUsed.waitUntilUsedOnHost({port:44205, host:'127.0.0.1', retryTimeMs:500, tmieOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });


    it('should timeout when no port is listening', function(done) {
        tcpPortUsed.waitUntilUsedOnHost(44205, '127.0.0.1', 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

describe('waitUntilFree', function() {
    this.timeout(8000);
    this.slow(8000);

    before(function(cb) {
        bindPort(44203, function(err) {
            cb(err);
        });
    });

    it('should reject promise for used port number after timeout using arg obj', function(done) {
        this.slow(18000);
        tcpPortUsed.waitUntilFree({port:44203, retryTimeMs:500, timeOutMs:4000})
        .then(function() {
            done(new Error('waitUntilFree unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise for used port number after timeout', function(done) {
        this.slow(18000);
        tcpPortUsed.waitUntilFree(44203, 500, 4000)
        .then(function() {
            done(new Error('waitUntilFree unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should fufill promise for free port number using arg object', function(done) {
        tcpPortUsed.waitUntilFree({port:44205, retryTimeMs:500, timeOutMs:4000})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should fufill promise for free port number', function(done) {
        tcpPortUsed.waitUntilFree(44205, 500, 4000)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should fufill promise for free port number and default retry and timeout using arg object', function(done) {
        tcpPortUsed.waitUntilFree({port: 44205})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should fufill promise for free port number and default retry and timeout', function(done) {
        tcpPortUsed.waitUntilFree(44205)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should reject promise for invalid port number using arg object', function(done) {
        tcpPortUsed.waitUntilFree({})
        .then(function() {
            done(new Error('waitUntilFreeOnHost: unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'invalid port: undefined') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise for invalid port number', function(done) {
        tcpPortUsed.waitUntilFree()
        .then(function() {
            done(new Error('waitUntilFreeOnHost: unexpectedly succeeded'));
        }, function(err) {
            if (err.message === 'invalid port: undefined') {
                done();
            } else {
                done(err);
            }
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

describe('waitUntilUsed', function() {
    this.timeout(5000);
    this.slow(5000);

    before(function() {
        setTimeout(function() {
            bindPort(44204);
        }, 2000);
    });

    it('should wait until the port is listening using arg obj', function(done) {
        tcpPortUsed.waitUntilUsed({port:44204, retryTimeMs:500, timeOutMs:4000})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should wait until the port is listening', function(done) {
        tcpPortUsed.waitUntilUsed(44204, 500, 4000)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should reject promise when given an invalid port using arg object', function(done) {
        tcpPortUsed.waitUntilUsed({port:'hello', retryTimeMs:500, timeOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise when given an invalid port', function(done) {
        tcpPortUsed.waitUntilUsed('hello', 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should timeout when no port is listening using arg obj', function(done) {
        tcpPortUsed.waitUntilUsed({port:44205, retryTimeMs:500, timeOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should timeout when no port is listening', function(done) {
        tcpPortUsed.waitUntilUsed(44205, 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

describe('waitForStatus', function() {
    this.timeout(5000);
    this.slow(5000);

    before(function() {
        setTimeout(function() {
            bindPort(44204);
        }, 2000);
    });

    it('should wait until the port is listening using arg obj', function(done) {
        tcpPortUsed.waitForStatus({port:44204, host:'127.0.0.1', inUse:true, retryTimeMs:500, timeOutMs:4000})
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should wait until the port is listening', function(done) {
        tcpPortUsed.waitForStatus(44204, '127.0.0.1', true, 500, 4000)
        .then(function() {
            done();
        }, function(err) {
            done(err);
        });
    });

    it('should reject promise when given an invalid port using arg object', function(done) {
        tcpPortUsed.waitForStatus({port:'hello', host:'127.0.0.1', inUse:false, retryTimeMs:500, timeOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should reject promise when given an invalid port', function(done) {
        tcpPortUsed.waitForStatus('hello', '127.0.0.1', false, 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'invalid port: \'hello\'') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should timeout when no port is listening using arg obj', function(done) {
        tcpPortUsed.waitUntilUsed({port:44205, host:'127.0.0.1', inUse:true, retryTimeMs:500, timeOutMs:2000})
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    it('should timeout when no port is listening', function(done) {
        tcpPortUsed.waitUntilUsed(44205, '127.0.0.1', true, 500, 2000)
        .then(function() {
            done(new Error('waitUntil used unexpectedly successful.'));
        }, function(err) {
            if (err.message === 'timeout') {
                done();
            } else {
                done(err);
            }
        });
    });

    after(function(cb) {
        freePort(function(err) {
            cb(err);
        });
    });
});

