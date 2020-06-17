/*!
 * list-item <https://github.com/jonschlinkert/list-item>
 *
 * Copyright (c) 2015, Jon Schlinkert.
 * Licensed under the MIT License.
 */

'use strict';

var isNumber = require('is-number');
var expand = require('expand-range');
var repeat = require('repeat-string');
var extend = require('extend-shallow');

/**
 * Expose `listitem`
 */

module.exports = listitem;

/**
 * Returns a function to generate a plain-text/markdown list-item,
 * allowing options to be cached for subsequent calls.
 *
 * ```js
 * var li = listitem(options);
 *
 * li(0, 'Level 0 list item');
 * //=> '- Level 0 list item'
 *
 * li(1, 'Level 1 list item');
 * //=> '  * Level 1 list item'
 *
 * li(2, 'Level 2 list item');
 * //=> '    + Level 2 list item'
 * ```
 *
 * @param  {Object} `options` pass options to customize list item characters, indentation, etc.
 * @param {Boolean} `options.nobullet` Pass true if you only want the list iten and identation, but no bullets.
 * @param {String} `options.indent` The amount of leading indentation to use. default is `  `.
 * @param {String|Array} `options.chars` If a string is passed, [expand-range][] will be used to generate an array of bullets (visit [expand-range][] to see all options.) Or directly pass an array of bullets, numbers, letters or other characters to use for each list item. Default `['-', '*', '+']`
 * @param {Function} `fn` pass a function [expand-range][] to modify the bullet for an item as it's generated. See the [examples](#examples).
 * @return {String} returns a formatted list item
 * @api public
 */

function listitem(opts, fn) {
  if (typeof opts === 'function') {
    fn = opts;
    opts = {};
  }

  opts = opts || {};
  var ch = character(opts, fn);

  return function(lvl, str) {
    if (!isNumber(lvl)) {
      throw new Error('expected level to be a number');
    }

    // cast to integer
    lvl = +lvl;

    var bullet = ch ? ch[lvl % ch.length] : '';
    var indent = typeof opts.indent !== 'string'
      ? (lvl > 0 ? '  ' : '')
      : opts.indent;

    var prefix = !opts.nobullet
      ? bullet + ' '
      : '';

    var res = '';
    res += repeat(indent, lvl);
    res += prefix;
    res += str;
    return res;
  };
}

/**
 * Generate and cache the array of characters to use as
 * bullets.
 *
 * - http://spec.commonmark.org/0.19/#list-items
 * - https://daringfireball.net/projects/markdown/syntax#list
 * - https://help.github.com/articles/markdown-basics/#lists
 *
 * @param  {Object} `opts` Options to pass to [expand-range][]
 * @param  {Function} `fn`
 * @return {Array}
 */

function character(opts, fn) {
  opts = extend({}, opts);
  var chars = opts.chars || ['-', '*', '+'];

  if (typeof chars === 'string') {
    return expand(chars, opts, fn);
  }

  if (typeof fn === 'function') {
    return chars.map(fn);
  }
  return chars;
}
