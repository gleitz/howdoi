var testServer = require("test-server")
var test = require("tape")
var sendJson = require("send-data/json")
var after = require("after")

var body = require("../index")
var jsonBody = require("../json")
var formBody = require("../form")
var anyBody = require("../any")

testServer(handleRequest, runTests)

function handleRequest(req, res) {
    function send(err, body) {
        if (err) {
            return sendJson(req, res, err.message)
        }

        sendJson(req, res, body)
    }

    if (req.url === "/body") {
        body(req, res, {}, send)
    } else if (req.url === "/form") {
        formBody(req, res, send)
    } else if (req.url === "/json") {
        jsonBody(req, {}, send)
    } else if (req.url === "/any") {
        anyBody(req, send)
    }
}

function runTests(request, done) {
    test("body works", function (t) {
        t.end = after(2, t.end.bind(t))
        testBody("/body", request, t)

        request({
            uri: "/any",
            body: "foo"
        }, function (err, res, body) {
            t.equal(err, null)
            t.equal(JSON.parse(body), "Could not parse content type header: ")
            t.end()
        })
    })

    test("form works", function (t) {
        t.end = after(2, t.end.bind(t))
        testFormBody("/form", request, t)
        testFormBody("/any", request, t)
    })

    test("json works", function (t) {
        t.end = after(2, t.end.bind(t))
        testJsonBody("/json", request, t)
        testJsonBody("/any", request, t)
    })

    .on("end", done)
}

function testBody(uri, request, t) {
    request({
        uri: uri,
        body: "foo"
    }, function (err, res, body) {
        t.equal(err, null, "error is not null")

        console.log("body", body, JSON.parse(body))
        t.equal(JSON.parse(body), "foo", "body is incorrect")

        t.end()
    })
}

function testFormBody(uri, request, t) {
    request({
        uri: uri,
        form: {
            foo: "bar"
        }
    }, function (err, res, body) {
        t.equal(err, null, "error is not null")

        t.equal(JSON.parse(body).foo, "bar", "body is incorrect")

        t.end()
    })
}

function testJsonBody(uri, request, t) {
    request({
        uri: uri,
        json: {
            foo: "bar"
        }
    }, function (err, res, body) {
        t.equal(err, null, "error is not null")

        t.equal(body.foo, "bar", "body is incorrect")

        t.end()
    })
}
