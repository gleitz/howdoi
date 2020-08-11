'use strict'
import {HOWDOI_PREFIX, HowdoiObj, CommentChars} from './plugin_interfaces'

export function removeCommentChar(userCommand: string, commentChar: CommentChars): string {
  /* This function removes the single line comment regex from the userCommand and returns it*/
  const frontCommentChar: string = commentChar.frontComment
  const endCommentChar: string = commentChar.endComment

  if (!userCommand.includes(endCommentChar)) {
    return userCommand.replace(frontCommentChar, '').trim()
  }
  userCommand = userCommand.replace(frontCommentChar, '')
  return userCommand.replace(endCommentChar, '').trim()
}

export function removeHowdoiPrefix(command: string): string {
  // removes the prefix `howdoi` from the string
  if (!command.trim().startsWith(HOWDOI_PREFIX)) {
    throw Error('Place "howdoi" in front of query')
  }
  return command.replace(HOWDOI_PREFIX, '').trim()
}

export function removeNumFlag(userCommand: string): string { 
  /* This function removes the numFlag value within the userCommand and returns userCommand */
  const numFlag =  '-n'
  const index = userCommand.indexOf(numFlag)
   
  if (index === -1){
    return userCommand
  }
  const commandWithoutNumFlag = userCommand.slice(0, index).trim()
  return commandWithoutNumFlag
}

export function removeInlineRegex(howdoiResultObj: HowdoiObj): HowdoiObj {
  /* This function returns a HowdoiObj that has the arrow and dot regexes removed
  from the answer array to display inline code more cleanly */

  const arrowRegex = /[>->->]{3}/g
  const dotRegex = /[.-.-.]{3}/g

  for (let i = 0; i < howdoiResultObj.answer.length; i++) {
    if (howdoiResultObj.answer[i].match(arrowRegex)) {
      howdoiResultObj.answer[i] = howdoiResultObj.answer[i].replace(arrowRegex, '').trim()
    }
    if (howdoiResultObj.answer[i].match(dotRegex)) {
      howdoiResultObj.answer[i] = howdoiResultObj.answer[i].replace(dotRegex, '').trim()
    }
  }
  return howdoiResultObj
}
