#!/usr/bin/env node
'use strict';
const {spawn} = require('child_process');
const optipng = require('.');

const input = process.argv.slice(2);

spawn(optipng, input, {stdio: 'inherit'})
	.on('exit', process.exit);
