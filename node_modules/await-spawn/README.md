# await-spawn

> `child_process.spawn()` wrapped in a `Promise` for doing async/await.

[![npm](https://img.shields.io/npm/v/await-spawn.svg)](https://www.npmjs.com/package/await-spawn)
![Node version](https://img.shields.io/node/v/await-spawn.svg)
[![Build Status](https://travis-ci.org/ralphtheninja/await-spawn.svg?branch=master)](https://travis-ci.org/ralphtheninja/await-spawn)
[![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)

## Install

```
$ npm i await-spawn -S
```

## Usage

```js
const spawn = require('await-spawn')

const main = async () => {
  const bl = await spawn('ls', [ '-al' ])
  console.log(bl.toString())
}

main()
```

## Api

Exposes a single function, which has the same api as `child_process.spawn()`.

Returns a `Promise` with `.child` set to the spawned child process. The `Promise` resolves to the buffered output of `child.stdout` in the form of a [`BufferList`] object.

If there was an error, the `Promise` rejects with an `Error` object, which has the following extra properties:

* `code` the error code
* `stderr` the buffered output of `stderr` in the form of a [`BufferList`] object

Note that `child.stdout` doesn't exist if `options.stdio === 'inherit'`, so the `Promise` resolves to `''`.

## License

MIT

[`BufferList`]: https://github.com/rvagg/bl
