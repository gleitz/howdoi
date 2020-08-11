# Code Editor Integration Development

Simplifies the process of integrating howdoi as a code editor extension.

## Description

The Code Editor Integration plug-in is ran by calling the `runHowdoi` function which takes in a user's query of type string. The parameter is encapsulated by a single line comment and is formatted as follows:

    // howdoi query

`runHowdoi` returns an Object with the structure:

    {
        question: string
        answer: string[]
        link: string[] 
    }

The Object values:
* question contains the user's query
* answer contains the three possible answers to the user's query 
* link contains the three possible links to the answer encapsulated by a single line comment


## Installation

To install all necessary packages run:

    npm install

## Development

To compile the script:

    npm run compile

To run the script:

    npm start

To compile and run the script:

    npm run build

To run the testing script:

    npm test

## Usage

To utilize this plug-in to create a howdoi extension for a code editor: 

1. Copy the `code-editor-integration` folder into your workspace and remove the `node_modules` folder by adding the script
    
        "copy": "ncp ../code-editor-integration/ src/code-editor-integration/"
        "clean": "rimraf ./src/code-editor-integration/node_modules"
  
    into your `package.json` file and running it.
    First, you will need to install [ncp](https://www.npmjs.com/package/ncp) and [rimraf](https://www.npmjs.com/package/rimraf).

2. Import the `plugin.ts` file into your main file.
    
3. Call the `runHowdoi` function.

Refer to `vscode-howdoi` for an example.
