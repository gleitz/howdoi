import * as plugin from './code-editor-integration/src/plugin'

interface HowdoiObj {
  question: string
  answer: string[]
  link: string[]  
}

export async function howdoiWrapper(userArgs: string): Promise<HowdoiObj|Error> {
  let howdoiResultObj 

  try {
    howdoiResultObj = await plugin.runHowdoi(userArgs)
  } catch (e) {
    if (e instanceof ReferenceError) {
      console.log('Invalid line comment. Please use single line comment for howdoi.')
      return e
    } else if (e instanceof SyntaxError) {
      console.log('Place "howdoi" in front of query')
      return e
    }else if (e instanceof Error) {
      console.log('Could not find response for query')
      return e
    } else {
      console.log('Error. Try again')
      return e
    }
  }
  return howdoiResultObj
}