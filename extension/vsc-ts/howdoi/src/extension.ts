import * as vscode from 'vscode';
import * as cp from "child_process";


export function activate(context: vscode.ExtensionContext) {

	
	async function spawnChild(command:string, cb:any) {
		const updatedCommand = howdoiPrefix(command);
		const process = await cp.spawn("howdoi", [updatedCommand, '-n 3']);
		let result:string[] = [];
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

	function spliceArr(obj:string[], commentBegin:string, commentEnd:string) {
		let dataString = String(obj);
		let lines = dataString.split('\n'+'================================================================================' + '\n' + '\n');
		let newArr:string[][] = lines.map((elem) => elem.split(' ★'));
		for (let i = 0; i < newArr.length; i++) {
			newArr[i][0] = commentBegin + newArr[i][0] + commentEnd;
		}
		return newArr;
	}

	function helperFunc(editor:any, myArr:string[], userTxt:string, commentBegin:string, commentEnd:string) {
		const newResult = spliceArr(myArr,commentBegin,commentEnd);

		const quickPick = vscode.window.createQuickPick();
			quickPick.items = newResult.map((x:any) => ({label: x[1], link: x[0]}));
			quickPick.onDidChangeSelection(([item]) => {
				if (item) {
				editor.edit((edit:any) => {
					edit.replace(editor.selection, userTxt + '\n' + item.link + item.label);
				});	
				quickPick.dispose();
				}
			});
			quickPick.onDidHide(() => quickPick.dispose());
			quickPick.show();		
	}

	function howdoiPrefix(command:string) {
		const prefix = "howdoi";
		
		if (command.includes(prefix)) {
			const newCommand = command.replace(prefix,'');
			return newCommand;
		}
		else {
			return command;
		}

	}

	function modifyCommentedText(textToBeModified:string) {
		const regexBegins:RegExp =  /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
		const regexEnds:RegExp = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
		let commentBegin:string;
		let commentEnd:string;	
		let result:string[];
			
		if (textToBeModified.match(regexBegins) && textToBeModified.match(regexEnds)){
			commentBegin = textToBeModified.match(regexBegins)!.join();
			commentEnd = textToBeModified.match(regexEnds)!.join();
			textToBeModified = textToBeModified.replace(regexBegins, '');
			textToBeModified = textToBeModified.replace(regexEnds, '');
			result = [textToBeModified, commentBegin, commentEnd];
			return result;
		}
		else if(textToBeModified.match(regexEnds)){
			commentEnd = textToBeModified.match(regexEnds)!.join();
			textToBeModified = textToBeModified.replace(regexEnds, '');
			result = [textToBeModified,'',commentEnd];
			return result;
		}
		else if(textToBeModified.match(regexBegins)){
			commentBegin = textToBeModified.match(regexBegins)!.join();
			textToBeModified = textToBeModified.replace(regexBegins, '');
			result = [textToBeModified, commentBegin, ''];
			return result;
		}
	}

	
	let disposable = vscode.commands.registerCommand('howdoi.extension', () => {
		

		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showInformationMessage('create a file to enable howdoi');
			return;
		}

		const textToBeModified:string = editor.document.getText(editor.selection);
		let txtArr:string[]|undefined = modifyCommentedText(textToBeModified);
		const textToBeSearched:string = txtArr[0];
		const commentBegin:string  = txtArr[1];
		const commentEnd:string = txtArr[2];

		spawnChild(textToBeSearched, function(myArr:string[]) {
			helperFunc(editor, myArr, textToBeModified, commentBegin, commentEnd);
		});


	});

	context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() {}
