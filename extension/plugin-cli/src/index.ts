#!/usr/bin/env node

import yargs from 'yargs'
import * as wrapper from './wrapper'
import { HowdoiObj } from './code-editor-integration/src/plugin_interfaces'

export async function parseArgs(): Promise<HowdoiObj|Error> {
  const args = yargs.options({'query': { 
    type: 'string', 
    demandOption: true, 
    alias: 'q',
    describe: 'howdoi query encapsulated in single line comment',
  }}).help().argv

  const result = await wrapper.howdoiWrapper(args['query'])
  return result
}

