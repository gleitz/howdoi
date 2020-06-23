import * as vscode from 'vscode';
import * as cp from "child_process";

const HOWDOI_PREFIX = 'howdoi';

interface HowdoiResult {
    question: string;
    answer: string[];
    link: string[];   
}

export function activate(context: vscode.ExtensionContext) {
	
	async function spawnChild(command:string, callback:any) {
		const commandWithoutPrefix = removeHowdoiPrefix(command);
		const process = await cp.spawn("howdoi", [commandWithoutPrefix, '-n 3']);
		let howdoiCommandOutput:string = '';
		process.stdout.on("data", (data:any) => {
			howdoiCommandOutput += String(data);
		});
	
		process.stderr.on("data", (data:any) => {
			console.log(`stderr: ${data}`);
		});
		
		process.on('error', (error:any) => {
			console.log(`error: ${error.message}`);
		});
		
		process.on("close", (code:any) => {
			console.log(`child process exited with code ${code}`);
			return callback(howdoiCommandOutput);
		});
	}

	function removeHowdoiPrefix(command:string): string {
		if (!command.trim().startsWith(HOWDOI_PREFIX)) {
			return command;
		}
		return command.replace(HOWDOI_PREFIX, '');
	}

	function modifyCommentedText(userCommand:string): string[]|null {
		/* This function finds the comment regex, removes it from the string and returns an array 
		with the modified string, the beginning comment regex, ending comment regex */
		const commentStartRegex:RegExp =  /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
		const commentEndRegex:RegExp = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
		let commentBegin:string;
		let commentEnd:string;	
		let userCommandWithoutComment:string[];
			
		if (userCommand.match(commentStartRegex) && userCommand.match(commentEndRegex)){
			commentBegin = userCommand.match(commentStartRegex)!.join();
			commentEnd = userCommand.match(commentEndRegex)!.join();
			userCommand = userCommand.replace(commentStartRegex, '');
			userCommand = userCommand.replace(commentEndRegex, '');
			userCommandWithoutComment = [userCommand, commentBegin, commentEnd];
			return userCommandWithoutComment;
		}
		else if(userCommand.match(commentEndRegex)){
			commentEnd = userCommand.match(commentEndRegex)!.join();
			userCommand = userCommand.replace(commentEndRegex, '');
			userCommandWithoutComment = [userCommand,'',commentEnd];
			return userCommandWithoutComment;
		}
		else if(userCommand.match(commentStartRegex)){
			commentBegin = userCommand.match(commentStartRegex)!.join();
			userCommand= userCommand.replace(commentStartRegex, '');
			userCommandWithoutComment = [userCommand, commentBegin, ''];
			return userCommandWithoutComment;
		}
		else {
			return null;
		}
	}

	function organizeHowdoiOutput(howdoiOutput:string, commentBegin:string, commentEnd:string): string[][] {
		/* Creates an array from the howdoiOutput string in which each element 
		is one of three answers from the usersCommand */
		let howdoiAnswersArr = howdoiOutput.split('\n'+'================================================================================' + '\n' + '\n');
		/* Creates a 2D array from howdoiAnswersArr in which each element is an array which denotes
		 one of three answers from the usersCommand, and the elements in that array are the link and answer */
		let newHowdoiAnswersArr:string[][] = howdoiAnswersArr.map((elem) => elem.split(' ★'));
		//  The comment Regex is added to the link string
		for (let i = 0; i < newHowdoiAnswersArr.length; i++) {
			newHowdoiAnswersArr[i][0] = commentBegin + newHowdoiAnswersArr[i][0] + commentEnd;
		}
	
		return newHowdoiAnswersArr;
	}

	function createHowdoiResult(howdoiResultArr:string[][], userCommand:string): HowdoiResult {
		let howdoiResultObj:HowdoiResult = {question: userCommand, answer: [], link: []};
		
		for (let i = 0; i < howdoiResultArr.length; i++) {
			howdoiResultObj.link.push(howdoiResultArr[i][0]);
			howdoiResultObj.answer.push(howdoiResultArr[i][1]);
		}
	
		return howdoiResultObj;
	}

	function howdoiResult(editor:any, howdoiOutput:string, userCommand:string, commentBegin:string, commentEnd:string): HowdoiResult {
		const organizedHowdoiArr:string[][] = organizeHowdoiOutput(howdoiOutput, commentBegin, commentEnd);
		const howdoiResultObj:HowdoiResult = createHowdoiResult(organizedHowdoiArr, userCommand);
		return howdoiResultObj;
	}

	function quickPicker(editor:any, howdoiResultObj:HowdoiResult, userCommand:string): void {
		const quickPick = vscode.window.createQuickPick();
		
		quickPick.items = howdoiResultObj.answer.map((answer:any) => (
			{label: answer, link:  howdoiResultObj.link[howdoiResultObj.answer.indexOf(answer)] }));
	
		quickPick.onDidChangeSelection(([item]:any) => {
			if (item) {
				editor.edit((edit:any) => {
					edit.replace(editor.selection, userCommand + '\n' + item.link + item.label);	
				});	
			quickPick.dispose();
			}
		});
		quickPick.onDidHide(() => quickPick.dispose());
		quickPick.show();	
	}

	let disposable = vscode.commands.registerCommand('howdoi.extension', () => {
		

		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showInformationMessage('create a file to enable howdoi');
			return;
		}

		const userCommand:string = editor.document.getText(editor.selection);
		const userCommandWithoutComment:string[]|null = modifyCommentedText(userCommand);

		if (userCommandWithoutComment !== null) {
			const textToBeSearched:string = userCommandWithoutComment[0];
			const commentBegin:string  = userCommandWithoutComment[1];
			const commentEnd:string = userCommandWithoutComment[2];

			spawnChild(textToBeSearched, function(howdoiOutput:string) {
				let howdoiResultObj = howdoiResult(editor, howdoiOutput, userCommand, commentBegin, commentEnd);
				quickPicker(editor, howdoiResultObj, userCommand);	
			});
		}
		else {
			vscode.window.showErrorMessage('please use single line comment for howdoi.');
		}
	});
	context.subscriptions.push(disposable);
}

export function deactivate() {}
