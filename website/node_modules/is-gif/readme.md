# is-gif [![Build Status](https://travis-ci.com/sindresorhus/is-gif.svg?branch=master)](https://travis-ci.com/sindresorhus/is-gif)

> Check if a Buffer/Uint8Array is a [GIF](https://en.wikipedia.org/wiki/Graphics_Interchange_Format) image


## Install

```
$ npm install is-gif
```


## Usage

```js
const readChunk = require('read-chunk');
const isGif = require('is-gif');

const buffer = readChunk.sync('unicorn.gif', 0, 3);

isGif(buffer);
//=> true
```


## API

### isGif(input)

#### input

Type: `Buffer` `Uint8Array`

It only needs the first 3 bytes.


## Related

- [file-type](https://github.com/sindresorhus/file-type) - Detect the file type of a Buffer/Uint8Array


## License

MIT © [Sindre Sorhus](https://sindresorhus.com)
