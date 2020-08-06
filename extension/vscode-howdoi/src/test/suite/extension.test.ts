import * as vscode from 'vscode'
import { assert, expect} from 'chai'
import * as pluginTests from '../../code-editor-integration/src/test/plugin.test'

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')
  pluginTests
})
