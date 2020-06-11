// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { spawn } = require("child_process");
const { create } = require('domain');
const { textChangeRangeNewSpan } = require('typescript');

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
		process.stdout.on("data", data => {

			result.push(String(data));
			
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

	function spliceArr(obj) {

		let dataString = String(obj);
		let lines = dataString.split('\n'+'================================================================================' + '\n');
		
		let newArr = lines.map((elem) => elem.split(' ★'));
		
		return newArr
	}

	function helperFunc(editor, myArr, userTxt) {

		const newResult = spliceArr(myArr);

		const quickPick = vscode.window.createQuickPick();
			quickPick.items = newResult.map(x => ({label: x[1], link: x[0]}));
			
			quickPick.onDidChangeSelection(([item]) => {
				// item.answer
				if (item) {
				
				editor.edit(edit => {
					edit.replace(editor.selection, userTxt + '\n' + item.link + item.label);
					// 								item.text + \n + item.link + \n + item.answer
				});
				quickPick.dispose();
				}
			});
			quickPick.onDidHide(() => quickPick.dispose());
			quickPick.show();			
	}
	function modifyCommentedText(textToBeModified){
		var regexBegins =  /^[!@#<>/\$%\^\&*\)\(+=._-]+/
		var regexEnds = /[!@#<>/\$%\^\&*\)\(+=._-]+$/
			
			
			if (textToBeModified.match(regexBegins) && textToBeModified.match(regexEnds)){
				textToBeModified = textToBeModified.replace(regexBegins, '')
				textToBeModified = textToBeModified.replace(regexEnds, '')
			}
			else if(textToBeModified.match(regexEnds)){
				textToBeModified = textToBeModified.replace(regexEnds, '')
			}
			else if(textToBeModified.match(regexBegins)){
				textToBeModified = textToBeModified.replace(regexBegins, '')
			}
		
		return textToBeModified
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

		var textToBeModified = editor.document.getText(editor.selection);
		var textToBeSearched = modifyCommentedText(textToBeModified)
	
		spawnChild(textToBeSearched, function(myArr) {
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
