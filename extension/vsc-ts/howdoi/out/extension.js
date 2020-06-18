"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const cp = require("child_process");
function activate(context) {
    function spawnChild(command, cb) {
        return __awaiter(this, void 0, void 0, function* () {
            const updatedCommand = howdoiPrefix(command);
            const process = yield cp.spawn("howdoi", [updatedCommand, '-n 3']);
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
        });
    }
    function spliceArr(obj, commentBegin, commentEnd) {
        let dataString = String(obj);
        let lines = dataString.split('\n' + '================================================================================' + '\n' + '\n');
        let newArr = lines.map((elem) => elem.split(' ★'));
        for (let i = 0; i < newArr.length; i++) {
            newArr[i][0] = commentBegin + newArr[i][0] + commentEnd;
        }
        return newArr;
    }
    function helperFunc(editor, myArr, userTxt, commentBegin, commentEnd) {
        const newResult = spliceArr(myArr, commentBegin, commentEnd);
        const quickPick = vscode.window.createQuickPick();
        quickPick.items = newResult.map((x) => ({ label: x[1], link: x[0] }));
        quickPick.onDidChangeSelection(([item]) => {
            if (item) {
                editor.edit((edit) => {
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
            const newCommand = command.replace(prefix, '');
            return newCommand;
        }
        else {
            return command;
        }
    }
    function modifyCommentedText(textToBeModified) {
        const regexBegins = /^[!@#<>/\$%\^\&*\)\(+=._-]+/;
        const regexEnds = /[!@#<>/\$%\^\&*\)\(+=._-]+$/;
        let commentBegin;
        let commentEnd;
        let result;
        if (textToBeModified.match(regexBegins) && textToBeModified.match(regexEnds)) {
            commentBegin = textToBeModified.match(regexBegins).join();
            commentEnd = textToBeModified.match(regexEnds).join();
            textToBeModified = textToBeModified.replace(regexBegins, '');
            textToBeModified = textToBeModified.replace(regexEnds, '');
            result = [textToBeModified, commentBegin, commentEnd];
            return result;
        }
        else if (textToBeModified.match(regexEnds)) {
            commentEnd = textToBeModified.match(regexEnds).join();
            textToBeModified = textToBeModified.replace(regexEnds, '');
            result = [textToBeModified, '', commentEnd];
            return result;
        }
        else if (textToBeModified.match(regexBegins)) {
            commentBegin = textToBeModified.match(regexBegins).join();
            textToBeModified = textToBeModified.replace(regexBegins, '');
            result = [textToBeModified, commentBegin, ''];
            return result;
        }
        else {
            return null;
        }
    }
    let disposable = vscode.commands.registerCommand('howdoi.extension', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('create a file to enable howdoi');
            return;
        }
        const textToBeModified = editor.document.getText(editor.selection);
        let txtArr = modifyCommentedText(textToBeModified);
        if (txtArr != null) {
            const textToBeSearched = txtArr[0];
            const commentBegin = txtArr[1];
            const commentEnd = txtArr[2];
            spawnChild(textToBeSearched, function (myArr) {
                helperFunc(editor, myArr, textToBeModified, commentBegin, commentEnd);
            });
        }
        else {
            vscode.window.showErrorMessage('please use single line comment for howdoi.');
        }
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map