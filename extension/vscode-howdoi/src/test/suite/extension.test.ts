import * as vscode from 'vscode'
import * as Mocha from 'mocha'
import * as plugin from '../../extension'
import { assert, expect} from 'chai'
import * as pluginTests from '../../code-editor-integration/src/test/plugin.test'

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')
  pluginTests
})
