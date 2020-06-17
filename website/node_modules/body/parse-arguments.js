module.exports = parseArguments

function isWritable(stream) {
    return typeof stream.write === "function" &&
        typeof stream.end === "function"
}

function parseArguments(req, res, opts, callback) {
    // (req, cb)
    if (typeof res === "function") {
        callback = res
        opts = {}
        res = null
    }

    // (req, res, cb)
    if (typeof opts === "function") {
        callback = opts
        opts = {}
    }

    // (req, opts, cb)
    if (res && !isWritable(res)) {
        opts = res
        res = null
    }

    // default (req, res, opts, cb)
    return { req: req, res: res, opts: opts, callback: callback }
}
