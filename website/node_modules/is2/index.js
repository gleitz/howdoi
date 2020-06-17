/**
 * @fileOverview
 * is2 derived from is by Enrico Marino, adapted for Node.js.
 * Slightly modified by Edmond Meinfelder
 *
 * is
 * the definitive JavaScript type testing library
 * Copyright(c) 2013,2014 Edmond Meinfelder <edmond@stdarg.com>
 * Copyright(c) 2011 Enrico Marino <enrico.marino@email.com>
 * MIT license
 */
'use strict';
const owns = {}.hasOwnProperty;
const toString = {}.toString;
const is = exports;
const deepIs = require('deep-is');
const ipRegEx =  require('ip-regex');
is.version = require('./package.json').version;

////////////////////////////////////////////////////////////////////////////////
// Environment

/**
 * Tests if is is running under a browser.
 * @return {Boolean} true if the environment has process, process.version and process.versions.
 */
is.browser = function() {
    return (!is.node() && typeof window !== 'undefined' && toString.call(window) === '[object global]');
};

/**
 * Test if 'value' is defined.
 * Alias: def
 * @param {Any} value The value to test.
 * @return {Boolean} true if 'value' is defined, false otherwise.
 */
is.defined = function(value) {
    return typeof value !== 'undefined';
};
is.def = is.defined;

/**
 * Tests if is is running under node.js
 * @return {Boolean} true if the environment has process, process.version and process.versions.
 */
is.nodejs = function() {
    return (process && process.hasOwnProperty('version') &&
            process.hasOwnProperty('versions'));
};
is.node = is.nodejs;

/**
 * Test if 'value' is undefined.
 * Aliases: undef, udef
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is undefined, false otherwise.
 */
is.undefined = function(value) {
    return value === undefined;
};
is.udef = is.undef = is.undefined;


////////////////////////////////////////////////////////////////////////////////
// Types

/**
 * Test if 'value' is an array.
 * Alias: ary, arry
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is an array, false otherwise.
 */
is.array = function(value) {
    return '[object Array]' === toString.call(value);
};
is.arr = is.ary = is.arry = is.array;

/**
 * Test if 'value' is an arraylike object (i.e. it has a length property with a valid value)
 * Aliases: arraylike, arryLike, aryLike
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is an arguments object, false otherwise.
 */
is.arrayLike = function(value) {
    if (is.nullOrUndef(value))
        return false;
    return value !== undefined &&
        owns.call(value, 'length') &&
        isFinite(value.length);
};
is.arrLike = is.arryLike = is.aryLike = is.arraylike = is.arrayLike;

/**
 * Test if 'value' is an arguments object.
 * Alias: args
 * @param {Any} value value to test
 * @return {Boolean} true if 'value' is an arguments object, false otherwise
 */
is.arguments = function(value) {
    return '[object Arguments]' === toString.call(value);
};
is.args = is.arguments;

/**
 * Test if 'value' is a boolean.
 * Alias: bool
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a boolean, false otherwise.
 */
is.boolean = function(value) {
    return '[object Boolean]' === toString.call(value);
};
is.bool = is.boolean;

/**
 * Test if 'value' is an instance of Buffer.
 * Aliases: instOf, instanceof
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is an instance of 'constructor'.
 */
is.buffer = function(value) {
    return is.nodejs() && Buffer && Buffer.hasOwnProperty('isBuffer') && Buffer.isBuffer(value);
};
is.buff = is.buf = is.buffer;

/**
 * Test if 'value' is a date.
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a date, false otherwise.
 */
is.date = function(value) {
    return '[object Date]' === toString.call(value);
};

/**
 * Test if 'value' is an error object.
 * Alias: err
 * @param value value to test.
 * @return {Boolean} true if 'value' is an error object, false otherwise.
 */
is.error = function(value) {
    return '[object Error]' === toString.call(value);
};
is.err = is.error;

/**
 * Test if 'value' is false.
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is false, false otherwise
 */
is.false = function(value) {
    return value === false;
};

/**
 * Test if 'value' is a function or async function.
 * Alias: func
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a function, false otherwise.
 */
is.function = function(value) {
    return is.syncFunction(value) || is.asyncFunction(value)
};
is.fun = is.func = is.function;

/**
 * Test if 'value' is an async function using `async () => {}` or `async function () {}`.
 * Alias: func
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a function, false otherwise.
 */
is.asyncFunction = function(value) {
  return '[object AsyncFunction]' === toString.call(value);
}
is.asyncFun = is.asyncFunc = is.asyncFunction;

