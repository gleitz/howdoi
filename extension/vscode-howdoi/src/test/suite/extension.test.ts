import * as assert from 'assert'
import * as vscode from 'vscode'
import * as Mocha from 'mocha'
import * as myExtension from '../../extension'

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')
  suite('removeHowdoiPrefix test', () => {
    test('test 1', function () {
      assert.equal(myExtension.removeHowdoiPrefix('howdoi query'), 'query')
    })
    test('test 2', function () {
      assert.equal(myExtension.removeHowdoiPrefix(' howdoi query '), 'query')
    })
    test('test 3', function () {
      assert.equal(myExtension.removeHowdoiPrefix('query'), 'query')
    })
    test('test 4', function () {
      assert.equal(myExtension.removeHowdoiPrefix(' query '), 'query')
    })

  })
  suite('modifyCommentedText test', () => {

    test('test 1', function () {
      // null
      assert.equal(myExtension.modifyCommentedText('howdoi query'), null)
    })
    test('test 2', function () {
      // JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
      assert.deepEqual(myExtension.modifyCommentedText('// howdoi query'), ['howdoi query', '//', ''])
      assert.deepEqual(myExtension.modifyCommentedText('//howdoi query'), ['howdoi query', '//', ''])
    })
    test('test 3', function () {
      // Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
      assert.deepEqual(myExtension.modifyCommentedText('# howdoi query'), ['howdoi query', '#', ''] )
      assert.deepEqual(myExtension.modifyCommentedText('#howdoi query'), ['howdoi query', '#', ''] )
    })
    test('test 4', function () {
      // C++, CSS single line comment 
      assert.deepEqual(myExtension.modifyCommentedText('/* howdoi query */'), ['howdoi query', '/*', '*/'] )
    })
    test('test 5', function () {
      // HTML, PHP, Markdown, Vue single line comment
      assert.deepEqual(myExtension.modifyCommentedText('<!-- howdoi query -->'), ['howdoi query', '<!--', '-->'] )
    })
    test('test 6', function () {
      // SQL, Haskell single line comment
      assert.deepEqual(myExtension.modifyCommentedText('-- howdoi query'), ['howdoi query', '--', ''] )
    })
    test('test 7', function () {
      // LaTex single line comment
      assert.deepEqual(myExtension.modifyCommentedText('% howdoi query'), ['howdoi query', '%', ''] )
    })
    test('test 8', function () {
      // clojure single line comment
      assert.deepEqual(myExtension.modifyCommentedText('; howdoi query'), ['howdoi query', ';', ''] ) 
    }) 
  })
})
