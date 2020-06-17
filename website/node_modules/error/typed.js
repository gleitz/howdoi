'use strict';

var template = require('string-template');
var assert = require('assert');

var hasOwnProperty = Object.prototype.hasOwnProperty;
var isWordBoundary = /[_.-](\w|$)/g;

var FUNCTION_FIELD_WHITELIST = Object.getOwnPropertyNames(TypedError)

module.exports = TypedError;

function TypedError(args) {
    assert(args, 'TypedError: must specify options');
    assert(args.type, 'TypedError: must specify options.type');
    assert(args.message, 'TypedError: must specify options.message');

    assert(!has(args, 'fullType'),
        'TypedError: fullType field is reserved');

    var message = args.message;
    var funcName = args.name
    if (!funcName) {
        var errorName = camelCase(args.type) + 'Error';
        funcName = errorName[0].toUpperCase() + errorName.substr(1);
    }

    var copyArgs = {}
    extend(copyArgs, args)
    for (var i = 0; i < FUNCTION_FIELD_WHITELIST.length; i++) {
        delete copyArgs[FUNCTION_FIELD_WHITELIST[i]]
    }

    extend(createError, copyArgs);
    createError._name = funcName;

    return createError;

    function createError(opts) {
        var result = new Error();

        Object.defineProperty(result, 'type', {
            value: result.type,
            enumerable: true,
            writable: true,
            configurable: true
        });

        var options = {}
        extend(options, args)
        extend(options, opts)
        if (!options.fullType) {
            options.fullType = options.type;
        }

        result.name = funcName
        extend(result, options);
        if (opts && opts.message) {
            result.message = template(opts.message, options);
        } else if (message) {
            result.message = template(message, options);
        }

        return result;
    }
}

function extend(target, source) {
    for (var key in source) {
        if (hasOwnProperty.call(source, key)) {
            target[key] = source[key]
        }
    }
}

function camelCase(str) {
    return str.replace(isWordBoundary, upperCase);
}

function upperCase(_, x) {
    return x.toUpperCase();
}

function has(obj, key) {
    return Object.prototype.hasOwnProperty.call(obj, key);
}
