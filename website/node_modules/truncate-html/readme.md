<h1 align="center">truncate-html</h1>

<h5 align="center"> Truncate html string(even contains emoji chars) and keep tags in safe. You can custom ellipsis sign, ignore unwanted elements and truncate html by words. </h5>
<div align="center">
  <a href="https://travis-ci.org/evecalm/truncate-html">
    <img src="https://travis-ci.org/evecalm/truncate-html.svg?branch=master" alt="Travis CI">
  </a>
  <a href="#readme">
    <img src="https://badges.frapsoft.com/typescript/code/typescript.svg?v=101" alt="code with typescript" height="20">
  </a>
  <a href="#readme">
    <img src="https://badge.fury.io/js/truncate-html.svg" alt="npm version" height="18">
  </a>
  <a href="https://www.npmjs.com/package/truncate-html">
    <img src="https://img.shields.io/npm/dm/truncate-html.svg" alt="npm version" height="18">
  </a>
</div>

<br>

**Notice** This is a node module depends on [cheerio](https://github.com/cheeriojs/cheerio) _can only run on nodejs_. If you need a browser version, you may consider [truncate](https://github.com/pathable/truncate) or [nodejs-html-truncate](https://github.com/huang47/nodejs-html-truncate).

```javascript
const truncate = require('truncate-html')
truncate('<p><img src="xxx.jpg">Hello from earth!</p>', 2, { byWords: true })
// => <p><img src="xxx.jpg">Hello from ...</p>
```

## Installation

`npm install truncate-html` <br>
or <br>
`yarn add truncate-html`

## Try it online

Click **<https://npm.runkit.com/truncate-html>** to try.

## API

```javascript
/**
 * truncate html
 * @method truncate(html, [length], [options])
 * @param  {String|CheerioStatic}         html    html string to truncate, or  existing cheerio instance(aka cheerio $)
 * @param  {Object|number}  length how many letters(words if `byWords` is true) you want reserve
 * @param  {Object|null}    options
 * @param  {Boolean}        [options.stripTags] remove all tags, default false
 * @param  {String}         [options.ellipsis] ellipsis sign, default '...'
 * @param  {Boolean}        [options.decodeEntities] decode html entities(e.g. convert `&amp;` to `&`) before
 *                                                   counting length, default false
 * @param  {String|Array}   [options.excludes] elements' selector you want ignore
 * @param  {Number}         [options.length] how many letters(words if `byWords` is true)
 *                                           you want reserve
 * @param  {Boolean}        [options.byWords] if true, length means how many words to reserve
 * @param  {Boolean|Number} [options.reserveLastWord] how to deal with when truncate in the middle of a word
 *                                1. by default, just cut at that position.
 *                                2. set it to true, with max exceed 10 letters can exceed to reserver the last word
 *                                3. set it to a positive number decide how many letters can exceed to reserve the last word
 *                                4. set it to negetive number to remove the last word if cut in the middle.
 * @param  {Boolean}        [options.keepWhitespaces] keep whitespaces, by default continuous
 *                                spaces will be replaced with one space
 *                                set it true to reserve them, and continuous spaces will count as one
 * @return {String}
 */
truncate(html, [length], [options])
// and truncate.setup to change default options
truncate.setup(options)
```

### Default options

```js
{
  byWords: false,
  stripTags: false,
  ellipsis: '...',
  decodeEntities: false,
  keepWhitespaces: false,
  excludes: '',
  reserveLastWord: false,
  keepWhitespaces: false
}
```

You can change default options by using `truncate.setup`

e.g.

```js
truncate.setup({ stripTags: true, length: 10 })
truncate('<p><img src="xxx.jpg">Hello from earth!</p>')
// => Hello from
```

or use existing [cheerio instance](https://github.com/cheeriojs/cheerio#loading)

```js
import * as cheerio from 'cheerio'
truncate.setup({ stripTags: true, length: 10 })
// truncate option `decodeEntities` will not work
//    you should config it in cheerio options by yourself
const $ = cheerio.load('<p><img src="xxx.jpg">Hello from earth!</p>', {
  /** set decodeEntities if you need it */
  decodeEntities: true
  /* any cheerio instance options*/
})
truncate($)
// => Hello from
```

## Notice

### Typescript support

This lib is written with typescript and has a defination file along with it. You may need to update your `tsconfig.json` by adding `"esModuleInterop": true` to the `compilerOptions` if you encounter some typing errors, see #19.

### About final string length

If the html string content's length is shorter than `options.length`, then no ellipsis will be appended to the final html string. If longer, then the final string length will be `options.length` + `options.ellipsis`. And if you set `reserveLastWord` to true of none zero number, the final string will be various.

### About html comments

All html comments `<!-- xxx -->` will be removed

### About dealing with none alphabetic languages

When dealing with none alphabetic languages, such as Chinese/Japanese/Korean, they don't separate words with whitespaces, so options `byWords` and `reserveLastWord` should only works well with alphabetic languages.

And the only dependency of this project `cheerio` has an issue when dealing with none alphabetic languages, see [Known Issues](#known-issues) for details.

### Using existing cheerio instance

If you want to use existing cheerio instance, truncate option `decodeEntities` will not work, you should set it in your own cheerio instance:

```js
const $ = cheerio.load(`${html}`, {
  decodeEntities: true
  /** other cheerio options */
})
```

## Examples

```javascript
var truncate = require('truncate-html')

// truncate html
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, 10)
// returns: <p><img src="abc.png">This is a ...</p>

// truncate string with emojis
var string = '<p>poo 💩💩💩💩💩<p>'
truncate(string, 6)
// returns: <p>poo 💩💩...</p>

// with options, remove all tags
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, 10, { stripTags: true })
// returns: This is a ...

// with options, truncate by words.
//  if you try to truncate none alphabet language(like CJK)
//      it will not act as you wish
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, 3, { byWords: true })
// returns: <p><img src="abc.png">This is a ...</p>

// with options, keep whitespaces
var html = '<p>         <img src="abc.png">This is a string</p> for test.'
truncate(html, 10, { keepWhitespaces: true })
// returns: <p>         <img src="abc.png">This is a ...</p>

// combine length and options
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, {
  length: 10,
  stripTags: true
})
// returns: This is a ...

// custom ellipsis sign
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, {
  length: 10,
  ellipsis: '~'
})
// reutrns: <p><img src="abc.png">This is a ~</p>

// exclude some special elements(by selector), they will be removed before counting content's length
var html = '<p><img src="abc.png">This is a string</p> for test.'
truncate(html, {
  length: 10,
  ellipsis: '~',
  excludes: 'img'
})
// reutrns: <p>This is a ~</p>

// exclude more than one category elements
var html =
  '<p><img src="abc.png">This is a string</p><div class="something-unwanted"> unwanted string inserted ( ´•̥̥̥ω•̥̥̥` ）</div> for test.'
truncate(html, {
  length: 20,
  stripTags: true,
  ellipsis: '~',
  excludes: ['img', '.something-unwanted']
})
// returns: This is a string for~

// handing encoded characters
var html = '<p>&nbsp;test for &lt;p&gt; encoded string</p>'
truncate(html, {
  length: 20,
  decodeEntities: true
})
// returns: <p> test for &lt;p&gt; encode...</p>

// when set decodeEntities false
var html = '<p>&nbsp;test for &lt;p&gt; encoded string</p>'
truncate(html, {
  length: 20,
  decodeEntities: false // this is the dafault value
})
// returns: <p>&nbsp;test for &lt;p...</p>

// and there may be a surprise by setting `decodeEntities` to true  when handing CJK characters
var html = '<p>&nbsp;test for &lt;p&gt; 中文 string</p>'
truncate(html, {
  length: 20,
  decodeEntities: true
})
// returns: <p> test for &lt;p&gt; &#x4E2D;&#x6587; str...</p>
// to fix this, see below for instructions
```

for More usages, check [truncate.spec.ts](./test/truncate.spec.ts)

## Known issues

Known issues about handing CJK(Chinese/Japanese/Korean) characters when set the option `decodeEntities` to `true`.

You have seen the option `decodeEntities`, it's really magic! When it's true, encoded html entities will be decoded automatically, so `&amp;` will be treat as a single character. This is probably what we want. But, if there are CJK characters in the html string, they will be replaced by characters like `&#xF6;`(still count as one character when truncating) in the final html you get. That's confused.

To fix this, you have two choices:

- keep the option `decodeEntities` false, but `&amp;` will treat as five characters.
- modify cheerio's source code: find out the function `getInverse` in the file `./node_modules/cheerio/node_modules/entities/lib/decode.js`, comment out the last line `.replace(re_nonASCII, singleCharReplacer);`.

## Credits

Thanks to:

- [@calebeno](https://github.com/calebeno) es6 support and unit tests
- [@aaditya-thakkar](https://github.com/aaditya-thakkar) emoji truncating support
