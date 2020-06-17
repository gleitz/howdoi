# continuable-cache

<!-- [![build status][1]][2] [![dependency status][3]][4]

[![browser support][5]][6] -->

Cache a continuable

## Example

```js
var cache = require("continuable-cache")
var fs = require("fs")

var readFile = function (uri) { return function (cb) {
    fs.readFile(uri, cb)
} }

var continuableFile = readFile("./package.json")

var cached = cache(continuableFile)

// will only do one file read operation
cached(function (err, file) {
    /* calls out to fs.readFile */
})

cached(function (err, file) {
    /* get's either err or file from cache in cached */
})
```

## Installation

`npm install continuable-cache`

## Contributors

 - Raynos

## MIT Licenced

  [1]: https://secure.travis-ci.org/Raynos/continuable-cache.png
  [2]: http://travis-ci.org/Raynos/continuable-cache
  [3]: https://david-dm.org/Raynos/continuable-cache/status.png
  [4]: https://david-dm.org/Raynos/continuable-cache
  [5]: https://ci.testling.com/Raynos/continuable-cache.png
  [6]: https://ci.testling.com/Raynos/continuable-cache
