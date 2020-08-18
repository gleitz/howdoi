'use strict'
import {CommentChars} from './plugin_interfaces'

export function findCommentChar(userCommand: string): CommentChars { 
  /* This function finds the comment regex, removes it from the string and returns a
    CommentChars interface with the beginning comment regex and ending comment regex or returns
    null if there is no comment regex/an invalid comment regex */
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

export function findNumFlagVal(userCommand: string): number { 
  /* This function finds the numFlag value within the userCommand and returns the value */
  const numFlag =  '-n'
  const defaultNumFlag = 3
  const index = userCommand.indexOf(numFlag)
   
  if (index === -1){
    return defaultNumFlag
  }

  const userNumFlag = Number(userCommand.slice(index).replace(numFlag, '').trim())
  if (isNaN(userNumFlag) || (userNumFlag === 0)) {
    throw new RangeError('Invalid num flag value')
  }
  return userNumFlag
}
