# body [![build status][1]][2]

Body parsing

Originally taken from [npm-www](https://github.com/isaacs/npm-www)

## Example

```js
var textBody = require("body")
var jsonBody = require("body/json")
var formBody = require("body/form")
var anyBody = require("body/any")
var http = require("http")
var sendJson = require("send-data/json")

http.createServer(function handleRequest(req, res) {
    function send(err, body) {
        sendJson(req, res, body)
    }

    if (req.url === "/body") {
        // all functions can be called with (req, cb)
        textBody(req, send)
    } else if (req.url === "/form") {
        // all functions can be called with (req, opts, cb)
        formBody(req, {}, send)
    } else if (req.url === "/json") {
        // all functions can be called with (req, res, cb)
        jsonBody(req, res, send)
    } else if (req.url === "/any") {
        // all functions can be called with (req, res, opts, cb)
        anyBody(req, res, {}, send)
    }
})
```

`body` simply parses the request body and returns it in the callback. `jsonBody` and `formBody` call JSON.parse and querystring.parse respectively on the body.

anyBody will detect the content-type of the request and use the appropiate body method.

## Example generators

You can use `body` with generators as the body functions will
    return a continuable if you don't pass a callback.

```js
var http = require("http")
var Router = require("routes-router")
var jsonBody = require("body/json")
var formBody = require("body/form")
// async turns a generator into an async function taking a cb
var async = require("gens")

// the router works with normal async functions.
// router automatically handles errors as 500 responses
var app = Router({
    // do whatever you want. the jsonBody error would go here
    errorHandler: function (req, res, err) {
        res.statusCode = 500
        res.end(err.message)
    }
})

app.addRoute("/json", async(function* (req, res) {
    // if jsonBody has an error it just goes to the cb
    // in the called in the router. and it does the correct thing
    // it shows your 500 page.
    var body = yield jsonBody(req, res)

    res.setHeader("content-type", "application/json")
    res.end(JSON.stringify(body))
}))

app.addRoute("/form", async(function* (req, res) {
    var body = yield formBody(req, res)

    res.setHeader("content-type", "application/json")
    res.end(JSON.stringify(body))
}))

// app returned from the router is just a function(req, res) {}
// that dispatches the req/res to the correct route based on
// the routers routing table & req.url
http.createServer(app).listen(8080)
```

## Documentation

### `textBody(req, res?, opts?, cb<Error, String>)`

```ocaml
textBody := (
    req: HttpRequest,
    res?: HttpResponse,
    opts?: {
        limit?: Number,
        cache?: Boolean,
        encoding?: String
    },
    cb: Callback<err: Error, bodyPayload: String>
) => void
```

`textBody` allows you to get the body from any readable stream.
It will read the entire content of the stream into memory and
give it back to you in the callback.

 - `limit`: You can set `opts.limit` to a custom number to change the 
    limit at which `textBody` gives up. By default it will only
    read a 1MB body, if a stream contains more then 1MB it returns
    an error. This prevents someone attacking your HTTP server
    with an infinite body causing an out of memory attack.
 - `encoding`: You can set `encoding`. All encodings that are valid on a 
    [`Buffer`](http://nodejs.org/api/buffer.html#buffer_buffer) are
    valid options. It defaults to `'utf8'`

```js
var textBody = require("body")
var http = require("http")

http.createServer(function (req, res) {
    textBody(req, res, function (err, body) {
        // err probably means invalid HTTP protocol or some shiz.
        if (err) {
            res.statusCode = 500
            return res.end("NO U")
        }

        // I am an echo server
        res.end(body)
    })
}).listen(8080)
```

### `formBody(req, res?, opts?, cb<Error, Any>)`

```ocaml
formBody := (
    req: HttpRequest,
    res?: HttpResponse,
    opts?: {
        limit?: Number,
        encoding?: String,
        querystring: {
            parse: (String, Callback<Error, Any>) => void
        }
    },
    cb: Callback<err: Error, bodyPayload: Any>
) => void
```

`formBody` allows you to get the body of a readable stream. It
does the same as `textBody` but assumes the content is querystring
encoded and parses just like it was a &lt;form&gt; submit.

 - `limit`: same as `textBody`
 - `encoding`: same as `textBody`
 - `querystring`: You can pass a custom querystring parser if 
    you want. It should have a `parse` method that takes a 
    string and a callback. It should return the value in the
    callback or a parsing error

```js
var formBody = require("body/form")
var http = require("http")

http.createServer(function (req, res) {
    formBody(req, res, function (err, body) {
        // err probably means invalid HTTP protocol or some shiz.
        if (err) {
            res.statusCode = 500
            return res.end("NO U")
        }

        // I am an echo server
        res.setHeader("content-type", "application/json")
        res.end(JSON.stringify(body))
    })
}).listen(8080)
```

### `jsonBody(req, res?, opts?, cb<Error, Any>)`

```ocaml
jsonBody := (
    req: HttpRequest,
    res?: HttpResponse,
    opts?: {
        limit?: Number,
        encoding?: String,
        reviver?: (Any) => Any
        JSON?: {
            parse: (String, reviver?: Function, Callback<Error, Any>) => void
        }
    },
    cb: Callback<err: Error, bodyPayload: Any>
) => void
```

`jsonBody` allows you to get the body of a readable stream. It
does the same as `textbody` but assumes the content it a JSON
value and parses it using `JSON.parse`. If `JSON.parse` throws
an exception then it calls the callback with the exception.

 - `limit`: same as `textBody`
 - `encoding`: same as `textBody`
 - `reviver`: A reviver function that will be passed to `JSON.parse`
    as the second argument
 - `JSON`: You can pass a custom JSON parser if you want.
    It should have a `parse` method that takes a string, an
    optional reviver and a callback. It should return the value
    in the callback or a parsing error.

```js
var jsonBody = require("body/json")
var http = require("http")

http.createServer(function (req, res) {
    jsonBody(req, res, function (err, body) {
        // err is probably an invalid json error
        if (err) {
            res.statusCode = 500
            return res.end("NO U")
        }

        // I am an echo server
        res.setHeader("content-type", "application/json")
        res.end(JSON.stringify(body))
    })
}).listen(8080)
```

### `anyBody(req, res?, opts?, cb<Error, Any>)`

```ocaml
anyBody := (
    req: HttpRequest,
    res?: HttpResponse,
    opts?: {
        limit?: Number,
        encoding?: String,
        reviver?: (Any) => Any
        JSON?: {
            parse: (String, reviver?: Function, Callback<Error, Any>) => void
        },
        querystring: {
            parse: (String, Callback<Error, Any>) => void
        }
    },
    cb: Callback<err: Error, bodyPayload: Any>
) => void
```

`anyBody` allows you to get the body of a HTTPRequest. It 
does the same as `textBody` except it parses the `content-type`
header and uses either the jsonBody or the formBody function.

This allows you to write POST route handlers that work with
both ajax and html form submits.

 - `limit`: same as `textBody`
 - `encoding`: same as `textBody`
 - `reviver`: same as `jsonBody`
 - `JSON`: same as `jsonBody`
 - `querystring`: same as `formBody`

```js
var anyBody = require("body/any")
var http = require("http")

http.createServer(function (req, res) {
    anyBody(req, res, function (err, body) {
        // err is probably an invalid json error
        if (err) {
            res.statusCode = 500
            return res.end("NO U")
        }

        // I am an echo server
        res.setHeader("content-type", "application/json")
        res.end(JSON.stringify(body))
    })
}).listen(8080)
```


## Installation

`npm install body`

## Tests

`npm test`

## Contributors

 - Raynos

## MIT Licenced

  [1]: https://secure.travis-ci.org/Raynos/body.png
  [2]: http://travis-ci.org/Raynos/body
