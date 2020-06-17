'use strict';
const fileType = require('file-type');

module.exports = input => {
	const match = fileType(input);

	if (!match) {
		return false;
	}

	return match.ext === 'gif';
};