/**
 * Test if 'value' is a synchronous function.
 * Alias: syncFunc
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a function, false otherwise.
 */
is.syncFunction = function (value) {
  return '[object Function]' === toString.call(value);
}
is.syncFun = is.syncFunc = is.syncFunction
/**
 * Test if 'value' is null.
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is null, false otherwise.
 */
is.null = function(value) {
    return value === null;
};

/**
 * Test is 'value' is either null or undefined.
 * Alias: nullOrUndef
 * @param {Any} value value to test.
 * @return {Boolean} True if value is null or undefined, false otherwise.
 */
is.nullOrUndefined = function(value) {
    return value === null || typeof value === 'undefined';
};
is.nullOrUndef = is.nullOrUndefined;

/**
 * Test if 'value' is a number.
 * Alias: num
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a number, false otherwise.
 */
is.number = function(value) {
    return '[object Number]' === toString.call(value);
};
is.num = is.number;

/**
 * Test if 'value' is an object. Note: Arrays, RegExps, Date, Error, etc all return false.
 * Alias: obj
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is an object, false otherwise.
 */
is.object = function(value) {
    return '[object Object]' === toString.call(value);
};
is.obj = is.object;

/**
 * Test if 'value' is a regular expression.
 * Alias: regexp
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a regexp, false otherwise.
 */
is.regExp = function(value) {
    return '[object RegExp]' === toString.call(value);
};
is.re = is.regexp = is.regExp;

/**
 * Test if 'value' is a string.
 * Alias: str
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a string, false otherwise.
 */
is.string = function(value) {
    return '[object String]' === toString.call(value);
};
is.str = is.string;

/**
 * Test if 'value' is true.
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is true, false otherwise.
 */
is.true = function(value) {
    return value === true;
};

/**
 * Test if 'value' is a uuid (v1-v5)
 * @param {Any} value to test.
 * @return {Boolean} true if 'value is a valid RFC4122 UUID. Case non-specific.
 */
var uuidRegExp = new RegExp('[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab]'+
                            '[0-9a-f]{3}-[0-9a-f]{12}', 'i');
is.uuid = function(value) {
    return uuidRegExp.test(value);
};

////////////////////////////////////////////////////////////////////////////////
// Object Relationships

/**
 * Test if 'value' is equal to 'other'. Works for objects and arrays and will do deep comparisions,
 * using recursion.
 * Alias: eq
 * @param {Any} value value.
 * @param {Any} other value to compare with.
 * @return {Boolean} true if 'value' is equal to 'other', false otherwise
 */
is.equal = function(value, other) {
    var type = toString.call(value);

    if (typeof value !== typeof other) {
        return false;
    }

    if (type !== toString.call(other)) {
        return false;
    }

    if ('[object Object]' === type || '[object Array]' === type) {
        return deepIs(value, other);
    } else if ('[object Function]' === type) {
        return value.prototype === other.prototype;
    } else if ('[object Date]' === type) {
        return value.getTime() === other.getTime();
    }

    return value === other;
};
is.objEquals = is.eq = is.equal;

/**
 * JS Type definitions which cannot host values.
 * @api private
 */
var NON_HOST_TYPES = {
    'boolean': 1,
    'number': 1,
    'string': 1,
    'undefined': 1
};

/**
 * Test if 'key' in host is an object. To be hosted means host[value] is an object.
 * @param {Any} value The value to test.
 * @param {Any} host Host that may contain value.
 * @return {Boolean} true if 'value' is hosted by 'host', false otherwise.
 */
is.hosted = function(value, host) {
    if (is.nullOrUndef(value))
        return false;
    var type = typeof host[value];
    return type === 'object' ? !!host[value] : !NON_HOST_TYPES[type];
};

/**
 * Test if 'value' is an instance of 'constructor'.
 * Aliases: instOf, instanceof
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is an instance of 'constructor'.
 */
is.instanceOf = function(value, constructor) {
    if (is.nullOrUndef(value) || is.nullOrUndef(constructor))
        return false;
    return (value instanceof constructor);
};
is.instOf = is.instanceof = is.instanceOf;

/**
 * Test if 'value' is an instance type objType.
 * Aliases: objInstOf, objectinstanceof, instOf, instanceOf
 * @param {object} objInst an object to testfor type.
 * @param {object} objType an object type to compare.
 * @return {Boolean} true if 'value' is an object, false otherwise.
 */
is.objectInstanceOf = function(objInst, objType) {
    try {
        return '[object Object]' === toString.call(objInst) && (objInst instanceof objType);
    } catch(err) {
        return false;
    }
};
is.instOf = is.instanceOf = is.objInstOf = is.objectInstanceOf;

