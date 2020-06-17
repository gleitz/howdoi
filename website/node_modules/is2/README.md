is2
===
is2 is a type-checking module for JavaScript to test values. Is does not throw
exceptions and every function only returns true or false. Use is2 to validate
types in your node.js code. Every function in is2 returns either true of false.

## Installation
To install is2, type:

  $ npm install is2

## Usage

    const is = require('is2');

    console.log(`1===1 is: ${is.equal(true, 1===1)}`);
    console.log(`10 is a positive number: ${is.positiveNumber(10)}`);
    console.log(`11 is an odd number: ${is.oddNumber(11)}`);

## API

Each function returns true or false. The names after the '-' are aliases, which
provide brevity.

Environment:

* is.browser()
* is.defined(val) - is.def
* is.nodejs() - is.node()
* is.undefined(val) - is.udef, is.undef

Types:

* is.array(val) - is.ary, is.arry
* is.arrayLike(val) - is.arryLike, is.aryLike, is.arrLike
* is.arguments(val) - is.args
* is.boolean(val) - is.bool
* is.buffer(val) - is.buf, is.buff
* is.date(val)
* is.error(val) - is.err
* is.false(val)
* is.function(val) - is.funct, is.fun
* is.mongoId - is.objectId, is.objId
* is.null(val)
* is.nullOrUndefined(val) - is.nullOrUndef
* is.number(val) - is.num
* is.object(val) - is.obj
* is.regExp(val) - is.regexp, is.re
* is.string(val) - is.str
* is.true(val)
* is.uuid(val)

Relationships:

* is.equal(val, other) - is.eq, is.objEquals
* is.hosted(val, host)
* is.instanceOf(val, constructor) - is.instOf, is.instanceof
* is.matching(val1, val2 [, val3, ...]) - is.match : true if the first arument
  is strictly equal to any of the subsequent args.
* is.objectInstanceof(obj, objType) - is.instOf, is.instanceOf, is.objInstOf, is.objectInstanceOf
* is.type(val, type) - is.a
* is.enumerator(val, array) - is.enum, is.inArray

Object State:

* is.empty(val)
* is.emptyArguments(val) - is.emptyArgs, is.noArgs
* is.emptyArray(val) - is.emptyArry, is.emptyAry, is.emptyArray
* is.emptyArrayLike(val) - is.emptyArrLike
* is.emptyString(val) - is.emptyStr
* is.nonEmptyArray(val) - is.nonEmptyArry, is.nonEmptyAry
* is.nonEmptyObject(val) - is.nonEmptyObj
* is.emptyObject(val) - is.emptyObj
* is.nonEmptyString(val) - is.nonEmptyStr

Numeric Types within Number:

* is.even(val) - is.evenNum, is.evenNumber
* is.decimal(val) - is.decNum, is.dec
* is.integer(val) - is.int
* is.notANumber(val) - is.nan, is.notANum
* is.odd(val) - is.oddNum, is.oddNumber

Numeric Type and State:

* is.positiveNumber(val) - is.pos, is.positive, is.posNum, is.positiveNum
* is.negativeNumber(val) - is.neg,  is.negNum,  is.negativeNum,  is.negativeNumber
* is.negativeInteger(val) - is.negativeInt, is.negInt
* is.positiveInteger(val) - is.posInt, is.positiveInt

Numeric Relationship:

* is.divisibleBy(val, other) - is.divisBy, is.divBy
* is.greaterOrEqualTo(val, other) - is.ge, is.greaterOrEqual
* is.greaterThan(val, other) - is.gt
* is.lessThanOrEqualTo(val, other) - is.lessThanOrEq, is.lessThanOrEqual, is.le
* is.lessThan(val, other) - is.lt
* is.maximum(val, array) - is.max
* is.minimum(val, array) - is.min
* is.withIn(val, start, finish) - is.within
* is.prettyClose(val, comp, precision) - is.closish, is.near

Networking:

* is.dnsAddress(val) - is.dnsAddr, is.dns
* is.emailAddress(val) - is.email, is.emailAddr
* is.ipv4Address(val) - is.ipv4, is.ipv4Addr
* is.ipv6Address(val) - is.ipv6, is.ipv6Addr
* is.ipAddress(val) - is.ip, is.ipAddr
* is.hostAddress(val) - is.host = is.hostIp = is.hostAddr
* is.port(val)
* is.systemPort(val) - is.sysPort
* is.url(val) - is.uri
* is.userPort(val)

Credit Cards:

* is.creditCardNumber(str) - is.creditCard, is.creditCardNum
* is.americanExpressCardNumber(str) - is.amexCardNum, is.amexCard
* is.chinaUnionPayCardNumber(str) - is.chinaUnionPayCard, is.chinaUnion
* is.dankortCardNumber(str) - is.dankortCard, is.dankort
* is.dinersClubCarteBlancheCardNumber(str) - is.dinersClubCarteBlancheCard,
  is.dinersClubCB
* is.dinersClubInternationalCardNumber(str) - is.dinersClubInternationalCard,
  is.dinersClubInt
* is.dinersClubUSACanadaCardNumber(str) - is.dinersClubUSACanCard, is.dinersClub
* is.discoverCardNumber(str) - is.discoverCard, is.discover
* is.instaPaymentCardNumber(str) - is.instaPayment
* is.jcbCardNumber(str) - is.jcbCard, is.jcb
* is.laserCardNumber(str) - is.laserCard, is.laser
* is.maestroCardNumber(str) - is.maestroCard, is.maestro
* is.masterCardCardNumber - is.masterCardCard, is.masterCard
* is.visaCardNumber(str) - is.visaCard, is.visa
* is.visaElectronCardNumber(str) - is.visaElectronCard, is.visaElectron

Personal information:

* is.streetAddress(str) - is.street, is.address
* is.zipCode(str) - is.zip
* is.phoneNumber(str) - is.phone


## License
The MIT License (MIT)

Copyright (c) 2013,2014 Edmond Meinfelder
Copyright (c) 2011 Enrico Marino

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
