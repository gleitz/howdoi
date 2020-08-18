export const HOWDOI_PREFIX = 'howdoi'

export interface HowdoiObj {
  question: string
  answer: string[]
  link: string[]  
}

export interface JSONObj {
  answer: string
  link: string
  position: string
}

export interface CommentChars {
  frontComment: string
  endComment: string
}
