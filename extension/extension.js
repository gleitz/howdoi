// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { spawn } = require("child_process");
const { create } = require('domain');

// const fs = require("fs");
// const path = require("path");

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	async function spawnChild(command, cb) {
		const process = await spawn("howdoi", [command, '-n 3']);
		let result = []
		
		// {{link: ww.com, answer: suggestions}}
		// for each element, get the first line->link, the rest is the answer
		process.stdout.on("data", data => {

			result = createObj(data);
			console.log('lines: ', result);
			// let suggestions = JSON.stringify(createObj(data));
			// console.log('suggestions: ', suggestions);
			// suggestions.map((elem) => result.push(suggestions[elem]));
			// result.push(JSON.stringify(suggestions)); 
			// console.log('results: ', result);
			
		});

		process.stderr.on("data", data => {
			console.log(`stderr: ${data}`);
		});
		
		process.on('error', (error) => {
			console.log(`error: ${error.message}`);
		});
		
		process.on("close", code => {
			console.log(`child process exited with code ${code}`);
			cb(result);
		});
		
	}

	function createObj(obj) {
		// let suggestions = new Object();
		let dataString = String(obj);
		let lines = dataString.split('\n'+'================================================================================' + '\n');
		// let newArr = lines.map((elem) => elem.split(' ★'));
		// for (let i = 0; i < newArr.length; i++) { 
		// 	suggestions[i] = {}
		// 	suggestions[i]['link'] = newArr[i][0];
		// 	suggestions[i]['answer'] = String(newArr[i].slice(1));
		// } 
		return lines
	}

	function helperFunc(editor, myArr) {
		const quickPick = vscode.window.createQuickPick();
			quickPick.items = myArr.map(x => ({label: x}));
			quickPick.onDidChangeSelection(([item]) => {
				if (item) {
				// vscode.window.showInformationMessage(item.label);
				editor.edit(edit => {
					edit.replace(editor.selection, item.label);
				});
				quickPick.dispose();
				}
			});
			quickPick.onDidHide(() => quickPick.dispose());
			quickPick.show();			
	}


	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('howdoi.extension', function () {
		// The code you place here will be executed every time your command is executed
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showInformationMessage('create a file to enable howdoi');
			return;
		}

		const text = editor.document.getText(editor.selection);
		
		spawnChild(text, function(myArr) {
			helperFunc(editor, myArr);	
		});


	});

	context.subscriptions.push(disposable);
}
exports.activate = activate;

// this method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
