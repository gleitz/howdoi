var jsonParse = require("safe-json-parse")

var body = require("./index.js")
var parseArguments = require("./parse-arguments.js")

module.exports = jsonBody

function jsonBody(req, res, opts, callback) {
    var args = parseArguments(req, res, opts, callback)
    req = args.req
    res = args.res
    opts = args.opts
    callback = args.callback

    if (!callback) {
        return jsonBody.bind(null, req, res, opts)
    }

    var parse = opts.JSON ? opts.JSON.parse : jsonParse
    var reviver = opts.reviver || null

    body(req, res, opts, function (err, body) {
        if (err) {
            return callback(err)
        }

        parse(body, reviver, callback)
    })
}
