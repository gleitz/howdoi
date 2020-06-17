# safe-json-parse

[![build status][1]][2] [![dependency status][3]][4]

<!-- [![browser support][5]][6] -->

Parse JSON safely without throwing

## Example

```js
var safeParse = require("safe-json-parse")

safeParse("{}", function (err, json) {
    /* we have json */
})

safeparse("WRONG", function (err) {
    /* we have err! */
})
```

## Installation

`npm install safe-json-parse`

## Contributors

 - Raynos

## MIT Licenced


  [1]: https://secure.travis-ci.org/Raynos/safe-json-parse.png
  [2]: https://travis-ci.org/Raynos/safe-json-parse
  [3]: https://david-dm.org/Raynos/safe-json-parse.png
  [4]: https://david-dm.org/Raynos/safe-json-parse
  [5]: https://ci.testling.com/Raynos/safe-json-parse.png
  [6]: https://ci.testling.com/Raynos/safe-json-parse
