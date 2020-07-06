'use strict'
import * as cp from 'child_process'

const HOWDOI_PREFIX = 'howdoi'

interface HowdoiResult {
    question: string
    answer: string[]
    link: string[]  
}

interface CallBack {
  (howdoiOutput: string): void
}

export function main(arg: string): void {
  const userCommand: string = arg
  const userCommandWithoutComment: string[]|null = modifyCommentedText(userCommand)
    
  if (userCommandWithoutComment !== null) {
    const textToBeSearched: string = userCommandWithoutComment[0]
    const frontCommentChar: string  = userCommandWithoutComment[1]
    const endCommentChar: string = userCommandWithoutComment[2]

    
    const callbackFunc: CallBack = function(howdoiOutput: string): void {
      howdoi(howdoiOutput, userCommand, frontCommentChar, endCommentChar)
    }

    spawnChild(textToBeSearched, callbackFunc)
  }   
}

export async function spawnChild(command: string, callbackFunc: CallBack): Promise<void> {
  const commandWithoutPrefix = removeHowdoiPrefix(command)
  const process = await cp.spawn(HOWDOI_PREFIX, [commandWithoutPrefix, '-n 3'])
  let howdoiCommandOutput = ''
  process.stdout.on('data', (data: Buffer) => {
    howdoiCommandOutput += String(data)
  })

  process.stderr.on('data', (data: Buffer) => {
    console.log(`stderr: ${data}`)
  })
    
  process.on('error', (error: Error) => {
    console.log(`error: ${error.message}`)
  })
    
  process.on('close', (code:number) => {
    console.log(`child process exited with code ${code}`)
    return callbackFunc(howdoiCommandOutput)
  })
}

export function removeHowdoiPrefix(command: string): string {
  if (!command.trim().startsWith(HOWDOI_PREFIX)) {
    return command.trim()
  }
  return command.replace(HOWDOI_PREFIX, '').trim()
}

export function modifyCommentedText(userCommand: string): string[]|null {
  /* This function finds the comment regex, removes it from the string and returns an array 
  with the modified string, the beginning comment regex, ending comment regex */
  const frontCommentRegex =  /^[!@#<>/;%*(+=._-]+/
  const endCommentRegex = /[!@#<>/%*+=._-]+$/
  let frontCommentChar: string
  let endCommentChar: string
  let userCommandWithoutComment: string[]
  const initialMatchRegex: RegExpMatchArray | null = userCommand.match(frontCommentRegex)
  const endMatchRegex: RegExpMatchArray | null = userCommand.match(endCommentRegex)
        
  if (initialMatchRegex && endMatchRegex){
    frontCommentChar = initialMatchRegex.join()
    endCommentChar = endMatchRegex.join()
    userCommand = userCommand.replace(frontCommentRegex, '')
    userCommand = userCommand.replace(endCommentRegex, '')
    userCommandWithoutComment = [userCommand.trim(), frontCommentChar, endCommentChar]
    return userCommandWithoutComment
  }
  else if(endMatchRegex){
    endCommentChar = endMatchRegex.join()
    userCommand = userCommand.replace(endCommentRegex, '')
    userCommandWithoutComment = [userCommand.trim(), '', endCommentChar]
    return userCommandWithoutComment
  }
  else if(initialMatchRegex){
    frontCommentChar = initialMatchRegex.join()
    userCommand= userCommand.replace(frontCommentRegex, '')
    userCommandWithoutComment = [userCommand.trim(), frontCommentChar, '']
    return userCommandWithoutComment
  }
  else {
    return null
  }
}

function organizeHowdoiOutput(howdoiOutput: string, frontCommentChar: string, endCommentChar: string): string[][] {
  /* Creates an array from the howdoiOutput string in which each element 
  is one of three answers from the usersCommand */
  const delim = '\n'+'================================================================================' + '\n' + '\n'
  const howdoiAnswersArr = howdoiOutput.split(delim)
  /* Creates a 2D array from howdoiAnswersArr in which each element is an array which denotes
  one of three answers from the usersCommand, and the elements in that array are link and answer */
  const newHowdoiAnswersArr: string[][] = howdoiAnswersArr.map((elem) => elem.split(' ★'))
  //  The comment Regex is added to the link string
  for (let i = 0; i < newHowdoiAnswersArr.length; i++) {
    newHowdoiAnswersArr[i][0] = frontCommentChar + newHowdoiAnswersArr[i][0] + endCommentChar
  }

  return newHowdoiAnswersArr
}

export function createHowdoiResult(howdoiResultArr: string[][], userCommand: string): HowdoiResult {
  const howdoiResultObj: HowdoiResult = {question: userCommand, answer: [], link: []}

  for (let i = 0; i < howdoiResultArr.length; i++) {
    howdoiResultObj.link.push(howdoiResultArr[i][0])
    howdoiResultObj.answer.push(howdoiResultArr[i][1])
  }

  return howdoiResultObj
}

function howdoi(output: string, userCommand: string, frontCommentChar: string, endCommentChar: string): HowdoiResult {
  const organizedHowdoiArr: string[][] = organizeHowdoiOutput(output, frontCommentChar, endCommentChar)
  const howdoiResultObj: HowdoiResult = createHowdoiResult(organizedHowdoiArr, userCommand)
  return howdoiResultObj
}