/**
 * Test if 'value' is a type of 'type'.
 * Alias: a
 * @param value value to test.
 * @param {String} type The name of the type.
 * @return {Boolean} true if 'value' is an arguments object, false otherwise.
 */
is.type = function(value, type) {
    return typeof value === type;
};
is.a = is.type;

////////////////////////////////////////////////////////////////////////////////
// Object State

/**
 * Test if 'value' is empty. To be empty means to be an array, object or string with nothing contained.
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is empty, false otherwise.
 */
is.empty = function(value) {
    var type = toString.call(value);

    if ('[object Array]' === type || '[object Arguments]' === type) {
        return value.length === 0;
    }

    if ('[object Object]' === type) {
        for (var key in value) if (owns.call(value, key)) return false;
        return true;
    }

    if ('[object String]' === type) {
        return value === '';
    }

    return false;
};

/**
 * Test if 'value' is an arguments object that is empty.
 * Alias: args
 * @param {Any} value value to test
 * @return {Boolean} true if 'value' is an arguments object with no args, false otherwise
 */
is.emptyArguments = function(value) {
    return '[object Arguments]' === toString.call(value) && value.length === 0;
};
is.noArgs = is.emptyArgs = is.emptyArguments;

/**
 * Test if 'value' is an array containing no entries.
 * Aliases: emptyArry, emptyAry
 * @param {Any} value The value to test.
 * @return {Boolean} true if 'value' is an array with no elemnets.
 */
is.emptyArray = function(value) {
    return '[object Array]' === toString.call(value) && value.length === 0;
};
is.emptyArry = is.emptyAry = is.emptyArray;

/**
 * Test if 'value' is an empty array(like) object.
 * Aliases: arguents.empty, args.empty, ary.empty, arry.empty
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is an empty array(like), false otherwise.
 */
is.emptyArrayLike = function(value) {
    return value.length === 0;
};
is.emptyArrLike = is.emptyArrayLike;

/**
 * Test if 'value' is an empty string.
 * Alias: emptyStr
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is am empty string, false otherwise.
 */
is.emptyString = function(value) {
    return is.string(value) && value.length === 0;
};
is.emptyStr = is.emptyString;

/**
 * Test if 'value' is an array containing at least 1 entry.
 * Aliases: nonEmptyArry, nonEmptyAry
 * @param {Any} value The value to test.
 * @return {Boolean} true if 'value' is an array with at least 1 value, false otherwise.
 */
is.nonEmptyArray = function(value) {
    return '[object Array]' === toString.call(value) && value.length > 0;
};
is.nonEmptyArr = is.nonEmptyArry = is.nonEmptyAry = is.nonEmptyArray;

/**
 * Test if 'value' is an object with properties. Note: Arrays are objects.
 * Alias: nonEmptyObj
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is an object, false otherwise.
 */
is.nonEmptyObject = function(value) {
    return '[object Object]' === toString.call(value) && Object.keys(value).length > 0;
};
is.nonEmptyObj = is.nonEmptyObject;

/**
 * Test if 'value' is an object with no properties. Note: Arrays are objects.
 * Alias: nonEmptyObj
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is an object, false otherwise.
 */
is.emptyObject = function(value) {
    return '[object Object]' === toString.call(value) && Object.keys(value).length === 0;
};
is.emptyObj = is.emptyObject;

/**
 * Test if 'value' is a non-empty string.
 * Alias: nonEmptyStr
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a non-empty string, false otherwise.
 */
is.nonEmptyString = function(value) {
    return is.string(value) && value.length > 0;
};
is.nonEmptyStr = is.nonEmptyString;

////////////////////////////////////////////////////////////////////////////////
// Numeric Types within Number

/**
 * Test if 'value' is an even number.
 * @param {Number} value to test.
 * @return {Boolean} true if 'value' is an even number, false otherwise.
 */
is.even = function(value) {
    return '[object Number]' === toString.call(value) && value % 2 === 0;
};

/**
 * Test if 'value' is a decimal number.
 * Aliases: decimalNumber, decNum
 * @param {Any} value value to test.
 * @return {Boolean} true if 'value' is a decimal number, false otherwise.
 */
is.decimal = function(value) {
    return '[object Number]' === toString.call(value) && value % 1 !== 0;
};
is.dec = is.decNum = is.decimal;

/**
 * Test if 'value' is an integer.
 * Alias: integer
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is an integer, false otherwise.
 */
