var TypedError = require("error/typed")

var parseArguments = require("./parse-arguments.js")
var jsonBody = require("./json.js")
var formBody = require("./form.js")

var jsonType = "application/json"
var formType = "application/x-www-form-urlencoded"
var INVALID_CONTENT_TYPE = TypedError({
    message: "Could not parse content type header: {contentType}",
    type: "invalid.content.type",
    statusCode: 415,
    contentType: null
})

module.exports = anyBody

function anyBody(req, res, opts, callback) {
    var args = parseArguments(req, res, opts, callback)
    req = args.req
    res = args.res
    opts = args.opts
    callback = args.callback

    if (!callback) {
        return anyBody.bind(null, req, res, opts)
    }

    var contentType = req.headers["content-type"] || ""

    if (contentType.indexOf(jsonType) !== -1) {
        jsonBody(req, res, opts, callback)
    } else if (contentType.indexOf(formType) !== -1) {
        formBody(req, res, opts, callback)
    } else {
        callback(INVALID_CONTENT_TYPE({contentType: contentType}))
    }
}
