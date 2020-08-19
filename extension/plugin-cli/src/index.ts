#!/usr/bin/env node

import yargs from 'yargs'
import * as wrapper from './wrapper'

export async function parseArgs(): Promise<void> {
  const args = yargs.options({'query': { 
    type: 'string', 
    demandOption: true, 
    alias: 'q',
    describe: 'howdoi query encapsulated in single line comment',
  }}).help().argv

  const result = await wrapper.howdoiWrapper(args['query'])
  console.log(result)
}

