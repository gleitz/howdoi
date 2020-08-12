'use strict'
import {HowdoiObj, JSONObj, CommentChars} from './plugin_interfaces'

export function createComment(command: string, commentChar: CommentChars): string {
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

export function createHowdoiObj(parsedJson: JSONObj[], userCommand: string, commentChar: CommentChars): HowdoiObj {
  // creates a HowdoiObj interface 
  const howdoiObj: HowdoiObj = {question: userCommand, answer: [], link: []}

  for (let i = 0; i < parsedJson.length; i++) {
    if (parsedJson[i].answer.trim() === 'end=\'\'') { 
      break
    }
    howdoiObj.answer.push(parsedJson[i].answer.trim())
    howdoiObj.link.push(createComment(parsedJson[i].link.trim(), commentChar))
  }
  return howdoiObj
}