is.integer = function(value) {
    return '[object Number]' === toString.call(value) && value % 1 === 0;
};
is.int = is.integer;

/**
 * is.nan
 * Test if `value` is not a number.
 *
 * @param {Mixed} value value to test
 * @return {Boolean} true if `value` is not a number, false otherwise
 * @api public
 */
is.notANumber = function(value) {
    return !is.num(value) || value !== value;
};
is.nan = is.notANum = is.notANumber;

/**
 * Test if 'value' is an odd number.
 * @param {Number} value to test.
 * @return {Boolean} true if 'value' is an odd number, false otherwise.
 */
is.odd = function(value) {
    return !is.decimal(value) && '[object Number]' === toString.call(value) && value % 2 !== 0;
};
is.oddNumber = is.oddNum = is.odd;

////////////////////////////////////////////////////////////////////////////////
// Numeric Type & State

/**
 * Test if 'value' is a positive number.
 * Alias: positiveNum, posNum
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a number, false otherwise.
 */
is.positiveNumber = function(value) {
    return '[object Number]' === toString.call(value) && value > 0;
};
is.pos = is.positive = is.posNum = is.positiveNum = is.positiveNumber;

/**
 * Test if 'value' is a negative number.
 * Aliases: negNum, negativeNum
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a number, false otherwise.
 */
is.negativeNumber = function(value) {
    return '[object Number]' === toString.call(value) && value < 0;
};
is.neg = is.negNum = is.negativeNum = is.negativeNumber;

/**
 * Test if 'value' is a negative integer.
 * Aliases: negInt, negativeInteger
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a negative integer, false otherwise.
 */
is.negativeInteger = function(value) {
    return '[object Number]' === toString.call(value) && value % 1 === 0 && value < 0;
};
is.negativeInt = is.negInt = is.negativeInteger;

/**
 * Test if 'value' is a positive integer.
 * Alias: posInt
 * @param {Any} value to test.
 * @return {Boolean} true if 'value' is a positive integer, false otherwise.
 */
is.positiveInteger = function(value) {
    return '[object Number]' === toString.call(value) && value % 1 === 0 && value > 0;
};
is.posInt = is.positiveInt = is.positiveInteger;

////////////////////////////////////////////////////////////////////////////////
// Numeric Relationships

/**
 * Test if 'value' is divisible by 'n'.
 * Alias: divisBy
 * @param {Number} value value to test.
 * @param {Number} n dividend.
 * @return {Boolean} true if 'value' is divisible by 'n', false otherwise.
 */
is.divisibleBy = function(value, n) {
    if (value === 0)
        return false;
    return '[object Number]' === toString.call(value) &&
        n !== 0 &&
        value % n === 0;
};
is.divBy = is.divisBy = is.divisibleBy;

/**
 * Test if 'value' is greater than or equal to 'other'.
 * Aliases: greaterOrEq, greaterOrEqual
 * @param {Number} value value to test.
 * @param {Number} other value to compare with.
 * @return {Boolean} true, if value is greater than or equal to other, false otherwise.
 */
is.greaterOrEqualTo = function(value, other) {
    return value >= other;
};
is.greaterOrEqual = is.ge = is.greaterOrEqualTo;

/**
 * Test if 'value' is greater than 'other'.
 * Aliases: greaterThan
 * @param {Number} value value to test.
 * @param {Number} other value to compare with.
 * @return {Boolean} true, if value is greater than other, false otherwise.
 */
is.greaterThan = function(value, other) {
    return value > other;
};
is.gt = is.greaterThan;

/**
 * Test if 'value' is less than or equal to 'other'.
 * Alias: lessThanOrEq, lessThanOrEqual
 * @param {Number} value value to test
 * @param {Number} other value to compare with
 * @return {Boolean} true, if 'value' is less than or equal to 'other', false otherwise.
 */
is.lessThanOrEqualTo = function(value, other) {
    return value <= other;
};
is.lessThanOrEq = is.lessThanOrEqual = is.le = is.lessThanOrEqualTo;

/**
 * Test if 'value' is less than 'other'.
 * Alias: lessThan
 * @param {Number} value value to test
 * @param {Number} other value to compare with
 * @return {Boolean} true, if 'value' is less than 'other', false otherwise.
 */
is.lessThan = function(value, other) {
    return value < other;
};
is.lt = is.lessThan;

/**
 * Test if 'value' is greater than 'others' values.
 * Alias: max
 * @param {Number} value value to test.
 * @param {Array} others values to compare with.
 * @return {Boolean} true if 'value' is greater than 'others' values.
 */
