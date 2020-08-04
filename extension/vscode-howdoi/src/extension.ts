import * as vscode from 'vscode'
import * as plugin from './code-editor-integration/src/plugin'


export function activate(context: vscode.ExtensionContext) {

  let disposable = vscode.commands.registerCommand('howdoi.extension', async () => {

    const editor = vscode.window.activeTextEditor
    if (!editor) {
      vscode.window.showInformationMessage('create a file to enable howdoi')
      return
    }

    const userCommand: string = editor.document.getText(editor.selection).trim()
    let howdoiResultObj 
  
    try {
      howdoiResultObj = await plugin.runHowdoi(userCommand)
    } catch (e) {
      if (e instanceof ReferenceError) {
        vscode.window.showInformationMessage('Invalid line comment. Please use single line comment for howdoi.')
      } else if (e instanceof SyntaxError) {
        vscode.window.showInformationMessage('Place "howdoi" in front of query')
      }else if (e instanceof Error) {
        vscode.window.showInformationMessage('Could not find response for query')
      } else {
        vscode.window.showInformationMessage('Error. Try again')
      }
    } 

    quickPicker(editor, howdoiResultObj, userCommand)
  
 
  })
  context.subscriptions.push(disposable)
}

function quickPicker(editor: any, howdoiResultObj: any, userCommand: string): void {
  const quickPick = vscode.window.createQuickPick()

  quickPick.items = howdoiResultObj.answer.map((answer: string) => (
    {label: answer, link: howdoiResultObj.link[howdoiResultObj.answer.indexOf(answer)] }))

  quickPick.onDidChangeSelection(([item]: any) => {
    if (item) {
      editor.edit((edit: any) => {
        edit.replace(editor.selection, userCommand + '\n' + item.link + '\n' + item.label)
      })
	  quickPick.dispose()
    }
  })
  quickPick.onDidHide(() => quickPick.dispose())
  quickPick.show()
}

export function deactivate() {}
