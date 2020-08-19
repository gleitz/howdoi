#!/usr/bin/env node
import mod = require('esm') 
import * as plugin_cli from './index'

mod(module/*, options*/)
plugin_cli.parseArgs()
