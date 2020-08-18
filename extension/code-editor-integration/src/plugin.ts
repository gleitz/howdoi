'use strict'
import * as cp from 'child_process'
import {once} from 'events'
import {HOWDOI_PREFIX, HowdoiObj, JSONObj, CommentChars} from './plugin_interfaces'
import * as removeRegex from './remove_regexes'
import * as findAttr from './find_attributes'
import * as createAttr from './create_attributes'

export async function retrieveHowdoiOutput(command: string, numFlagVal: number): Promise<JSONObj[]> {
  /* This function spawns an external application in a new process to run the howdoi query and returns
  the howdoi query answer formatted as a JSONObj[] */
  const numFlag: string = '-n' + String(numFlagVal)
  const process = cp.spawn(HOWDOI_PREFIX, [command, numFlag, '-j'])
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
  const endProcess = await once(process, 'close')
  try {
    endProcess
  } catch(e) {
    throw Error('Invalid json object or no json object returned')
  }
  return howdoiJSON
}

export async function runHowdoi(userCommand: string): Promise<HowdoiObj> {
  /* This functions modifies the users command while checking for errors
  and formats the howdoi query answer into a HowdoiObj*/
  
  let commentChar: CommentChars
  // check if query is enclosed by a single line comment and return commentChar
  try {
    // retrieve single line comment and store in CommentChars obj
    commentChar = findAttr.findCommentChar(userCommand)
  }catch (e) {
    throw new ReferenceError('Invalid line comment. Please use single line comment for howdoi.')
  }
  
  const commandWithoutComment: string = removeRegex.removeCommentChar(userCommand, commentChar)
  let commandWithoutPrefix: string

  // check if howdoi prefix is present and remove it
  try {
    commandWithoutPrefix = removeRegex.removeHowdoiPrefix(commandWithoutComment)
  }catch (e) {
    throw new SyntaxError('Place "howdoi" in front of query')
  }

  let numFlagVal: number
  // check if -n flag is present and remove it
  try {
    numFlagVal = findAttr.findNumFlagVal(commandWithoutPrefix)
  }catch (e) {
    throw new RangeError('Invalid num flag value')
  }

  const commandWithoutFlag = removeRegex.removeNumFlag(commandWithoutPrefix)

  let parsedJson: JSONObj[] 
  // check if howdoi output is valid and save the JSON Obj
  try {
    parsedJson = await retrieveHowdoiOutput(commandWithoutFlag, numFlagVal)
  }catch (e) {
    throw new Error('Invalid json object or no json object returned')
  }
  
  let howdoiResultObj = createAttr.createHowdoiObj(parsedJson, userCommand, commentChar)
  howdoiResultObj = removeRegex.removeInlineRegex(howdoiResultObj)
  return howdoiResultObj
}
