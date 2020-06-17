/**
 * @fileOverview
 * A simple promises-based check to see if a TCP port is already in use.
 */
'use strict';

// define the exports first to avoid cyclic dependencies.
exports.check = check;
exports.waitUntilFreeOnHost = waitUntilFreeOnHost;
exports.waitUntilFree = waitUntilFree;
exports.waitUntilUsedOnHost = waitUntilUsedOnHost;
exports.waitUntilUsed = waitUntilUsed;
exports.waitForStatus = waitForStatus;

var is = require('is2');
var net = require('net');
var util = require('util');
var debug = require('debug')('tcp-port-used');

// Global Values
var TIMEOUT = 2000;
var RETRYTIME = 250;

function getDeferred() {
    var resolve, reject, promise = new Promise(function(res, rej) {
        resolve = res;
        reject = rej;
    });

    return {
        resolve: resolve,
        reject: reject,
        promise: promise
    };
}

/**
 * Creates an options object from all the possible arguments
 * @private
 * @param {Number} port a valid TCP port number
 * @param {String} host The DNS name or IP address.
 * @param {Boolean} status The desired in use status to wait for: false === not in use, true === in use
 * @param {Number} retryTimeMs the retry interval in milliseconds - defaultis is 200ms
 * @param {Number} timeOutMs the amount of time to wait until port is free default is 1000ms
 * @return {Object} An options object with all the above parameters as properties.
 */
function makeOptionsObj(port, host, inUse, retryTimeMs, timeOutMs) {
    var opts = {};
    opts.port = port;
    opts.host = host;
    opts.inUse = inUse;
    opts.retryTimeMs = retryTimeMs;
    opts.timeOutMs = timeOutMs;
    return opts;
}

/**
 * Checks if a TCP port is in use by creating the socket and binding it to the
 * target port. Once bound, successfully, it's assume the port is availble.
 * After the socket is closed or in error, the promise is resolved.
 * Note: you have to be super user to correctly test system ports (0-1023).
 * @param {Number|Object} port The port you are curious to see if available. If an object, must have the parameters as properties.
 * @param {String} [host] May be a DNS name or IP address. Default '127.0.0.1'
 * @return {Object} A deferred Q promise.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.check(22, '127.0.0.1')
 * .then(function(inUse) {
 *    debug('Port 22 usage: '+inUse);
 * }, function(err) {
 *    console.error('Error on check: '+util.inspect(err));
 * });
 */
function check(port, host) {

    var deferred = getDeferred();
    var inUse = true;
    var client;

    var opts;
    if (!is.obj(port)) {
        opts = makeOptionsObj(port, host);
    } else {
        opts = port;
    }

    if (!is.port(opts.port)) {
        debug('Error invalid port: '+util.inspect(opts.port));
        deferred.reject(new Error('invalid port: '+util.inspect(opts.port)));
        return deferred.promise;
    }

    if (is.nullOrUndefined(opts.host)) {
        debug('set host address to default 127.0.0.1');
        opts.host = '127.0.0.1';
    }

    function cleanUp() {
        if (client) {
            client.removeAllListeners('connect');
            client.removeAllListeners('error');
            client.end();
            client.destroy();
            client.unref();
        }
        //debug('listeners removed from client socket');
    }

    function onConnectCb() {
        //debug('check - promise resolved - in use');
        deferred.resolve(inUse);
        cleanUp();
    }

    function onErrorCb(err) {
        if (err.code !== 'ECONNREFUSED') {
            //debug('check - promise rejected, error: '+err.message);
            deferred.reject(err);
        } else {
            //debug('ECONNREFUSED');
            inUse = false;
            //debug('check - promise resolved - not in use');
            deferred.resolve(inUse);
        }
        cleanUp();
    }

    client = new net.Socket();
    client.once('connect', onConnectCb);
    client.once('error', onErrorCb);
    client.connect({port: opts.port, host: opts.host}, function() {});

    return deferred.promise;
}

/**
 * Creates a deferred promise and fulfills it only when the socket's usage
 * equals status in terms of 'in use' (false === not in use, true === in use).
 * Will retry on an interval specified in retryTimeMs.  Note: you have to be
 * super user to correctly test system ports (0-1023).
 * @param {Number|Object} port a valid TCP port number, if an object, has all the parameters described as properties.
 * @param {String} host The DNS name or IP address.
 * @param {Boolean} status The desired in use status to wait for false === not in use, true === in use
 * @param {Number} [retryTimeMs] the retry interval in milliseconds - defaultis is 200ms
 * @param {Number} [timeOutMs] the amount of time to wait until port is free default is 1000ms
 * @return {Object} A deferred promise from the Q library.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.waitForStatus(44204, 'some.host.com', true, 500, 4000)
 * .then(function() {
 *     console.log('Port 44204 is now in use.');
 * }, function(err) {
 *     console.log('Error: ', error.message);
 * });
 */
