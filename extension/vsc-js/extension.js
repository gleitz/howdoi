// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { spawn } = require("child_process");

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	async function spawnChild(command, cb) {
		const updatedCommand = howdoiPrefix(command);
		const process = await spawn("howdoi", [updatedCommand, '-n 3']);
		let result = [];
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

	function spliceArr(obj, commentBegin, commentEnd) {
		let dataString = String(obj);
		let lines = dataString.split('\n'+'================================================================================' + '\n' + '\n');
		let newArr = lines.map((elem) => elem.split(' ★'));
		for (let i = 0; i < newArr.length; i++) {
			newArr[i][0] = commentBegin + newArr[i][0] + commentEnd;
		}
		return newArr
	}

	function helperFunc(editor, myArr, userTxt, commentBegin, commentEnd) {
		const newResult = spliceArr(myArr,commentBegin,commentEnd);

		const quickPick = vscode.window.createQuickPick();
			quickPick.items = newResult.map(x => ({label: x[1], link: x[0]}));
			
			quickPick.onDidChangeSelection(([item]) => {
				if (item) {
				editor.edit(edit => {
					edit.replace(editor.selection, userTxt + '\n' + item.link + item.label);
				});	
				quickPick.dispose();
				}
			});
			quickPick.onDidHide(() => quickPick.dispose());
			quickPick.show();		
	}

	function howdoiPrefix(command) {
		const prefix = "howdoi";
		
		if (command.includes(prefix)) {
			const newCommand = command.replace(prefix,'');
			return newCommand;
		}
		else {
			return command;
		}

	}

	function modifyCommentedText(textToBeModified) {
		var regexBegins =  /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
		var regexEnds = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
		let commentBegin;
		let commentEnd;	
		let result;
			
		if (textToBeModified.match(regexBegins) && textToBeModified.match(regexEnds)){
			commentBegin = textToBeModified.match(regexBegins).join();
			commentEnd = textToBeModified.match(regexEnds).join();
			textToBeModified = textToBeModified.replace(regexBegins, '');
			textToBeModified = textToBeModified.replace(regexEnds, '');
			result  = [textToBeModified, commentBegin, commentEnd];	
			return result;
		}
		else if(textToBeModified.match(regexEnds)){
			commentEnd = textToBeModified.match(regexEnds).join();
			textToBeModified = textToBeModified.replace(regexEnds, '');
			result = [textToBeModified,'',commentEnd];
			return result;
		}
		else if(textToBeModified.match(regexBegins)){
			commentBegin = textToBeModified.match(regexBegins).join();
			textToBeModified = textToBeModified.replace(regexBegins, '');
			result = [textToBeModified, commentBegin, ''];	
			return result;
		}
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
		
		const textToBeModified = editor.document.getText(editor.selection);
		let txtArr = modifyCommentedText(textToBeModified);
		const textToBeSearched = txtArr[0];
		const commentBegin = txtArr[1];
		const commentEnd = txtArr[2];

		spawnChild(textToBeSearched, function(myArr) {
			helperFunc(editor, myArr, textToBeModified, commentBegin, commentEnd);
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
