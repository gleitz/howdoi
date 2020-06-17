/// <reference types="node"/>

declare const isSvg: {
	/**
	Check if a string or buffer is [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics).

	@param input - The data to check.
	@returns Whether `input` is SVG or not.

	@example
	```
	import isSvg = require('is-svg');

	isSvg('<svg xmlns="http://www.w3.org/2000/svg"><path fill="#00CD9F"/></svg>');
	//=> true
	```
	*/
	(input: string | Buffer): boolean;

	// TODO: Remove this for the next major release, refactor the whole definition to:
	// declare function isSvg(input: string | Buffer): boolean;
	// export = isSvg;
	default: typeof isSvg;
};

export = isSvg;
