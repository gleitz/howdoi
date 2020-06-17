var querystringParse = require("querystring").parse

var body = require("./index.js")
var parseArguments = require("./parse-arguments.js")

module.exports = formBody

function formBody(req, res, opts, callback) {
    var args = parseArguments(req, res, opts, callback)
    req = args.req
    res = args.res
    opts = args.opts
    callback = args.callback

    if (!callback) {
        return formBody.bind(null, req, res, opts)
    }

    var parse = opts.querystring ?
        opts.querystring.parse : defaultQueryStringParse

    body(req, res, opts, function (err, body) {
        if (err) {
            return callback(err)
        }

        parse(body, callback)
    })
}

function defaultQueryStringParse(str, callback) {
    callback(null, querystringParse(str))
}
