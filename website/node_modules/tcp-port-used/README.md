tcp-port-used
=============

A simple Node.js module to check if a TCP port is currently in use. It returns a
deferred promise from the q library.

## Installation

    npm install tcp-port-used

## Examples
To check a port's state:

    var tcpPortUsed = require('tcp-port-used');

    tcpPortUsed.check(44201, '127.0.0.1')
    .then(function(inUse) {
        console.log('Port 44201 usage: '+inUse);
    }, function(err) {
        console.error('Error on check:', err.message);
    });

To wait until a port on localhost is available:

    tcpPortUsed.waitUntilFree(44203, 500, 4000)
    .then(function() {
        console.log('Port 44203 is now free.');
    }, function(err) {
        console.log('Error:', err.message);
    });

To wait until a port on a host is available:

    tcpPortUsed.waitUntilFreeOnHost(44203, 'some.host.com', 500, 4000)
    .then(function() {
        console.log('Port 44203 on some.host.com is now free.');
    }, function(err) {
        console.log('Error:', err.message);
    });

To wait until a port on localhost is accepting connections:

    tcpPortUsed.waitUntilUsed(44204, 500, 4000)
    .then(function() {
        console.log('Port 44204 is now in use.');
    }, function(err) {
        console.log('Error:', err.message);
    });

To wait until a port on a host is accepting connections:

    tcpPortUsed.waitUntilUsedOnHost(44204, 'some.host.com', 500, 4000)
    .then(function() {
        console.log('Port 44204 on some.host.com is now in use.');
    }, function(err) {
        console.log('Error:', err.message);
    });

To wait until a port on a host is in specific state:

    var inUse = true;   // wait until the port is in use
    tcpPortUsed.waitForStatus(44204, 'some.host.com', inUse, 500, 4000)
    .then(function() {
        console.log('Port 44204 on some.host.com is now in use.');
    }, function(err) {
        console.log('Error:', err.message);
    });


## API

### check(port [, host])
Checks if a TCP port is in use by attempting to connect to the port on host.
If no host is specified, the module uses '127.0.0.1' (localhost). When the
promise is resolved, there is a parameter `inUse`, when true means the port is
in use and false means the port is free.

**Parameters:**

* **Number|Object** *port* The port you are curious to see if available. If an
  object, must contain all the parameters as properties.
* **String** *host* The host name or IP address of the host. Default, if not defined: '127.0.0.1'

**Returns:**

**Object** A deferred promise from the q module.

### waitUntilFree(port [, retryTimeMs] [, timeOutMs])
Returns a deferred promise and fulfills it only when the localhost socket is
free.  Will retry on an interval specified in retryTimeMs until the timeout. If
not defined the retryTime is 200 ms and the timeout is 2000 ms.

**Parameters:**

* **Number|Object** *port* a valid TCP port number. If an object must contain
  all the parameters as properties.
* **Number** *[retryTimeMs]* the retry interval in milliseconds - defaultis is 100ms.
* **Number** *[timeOutMs]* the amount of time to wait until port is free. Default 300ms.

**Returns:**

**Object** A deferred promise from the q module.


### waitUntilFreeOnHost(port [, host] [, retryTimeMs] [, timeOutMs])
Returns a deferred promise and fulfills it only when the localhost socket is
free.  Will retry on an interval specified in retryTimeMs until the timeout. If
not defined the retryTime is 200 ms and the timeout is 2000 ms. If the host is
not defined, the modules uses the default '127.0.0.1'.

**Parameters:**

* **Number|Object** *port* a valid TCP port number. If an object, must contain
  all the parameters as properties.
* **String** *host* The host name or IP address of the host. Default, if not defined: '127.0.0.1'
* **Number** *[retryTimeMs]* the retry interval in milliseconds - defaultis is 100ms.
* **Number** *[timeOutMs]* the amount of time to wait until port is free. Default 300ms.

**Returns:**

**Object** A deferred promise from the q module.

### waitUntilUsed(port [, retryTimeMs] [, timeOutMs])
Returns a deferred promise and fulfills it only when the socket is accepting
connections. Will retry on an interval specified in retryTimeMs until the
timeout. If the host is not defined the retryTime is 200 ms and the timeout is
2000 ms.

**Parameters:**

* **Number|Object** *port* a valid TCP port number. If an object, must contain
  all the parameters as properties.
* **Number** *[retryTimeMs]* the retry interval in milliseconds - defaultis is 100ms.
* **Number** *[timeOutMs]* the amount of time to wait until port is free. Default 300ms.

**Returns:**

**Object** A deferred promise from the q module.

### waitUntilUsedOnHost(port [, host] [, retryTimeMs] [, timeOutMs])
Returns a deferred promise and fulfills it only when the socket is accepting
connections. Will retry on an interval specified in retryTimeMs until the
timeout. If not defined the retryTime is 200 ms and the timeout is 2000 ms.
If the host is not defined the module uses the default '127.0.0.1'.

**Parameters:**

* **Number|Object** *port* a valid TCP port number. If an object, must contain
  all the parameters as properties.
* **String** *host* The host name or IP address of the host. Default, if not defined: '127.0.0.1'
* **Number** *[retryTimeMs]* the retry interval in milliseconds - defaultis is 100ms.
* **Number** *[timeOutMs]* the amount of time to wait until port is free. Default 300ms.

**Returns:**

**Object** A deferred promise from the q module.

### waitForStatus(port, host, status [, retryTimeMs] [, timeOutMs])
Waits until the port on host matches the boolean status in terms of use. If the
status is true, the promise defers until the port is in use. If the status is
false the promise defers until the port is free. If the host is undefined or
null, the module uses the default '127.0.0.1'. Also, if not defined the
retryTime is 200 ms and the timeout is 2000 ms.

**Parameters:**

* **Number** *port* a valid TCP port number. If an object, must contain all the
  parameters as properties.
* **String** *host* The host name or IP address of the host. Default, if not defined: '127.0.0.1'
* **Boolean** *status* A boolean describing the condition to wait for in terms of "in use." True indicates wait until the port is in use. False indicates wait until the port is free.
* **Number** *[retryTimeMs]* the retry interval in milliseconds - defaultis is 100ms.
* **Number** *[timeOutMs]* the amount of time to wait until port is free. Default 300ms.

**Returns:**

**Object** A deferred promise from the q module.

## License

The MIT License (MIT)

Copyright (c) 2013 jut-io

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

