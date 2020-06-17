#!/usr/bin/env node
'use strict';
const {spawn} = require('child_process');
const jpegtran = require('.');

const input = process.argv.slice(2);

spawn(jpegtran, input, {stdio: 'inherit'})
	.on('exit', process.exit);
