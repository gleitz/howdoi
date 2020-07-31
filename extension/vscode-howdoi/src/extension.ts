import * as vscode from 'vscode'
import * as cp from 'child_process'

const HOWDOI_PREFIX = 'howdoi'

interface HowdoiObj {
    question: string
    answer: string[]
    link: string[]
}

interface JSONObj {
  answer: string,
  link: string,
  position: string
}

interface CallBack {
  (howdoiOutput: JSONObj[]): void
}

interface CommentChars {
  frontComment: string,
  endComment: string
}

export function activate(context: vscode.ExtensionContext) {

  let disposable = vscode.commands.registerCommand('howdoi.extension', () => {

    const editor = vscode.window.activeTextEditor
    if (!editor) {
      vscode.window.showInformationMessage('create a file to enable howdoi')
      return
    }

    const userCommand: string = editor.document.getText(editor.selection).trim()
    
    // retrieve single line comment regexes
    const commentChar: CommentChars|null = findCommentChar(userCommand)

    if (commentChar !== null) {
      // comment removed from usercommand
      const commandWithoutComment: string = removeCommentChar(userCommand, commentChar)

      // create callback function
      const callbackFunc: CallBack = function(howdoiJSON: JSONObj[]): void{
        let howdoiResultObj = createHowdoiObj(howdoiJSON, userCommand, commentChar)
        
        quickPicker(editor, howdoiResultObj, userCommand)
      }

      retrieveHowdoiOutput(commandWithoutComment, callbackFunc)
    }
    else {
      vscode.window.showErrorMessage('please use single line comment for howdoi.')
    }
  })
  context.subscriptions.push(disposable)
}

export function findCommentChar(userCommand: string): CommentChars|null { 
  /* This function finds the comment regex, removes it from the string and returns a
   CommentChars interface with the beginning comment regex and ending comment regex */
  const frontCommentRegex =  /^[!@#<>/;%*(+=._-]+/
  const endCommentRegex = /[!@#<>/%*+=._-]+$/
  let frontCommentChar: string
  let endCommentChar: string
  let userCommandWithoutComment: CommentChars
  const initialMatchRegex: RegExpMatchArray | null = userCommand.match(frontCommentRegex)
  const endMatchRegex: RegExpMatchArray | null = userCommand.match(endCommentRegex)
        
  if (initialMatchRegex && endMatchRegex){
    frontCommentChar = initialMatchRegex.join()
    endCommentChar = endMatchRegex.join()
    userCommandWithoutComment = {
      frontComment: frontCommentChar,
      endComment: endCommentChar
    }
    return userCommandWithoutComment
  }
  else if(initialMatchRegex){
    frontCommentChar = initialMatchRegex.join()
    userCommandWithoutComment = {
      frontComment: frontCommentChar,
      endComment: ''
    }
    return userCommandWithoutComment
  }
  else {
    return null
  }
}

export function removeCommentChar(userCommand: string, commentChar: CommentChars): string {
  // removes single line comment regex from the user command
  const frontCommentChar: string = commentChar.frontComment
  const endCommentChar: string = commentChar.endComment

  if (!userCommand.includes(endCommentChar)) {
    return userCommand.replace(frontCommentChar, '').trim()
  }
  userCommand = userCommand.replace(frontCommentChar, '')
  return userCommand.replace(endCommentChar, '').trim()
}

export async function retrieveHowdoiOutput(command: string, callbackFunc: CallBack): Promise<void> {
  
  const commandWithoutPrefix = removeHowdoiPrefix(command)
  // HOWDOI_PREFIX, [commandWithoutPrefix, '-n3']
  const process = cp.spawn(HOWDOI_PREFIX, [commandWithoutPrefix, '-n3', '-j'])
  
  let howdoiJSON: JSONObj[]

  process.stdout.on('data', (data: string) => {
    howdoiJSON = JSON.parse(data)
  })

  process.stderr.on('data', (data: Buffer) => {
    console.log(`stderr: ${data}`)
  })

  process.on('error', (error: Error) => {
    console.log(`error: ${error.message}`)
  })

  process.on('close', (code: number) => {
    console.log(`child process exited with code ${code}`)
    return callbackFunc(howdoiJSON)
  })
}

export function removeHowdoiPrefix(command: string): string {
  if (!command.trim().startsWith(HOWDOI_PREFIX)) {
    return command.trim()
  }
  return command.replace(HOWDOI_PREFIX, '').trim()
}

export function createHowdoiObj(parsedJson: JSONObj[], userCommand: string, commentChar: CommentChars): HowdoiObj {
  // creates a HowdoiObj interface 
  const howdoiObj: HowdoiObj = {question: userCommand, answer: [], link: []}

  for (let i = 0; i < parsedJson.length; i++) {
    howdoiObj.answer.push(parsedJson[i].answer.trim())
    howdoiObj.link.push(addComment(parsedJson[i].link.trim(), commentChar))
  }
  return howdoiObj
}

export function addComment(command: string, commentChar: CommentChars): string {
  // adds single line comment to string provided
  const frontCommentChar: string = commentChar.frontComment
  const endCommentChar: string = commentChar.endComment
  if (frontCommentChar && (endCommentChar !== '')) {
    const commentedCommand: string = frontCommentChar + ' ' + command + ' ' + endCommentChar
    return commentedCommand
  }
  const commentedCommand: string = frontCommentChar + ' ' + command
  return commentedCommand
}

function quickPicker(editor: any, howdoiResultObj: HowdoiObj, userCommand: string): void {
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
