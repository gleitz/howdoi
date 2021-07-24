## Extension development

You can integrate howdoi as a code editor extension. For this, you need to edit the files within the [extension/code-editor-integration](https://github.com/gleitz/howdoi/tree/master/extension/code-editor-integration) folder.
To improve the Visual Studio Code howdoi extension, edit the files within the [extension/vscode-howdoi](https://github.com/gleitz/howdoi/tree/master/extension/vscode-howdoi) folder and republish the extension.

#### How to integrate howdoi as a code editor extension?

1. The Code Editor Integration plug-in runs when you call
   ` runHowdoi` function which takes in a user’s query(type = string). The parameter is encapsulated by a single line comment and is formatted as : `// howdoi query`

   `runHowdoi` function returns and Object which looks like :

```
{
   Question: string
   Answer : string[]
   Link : string[]
}
```

2. What are these object values?

- question : it contains the user’s query encapsulated by a single line comment
- answer : contains the three possible answers to the user’s query.
- link : link contains the three possible links to the answer encapsulated by a single line comment

3. To start with development, you need to first install howdoi on your machine. Steps to do that lie here.

#### Development

Next, install all important packages by running `npm install`

- To compile the script, run `npm run compile`
- To run the script , run `npm start`
- To compile and run the script, run `npm run build`
- To run the testing script, run `npm test`
- Now, to utilize the plug-in to create a howdoi extension, you need to do the following

#### Integration

To use the plug-in to create a howdoi extension, follow these steps:

- Copy the `code-editor-integration` folder in your workspace and remove `node-modules` folder. You can do this by adding the script in your `package.json` file and running it. But, first you will need to install ncp and rimraf.:

```
"copy": "ncp ../code-editor-integration/ src/code-editor-integration/"
"clean": "rimraf ./src/code-editor-integration/node_modules"
```

- Import the `plugin.ts` file into your main file.
- Call the `runHowdoi` function.

#### Visual Code Extension development

To begin the development for Visual Studio Code extension, install all the necessary packages:

`npm install`

Then precompile the extension :

`npm run precompile`

To run and test extension, utilize the Visual Studio Code’s debugging tools.
