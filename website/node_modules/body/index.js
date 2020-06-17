var rawBody = require("raw-body")
var cache = require("continuable-cache")

var parseArguments = require("./parse-arguments.js")

var ONE_MB = 1024 * 1024
var THUNK_KEY = '__npm_body_thunk_cache__';

module.exports = body

function parseBodyThunk(req, res, opts) {
    return function thunk(callback) {
        var limit = "limit" in opts ? opts.limit : ONE_MB
        var contentLength = req.headers ?
            Number(req.headers["content-length"]) : null;

        rawBody(req, {
            limit: limit,
            length: contentLength,
            encoding: "encoding" in opts ? opts.encoding : true
        }, callback);
    };
}

function body(req, res, opts, callback) {
    var args = parseArguments(req, res, opts, callback)
    req = args.req
    res = args.res
    opts = args.opts
    callback = args.callback

    var thunk;

    if (opts.cache) {
        var thunk = req[THUNK_KEY] ||
            cache(parseBodyThunk(req, res, opts));
        req[THUNK_KEY] = thunk;
    } else {
        thunk = parseBodyThunk(req, res, opts);
    }

    if (!callback) {
        return thunk;
    }

    thunk(callback);
}