function waitForStatus(port, host, inUse, retryTimeMs, timeOutMs) {

    var deferred = getDeferred();
    var timeoutId;
    var timedout = false;
    var retryId;

    // the first arument may be an object, if it is not, make an object
    var opts;
    if (is.obj(port)) {
        opts = port;
    } else {
        opts = makeOptionsObj(port, host, inUse, retryTimeMs, timeOutMs);
    }

    //debug('opts:'+util.inspect(opts);

    if (!is.bool(opts.inUse)) {
        deferred.reject(new Error('inUse must be a boolean'));
        return deferred.promise;
    }

    if (!is.positiveInt(opts.retryTimeMs)) {
        opts.retryTimeMs = RETRYTIME;
        debug('set retryTime to default '+RETRYTIME+'ms');
    }

    if (!is.positiveInt(opts.timeOutMs)) {
        opts.timeOutMs = TIMEOUT;
        debug('set timeOutMs to default '+TIMEOUT+'ms');
    }

    function cleanUp() {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        if (retryId) {
            clearTimeout(retryId);
        }
    }

    function timeoutFunc() {
        timedout = true;
        cleanUp();
        deferred.reject(new Error('timeout'));
    }
    timeoutId = setTimeout(timeoutFunc, opts.timeOutMs);

    function doCheck() {
        check(opts.port, opts.host)
        .then(function(inUse) {
            if (timedout) {
                return;
            }
            //debug('doCheck inUse: '+inUse);
            //debug('doCheck opts.inUse: '+opts.inUse);
            if (inUse === opts.inUse) {
                deferred.resolve();
                cleanUp();
                return;
            } else {
                retryId = setTimeout(function() { doCheck(); }, opts.retryTimeMs);
                return;
            }
        }, function(err) {
            if (timedout) {
                return;
            }
            deferred.reject(err);
            cleanUp();
        });
    }

    doCheck();
    return deferred.promise;
}

/**
 * Creates a deferred promise and fulfills it only when the socket is free.
 * Will retry on an interval specified in retryTimeMs.
 * Note: you have to be super user to correctly test system ports (0-1023).
 * @param {Number} port a valid TCP port number
 * @param {String} [host] The hostname or IP address of where the socket is.
 * @param {Number} [retryTimeMs] the retry interval in milliseconds - defaultis is 100ms.
 * @param {Number} [timeOutMs] the amount of time to wait until port is free. Default 300ms.
 * @return {Object} A deferred promise from the q library.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.waitUntilFreeOnHost(44203, 'some.host.com', 500, 4000)
 * .then(function() {
 *     console.log('Port 44203 is now free.');
 *  }, function(err) {
 *     console.loh('Error: ', error.message);
 *  });
 */
function waitUntilFreeOnHost(port, host, retryTimeMs, timeOutMs) {

    // the first arument may be an object, if it is not, make an object
    var opts;
    if (is.obj(port)) {
        opts = port;
        opts.inUse = false;
    } else {
        opts = makeOptionsObj(port, host, false, retryTimeMs, timeOutMs);
    }

    return waitForStatus(opts);
}

/**
 * For compatibility with previous version of the module, that did not provide
 * arguements for hostnames. The host is set to the localhost '127.0.0.1'.
 * @param {Number|Object} port a valid TCP port number. If an object, must contain all the parameters as properties.
 * @param {Number} [retryTimeMs] the retry interval in milliseconds - defaultis is 100ms.
 * @param {Number} [timeOutMs] the amount of time to wait until port is free. Default 300ms.
 * @return {Object} A deferred promise from the q library.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.waitUntilFree(44203, 500, 4000)
 * .then(function() {
 *     console.log('Port 44203 is now free.');
 *  }, function(err) {
 *     console.loh('Error: ', error.message);
 *  });
 */
function waitUntilFree(port, retryTimeMs, timeOutMs) {

    // the first arument may be an object, if it is not, make an object
    var opts;
    if (is.obj(port)) {
        opts = port;
        opts.host = '127.0.0.1';
        opts.inUse = false;
    } else {
        opts = makeOptionsObj(port, '127.0.0.1', false, retryTimeMs, timeOutMs);
    }

    return waitForStatus(opts);
}

/**
 * Creates a deferred promise and fulfills it only when the socket is used.
 * Will retry on an interval specified in retryTimeMs.
 * Note: you have to be super user to correctly test system ports (0-1023).
 * @param {Number|Object} port a valid TCP port number. If an object, must contain all the parameters as properties.
 * @param {Number} [retryTimeMs] the retry interval in milliseconds - defaultis is 500ms
 * @param {Number} [timeOutMs] the amount of time to wait until port is free
 * @return {Object} A deferred promise from the q library.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.waitUntilUsedOnHost(44204, 'some.host.com', 500, 4000)
 * .then(function() {
 *     console.log('Port 44204 is now in use.');
 * }, function(err) {
 *     console.log('Error: ', error.message);
 * });
 */
function waitUntilUsedOnHost(port, host, retryTimeMs, timeOutMs) {

    // the first arument may be an object, if it is not, make an object
    var opts;
    if (is.obj(port)) {
        opts = port;
        opts.inUse = true;
    } else {
        opts = makeOptionsObj(port, host, true, retryTimeMs, timeOutMs);
    }

    return waitForStatus(opts);
}

/**
 * For compatibility to previous version of module which did not have support
 * for host addresses. This function works only for localhost.
 * @param {Number} port a valid TCP port number. If an Object, must contain all the parameters as properties.
 * @param {Number} [retryTimeMs] the retry interval in milliseconds - defaultis is 500ms
 * @param {Number} [timeOutMs] the amount of time to wait until port is free
 * @return {Object} A deferred promise from the q library.
 *
 * Example usage:
 *
 * var tcpPortUsed = require('tcp-port-used');
 * tcpPortUsed.waitUntilUsed(44204, 500, 4000)
 * .then(function() {
 *     console.log('Port 44204 is now in use.');
 * }, function(err) {
 *     console.log('Error: ', error.message);
 * });
 */
function waitUntilUsed(port, retryTimeMs, timeOutMs) {

    // the first arument may be an object, if it is not, make an object
    var opts;
    if (is.obj(port)) {
        opts = port;
        opts.host = '127.0.0.1';
        opts.inUse = true;
    } else {
        opts = makeOptionsObj(port, '127.0.0.1', true, retryTimeMs, timeOutMs);
    }

    return waitUntilUsedOnHost(opts);
}