is.maximum = function(value, others) {
    if (!is.arrayLike(others) || !is.number(value))
        return false;

    var len = others.length;
    while (--len > -1) {
        if (value < others[len]) {
            return false;
        }
    }

    return true;
};
is.max = is.maximum;

/**
 * Test if 'value' is less than 'others' values.
 * Alias: min
 * @param {Number} value value to test.
 * @param {Array} others values to compare with.
 * @return {Boolean} true if 'value' is less than 'others' values.
 */
is.minimum = function(value, others) {
    if (!is.arrayLike(others) || !is.number(value))
        return false;

    var len = others.length;
    while (--len > -1) {
        if (value > others[len]) {
            return false;
        }
    }

    return true;
};
is.min = is.minimum;

/**
 * Test if 'value' is within 'start' and 'finish'.
 * Alias: withIn
 * @param {Number} value value to test.
 * @param {Number} start lower bound.
 * @param {Number} finish upper bound.
 * @return {Boolean} true if 'value' is is within 'start' and 'finish', false otherwise.
 */
is.within = function(value, start, finish) {
    return value >= start && value <= finish;
};
is.withIn = is.within;

/**
 * Test if 'value' is within 'precision' decimal places from 'comparitor'.
 * Alias: closish, near.
 * @param {Number} value value to test
 * @param {Number} comparitor value to test 'value' against
 * @param {Number} precision number of decimals to compare floating points, defaults to 2
 * @return {Boolean} true if 'value' is within 'precision' decimal places from 'comparitor', false otherwise.
 */
is.prettyClose = function(value, comparitor, precision) {
  if (!is.number(value) || !is.number(comparitor)) return false;
  if (is.defined(precision) && !is.posInt(precision)) return false;
  if (is.undefined(precision)) precision = 2;

  return value.toFixed(precision) === comparitor.toFixed(precision);
};
is.closish = is.near = is.prettyClose;
////////////////////////////////////////////////////////////////////////////////
// Networking

/**
 * Test if a value is a valid DNS address. eg www.stdarg.com is true while
 * 127.0.0.1 is false.
 * @param {Any} value to test if a DNS address.
 * @return {Boolean} true if a DNS address, false otherwise.
 * DNS Address is made up of labels separated by '.'
 * Each label must be between 1 and 63 characters long
 * The entire hostname (including the delimiting dots) has a maximum of 255 characters.
 * Hostname may not contain other characters, such as the underscore character (_)
 * other DNS names may contain the underscore.
 */
is.dnsAddress = function(value) {
    if (!is.nonEmptyStr(value))  return false;
    if (value.length > 255)  return false;
    if (numbersLabel.test(value))  return false;
    if (!dnsLabel.test(value))  return false;
    return true;
    //var names = value.split('.');
    //if (!is.array(names) || !names.length)  return false;
    //if (names[0].indexOf('_') > -1)  return false;
    //for (var i=0; i<names.length; i++) {
        //if (!dnsLabel.test(names[i]))  return false;
    //}
    //return true;
};
is.dnsAddr = is.dns = is.dnsAddress;
var dnsLabel = /^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$/;
var numbersLabel = /^([0-9]|[0-9][0-9\-]{0,61}[0-9])(\.([0-9]|[0-9][0-9\-]{0,61}[0-9]))*$/;

/**
 * Test if value is a valid email address.
 * @param {Any} value to test if an email address.
 * @return {Boolean} true if an email address, false otherwise.
 */
is.emailAddress = function(value) {
    if (!is.nonEmptyStr(value))
        return false;
    return emailRegexp.test(value);
};
is.email = is.emailAddr = is.emailAddress;
var emailRegexp = /^([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22))*\x40([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d))*$/;

/**
 * Test if a value is either an IPv4 numeric IP address.
 * The rules are:
 * must be a string
 * length must be 15 characters or less
 * There must be four octets separated by a '.'
 * No octet can be less than 0 or greater than 255.
 * @param {Any} value to test if an ip address.
 * @return {Boolean} true if an ip address, false otherwise.
 */
is.ipv4Address = function(value) {
    if (!is.nonEmptyStr(value))  return false;
    if (value.length > 15)  return false;
    var octets = value.split('.');
    if (!is.array(octets) || octets.length !== 4)  return false;
    for (var i=0; i<octets.length; i++) {
        var val = parseInt(octets[i], 10);
        if (isNaN(val))  return false;
        if (val < 0 || val > 255)  return false;
    }
    return true;
};
is.ipv4 = is.ipv4Addr = is.ipv4Address;

