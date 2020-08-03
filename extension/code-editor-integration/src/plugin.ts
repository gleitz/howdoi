'use strict'
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
  (howdoiJSON: JSONObj[]): HowdoiObj
}

interface CommentChars {
  frontComment: string,
  endComment: string
}

export function runHowdoi(userCommand: string): void {

  // retrieve single line comment regexes
  const commentChar: CommentChars|null = findCommentChar(userCommand)
    
  if (commentChar !== null) {
    // comment removed from usercommand
    const commandWithoutComment: string = removeCommentChar(userCommand, commentChar)
    
    const callbackFunc: CallBack = function(howdoiJSON: JSONObj[]): HowdoiObj{
      return createHowdoiObj(howdoiJSON, userCommand, commentChar)
    }

    // retrieve answer for howodoi query
    retrieveHowdoiOutput(commandWithoutComment, callbackFunc)
  }   
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
  else if(endMatchRegex){
    endCommentChar = endMatchRegex.join()
    userCommandWithoutComment = {
      frontComment: '',
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
  // spawns an external application in a new process to run the howdoi query and retreives
  // the howdoi query answer 
  const commandWithoutPrefix = removeHowdoiPrefix(command)
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
    
  process.on('close', (code:number) => {
    console.log(`child process exited with code ${code}`)
    return callbackFunc(howdoiJSON)
  })
}

export function removeHowdoiPrefix(command: string): string {
  // removes the prefix `howdoi` from the string
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