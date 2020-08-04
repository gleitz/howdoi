'use strict'
import * as cp from 'child_process'
import {once} from 'events'

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

interface CommentChars {
  frontComment: string,
  endComment: string
}

export async function runHowdoi(userCommand: string): Promise<HowdoiObj> {
  
  let commentChar: CommentChars
  // check if query is enclosed by a single line comment and return commentChar
  try {
    commentChar = findCommentChar(userCommand)
  }catch (e) {
    throw new ReferenceError('Invalid line comment. Please use single line comment for howdoi.')
  }
  
  const commandWithoutComment: string = removeCommentChar(userCommand, commentChar)
  let commandWithoutPrefix: string

  // check if howdoi prefix is present and remove it
  try {
    commandWithoutPrefix = removeHowdoiPrefix(commandWithoutComment)
  }catch (e) {
    throw new SyntaxError('Place "howdoi" in front of query')
  }

  let parsedJson: JSONObj[] 
  // check if howdoi output is valid and save the JSON Obj
  try {
    parsedJson = await retrieveHowdoiOutput(commandWithoutPrefix)
  }catch (e) {
    throw new Error('Invalid json object or no json object returned')
  }
  
  const howdoiResultObj = createHowdoiObj(parsedJson, userCommand, commentChar)
  return howdoiResultObj
}

export function findCommentChar(userCommand: string): CommentChars { 
  /* This function finds the comment regex, removes it from the string and returns a
   CommentChars interface with the beginning comment regex and ending comment regex or returns
   null if there is no comment regex or an invalid comment regex*/
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
    throw Error('Invalid line comment. Please use single line comment for howdoi.')
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

export async function retrieveHowdoiOutput(command: string): Promise<JSONObj[]> {
  // spawns an external application in a new process to run the howdoi query and retreives
  // the howdoi query answer 
  const process = cp.spawn(HOWDOI_PREFIX, [command, '-n3', '-j'])
  let howdoiJSON: JSONObj[] = [{ answer: '', link: '', position: ''}]
  
  process.stdout.on('data', (data: string) => {
    howdoiJSON = JSON.parse(data)
  })

  process.stderr.on('dataErr', (dataErr: Buffer) => {
    console.log(`stderr: ${dataErr}`)
  })
    
  process.on('error', (error: Error) => {
    console.log(`error: ${error.message}`)
  })
    
  process.on('close', (code: number) => {
    console.log(`child process exited with code ${code}`)
  }) 
  
  // Wait for the child process to exit
  let endProcess 
  try {
    endProcess = await once(process, 'close')
  } catch(e) {
    throw Error('Invalid json object or no json object returned')
  }
  return howdoiJSON
}

export function removeHowdoiPrefix(command: string): string {
  // removes the prefix `howdoi` from the string
  if (!command.trim().startsWith(HOWDOI_PREFIX)) {
    throw Error('Place "howdoi" in front of query')
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