/**
 * Test if a value is either an IPv6 numeric IP address.
 * @param {Any} value to test if an ip address.
 * @return {Boolean} true if an ip address, false otherwise.
 */
is.ipv6Address = function(value) {
    if (!is.nonEmptyStr(value))  return false;
    return ipRegEx.v6({extract: true}).test(value);
};
is.ipv6 = is.ipv6Addr = is.ipv6Address;

/**
 * Test if a value is either an IPv4 or IPv6 numeric IP address.
 * @param {Any} value to test if an ip address.
 * @return {Boolean} true if an ip address, false otherwise.
 */
is.ipAddress = function(value) {
    if (!is.nonEmptyStr(value)) return false;
    return is.ipv4Address(value) || is.ipv6Address(value)
};
is.ip = is.ipAddr = is.ipAddress;

/**
 * Test is a value is a valid ipv4, ipv6 or DNS name.
 * Aliases: host, hostAddr, hostAddress.
 * @param {Any} value to test if a host address.
 * @return {Boolean} true if a host address, false otherwise.
 */
is.hostAddress = function(value) {
    if (!is.nonEmptyStr(value)) return false;
    return is.dns(value) || is.ipv4(value) || is.ipv6(value);
};
is.host = is.hostIp = is.hostAddr = is.hostAddress;

/**
 * Test if a number is a valid TCP port
 * @param {Any} value to test if its a valid TCP port
 */
is.port = function(value) {
    if (!is.num(value) || is.negativeInt(value) || value > 65535)
        return false;
    return true;
};

/**
 * Test if a number is a valid TCP port in the range 0-1023.
 * Alias: is.sysPort.
 * @param {Any} value to test if its a valid TCP port
 */
is.systemPort = function(value) {
    if (is.port(value) && value < 1024)
        return true;
    return false;
};
is.sysPort = is.systemPort;

/**
 * Test if a number is a valid TCP port in the range 1024-65535.
 * @param {Any} value to test if its a valid TCP port
 */
is.userPort = function(value) {
    if (is.port(value) && value > 1023)
        return true;
    return false;
};

/*
function sumDigits(num) {
    var str = num.toString();
    var sum = 0;
    for (var i = 0; i < str.length; i++)
        sum += (str[i]-0);
    return sum;
}
*/

/**
 * Test if a string is a credit card.
 * From http://en.wikipedia.org/wiki/Luhn_algorithm
 * @param {String} value to test if a credit card.
 * @return true if the string is the correct format, false otherwise
 */
is.creditCardNumber = function(str) {
    if (!is.str(str))
        return false;

    var ary = str.split('');
    var i, cnt;
    // From the rightmost digit, which is the check digit, moving left, double
    // the value of every second digit;
    for (i=ary.length-1, cnt=1; i>-1; i--, cnt++) {
        if (cnt%2 === 0)
            ary[i] *= 2;
    }

    str = ary.join('');
    var sum = 0;
    // if the product of the previous doubling operation is greater than 9
    // (e.g., 7 * 2 = 14), then sum the digits of the products (e.g., 10: 1 + 0
    // = 1, 14: 1 + 4 = 5).  We do the this by joining the array of numbers and
    // add adding the int value of all the characters in the string.
    for (i=0; i<str.length; i++)
        sum += Math.floor(str[i]);

    // If the total (sum) modulo 10 is equal to 0 (if the total ends in zero)
    // then the number is valid according to the Luhn formula; else it is not
    // valid.
    return sum % 10 === 0;
};
is.creditCard = is.creditCardNum = is.creditCardNumber;


////////////////////////////////////////////////////////////////////////////////
// The following credit card info is from:
// http://en.wikipedia.org/wiki/Bank_card_number#Issuer_identification_number_.28IIN.29

