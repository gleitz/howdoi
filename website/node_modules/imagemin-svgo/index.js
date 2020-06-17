'use strict';
const isSvg = require('is-svg');
const SVGO = require('svgo');

module.exports = options => buffer => {
	options = Object.assign({multipass: true}, options);

	if (!isSvg(buffer)) {
		return Promise.resolve(buffer);
	}

	if (Buffer.isBuffer(buffer)) {
		buffer = buffer.toString();
	}

	const svgo = new SVGO(options);
	return svgo.optimize(buffer).then(result => Buffer.from(result.data));
};