/**
 * Test if card number is an American Express card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.americanExpressCardNumber = function(str) {
    if (!is.str(str) || str.length !== 15)
        return false;

    var prefix = Math.floor(str.slice(0,2));
    if (prefix !== 34 && prefix !== 37)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.amexCard = is.amexCardNum = is.americanExpressCardNumber;

/**
 * Test if card number is a China UnionPay card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.chinaUnionPayCardNumber = function(str) {
    if (!is.str(str) || (str.length < 16 && str.length > 19))
        return false;

    var prefix = Math.floor(str.slice(0,2));
    if (prefix !== 62 && prefix !== 88)
        return false;

    // no validation for this card
    return true;
};
is.chinaUnion = is.chinaUnionPayCard = is.chinaUnionPayCardNumber;

/**
 * Test if card number is a Diner's Club Carte Blance card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.dinersClubCarteBlancheCardNumber = function(str) {
    if (!is.str(str) || str.length !== 14)
        return false;

    var prefix = Math.floor(str.slice(0,3));
    if (prefix < 300 || prefix > 305)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.dinersClubCB = is.dinersClubCarteBlancheCard =
    is.dinersClubCarteBlancheCardNumber;

/**
 * Test if card number is a Diner's Club International card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.dinersClubInternationalCardNumber = function(str) {
    if (!is.str(str) || str.length !== 14)
        return false;
    var prefix = Math.floor(str.slice(0,3));
    var prefix2 = Math.floor(str.slice(0,2));

    // 300-305, 309, 36, 38-39
    if ((prefix < 300 || prefix > 305) && prefix !== 309 && prefix2 !== 36 &&
        (prefix2 < 38 || prefix2 > 39)) {
        return false;
    }

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.dinersClubInt = is.dinersClubInternationalCard =
    is.dinersClubInternationalCardNumber;

/**
 * Test if card number is a Diner's Club USA & CA card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.dinersClubUSACanadaCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;
    var prefix = Math.floor(str.slice(0,2));

    if (prefix !== 54 && prefix !== 55)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.dinersClub = is.dinersClubUSACanCard = is.dinersClubUSACanadaCardNumber;

/**
 * Test if card number is a Diner's Club USA/CA card.
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.discoverCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    var prefix = Math.floor(str.slice(0,6));
    var prefix2 = Math.floor(str.slice(0,3));

    if (str.slice(0,4) !== '6011' && (prefix < 622126 || prefix > 622925) &&
        (prefix2 < 644 || prefix2 > 649) && str.slice(0,2) !== '65') {
        return false;
    }

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.discover = is.discoverCard = is.discoverCardNumber;

/**
 * Test if card number is an InstaPayment card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.instaPaymentCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    var prefix = Math.floor(str.slice(0,3));
    if (prefix < 637 || prefix > 639)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.instaPayment = is.instaPaymentCardNumber;

/**
 * Test if card number is a JCB card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.jcbCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    var prefix = Math.floor(str.slice(0,4));
    if (prefix < 3528 || prefix > 3589)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.jcb = is.jcbCard = is.jcbCardNumber;

/**
 * Test if card number is a Laser card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.laserCardNumber = function(str) {
    if (!is.str(str) || (str.length < 16 && str.length > 19))
        return false;

    var prefix = Math.floor(str.slice(0,4));
    var valid = [ 6304, 6706, 6771, 6709 ];
    if (valid.indexOf(prefix) === -1)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.laser = is.laserCard = is.laserCardNumber;

/**
 * Test if card number is a Maestro card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.maestroCardNumber = function(str) {
    if (!is.str(str) || str.length < 12 || str.length > 19)
        return false;

    var prefix = str.slice(0,4);
    var valid = [ '5018', '5020', '5038', '5612', '5893', '6304', '6759',
        '6761', '6762', '6763', '0604', '6390' ];

    if (valid.indexOf(prefix) === -1)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.maestro = is.maestroCard = is.maestroCardNumber;

/**
 * Test if card number is a Dankort card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.dankortCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    if (str.slice(0,4) !== '5019')
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.dankort = is.dankortCard = is.dankortCardNumber;

/**
 * Test if card number is a MasterCard card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.masterCardCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    var prefix = Math.floor(str.slice(0,2));
    if (prefix < 50 || prefix > 55)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};
is.masterCard = is.masterCardCard = is.masterCardCardNumber;

/**
 * Test if card number is a Visa card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.visaCardNumber = function(str) {
    if (!is.str(str) || (str.length !== 13 && str.length !== 16))
        return false;

    if ('4' !== str.slice(0,1))
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return true;
};

is.visa = is.visaCard = is.visaCardNumber;

/**
 * Test if card number is a Visa card number
 * @param {String} the credit card number string to test.
 * @return true if the string is the correct format, false otherwise
 */
is.visaElectronCardNumber = function(str) {
    if (!is.str(str) || str.length !== 16)
        return false;

    var prefix = Math.floor(str.slice(0,4));
    var valid = [ 4026, 4405, 4508, 4844, 4913, 4917 ];
    if ('417500' !== str.slice(0,6) && valid.indexOf(prefix) === -1)
        return false;

    if (!is.creditCardNumber(str))
        return false;

    return false;
};

is.visaElectron = is.visaElectronCard = is.visaElectronCardNumber;

/**
 * Test if the input is a valid MongoDB id.
 * @param {String|Object} Either a mongodb object id or a string representation.
 * @return true if the string is the correct format, false otherwise
 * Thanks to Jason Denizac (https://github.com/jden) for pointing this out.
 * https://github.com/jden/objectid/blob/master/index.js#L7-L10
 */
var objIdPattern = /^[0-9a-fA-F]{24}$/;
is.mongoId = is.objectId = is.objId = function(id) {
  return (Boolean(id) && !Array.isArray(id) && objIdPattern.test(String(id)));
};

/**
 * Test is the first argument is structly equal to any of the subsequent args.
 * @param Value to test against subsequent arguments.
 * @return true if the first value matches any of subsequent values.
 */
is.matching = is.match = is.inArgs = function(val) {
    if (arguments.length < 2)
        return false;
    var result = false;
    for (var i=1; i<arguments.length; i++) {
        var eq = is.equal(val, arguments[i]);
        result = result || eq;
    }
    return result;
};



// US Address components
/**********************************
***Definitely a work in progress***
**********************************/
/**
 * Test if a string contains a US street address
 * @param {String} the string to search
 * @return true if an address is present, false otherwise
 */
is.streetAddress = function(str) {
  if (!is.str(str))
      return false;

  var regex = /\b\d+[\s](?:[A-Za-z0-9.-]+[\s]+)+\b(ALLEY|ALY|AVENUE|AVE|BEND|BND|BLUFFS?|BLFS?|BOULEVARD|BLVD|BRANCH|BR|CENTERS?|CTRS?|CIRCLES?|CIRS?|CLIFFS?|CLFS?|COURTS?|CTS?|COVES?|CVS?|CREEK|CRK|CRESCENT|CRES|CREST|CRST|CROSSING|XING|DRIVES?|DRS?|EXPRESSWAY|EXPY|FREEWAY|FWY|HEIGHTS|HTS|HIGHWAY|HWY|HILLS?|HLS?|LANE|LN|LOOP|MANORS?|MNRS?|MOTORWAY|MTWY|MOUNT|MT|PARKS?|PARKWAYS?|PKWY|PASS|PLACE|PL|PLAZA|PLZ|POINTS?|PTS?|RIDGES?|RDGS?|ROADS?|RDS?|ROUTE|RTE?|SHOALS?|SHLS?|SHORES?|SHRS?|SPRINGS?|SPGS?|SPURS?|STREETS?|STS?|SUMMIT|SMT|TERRACE|TER|THROUGHWAY|TRWY|TRAFFICWAY|TRFY|TRAIL|TRL|TURNPIKE|TPKE|VALLEYS?|VLYS?|WAYS?)+(?:[\.\-\s\,]?)*((APARTMENT|APT|APPT|#|NUMBER|NUM|FLOOR|FL|\s)?(\d)*)\b/ig;

  return regex.test(str);
};
is.street = is.address = is.streetAddress;

/**
 * Test if a string resembles a US Zip code,
 * no regular expression will be perfect for this,
 * as there are many numbers that aren't valid zip codes
 * @param {String || Number} the string or number literal to test
 * @return true if zipcode like, false otherwise
 */
is.zipCode = function(str) {
  if (is.undefined(str) || !(is.string(str) || is.number(str)))
    return false;

  var zip = /^\d{5}(?:-\d{4})?$/;
  return zip.test(str);
};
is.zip = is.zipCode;

/**
 * Test if a string contains a US phone number
 * @param {String} the string to search
 * @return true if str contains a phone number, false otherwise.
 */
 is.phoneNumber = function(str){
   if (!is.string(str))
    return false;
   var nums = /(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:(\(?)(?:(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]‌​)\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\)?)\s*(?:[.-]\s*)?)?([2-9]1[02-‌​9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})/g;
   return nums.test(str);
 };
 is.phone = is.phoneNumber;

/**
 * Test is a string is a valid URL
 * @param {string} val - the possible url to check
 * @return true if str contains a phone number, false otherwise.
 */
var isUrl = require('is-url');
is.url = function(val) {
    return isUrl(val);
};
is.uri = is.url;

is.enumerator = function(val, ary){
  var value = false;

  if (!is.defined(val) || !is.defined(ary) || !is.arrayLike(ary))
    return value;

  for (var i = 0, len = ary.length; i < len; i++) {
    if (is.equal(val, ary[i])) {
      value = true;
      break;
    }
  }
  return value;
};
is.enum = is.inArray = is.enumerator;
