import * as assert from 'assert'
import * as vscode from 'vscode'
import * as myExtension from '../../extension'

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')
  test('removeHowdoiPrefix test', () => {
    assert.equal(myExtension.removeHowdoiPrefix('howdoi query'), 'query')
    assert.equal(myExtension.removeHowdoiPrefix(' howdoi query '), 'query')
    assert.equal(myExtension.removeHowdoiPrefix('query'), 'query')
    assert.equal(myExtension.removeHowdoiPrefix(' query '), 'query')
  })
  test('modifyCommentedText test', () => {
    // null
    assert.equal(myExtension.modifyCommentedText('howdoi query'), null)
    // JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
    assert.deepEqual(myExtension.modifyCommentedText('// howdoi query'), ['howdoi query', '//', ''])
    assert.deepEqual(myExtension.modifyCommentedText('//howdoi query'), ['howdoi query', '//', ''])
    // Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
    assert.deepEqual(myExtension.modifyCommentedText('# howdoi query'), ['howdoi query', '#', ''] )
    assert.deepEqual(myExtension.modifyCommentedText('#howdoi query'), ['howdoi query', '#', ''] )
    // C++, CSS single line comment 
    assert.deepEqual(myExtension.modifyCommentedText('/* howdoi query */'), ['howdoi query', '/*', '*/'] )
    // HTML, PHP, Markdown, Vue single line comment
    assert.deepEqual(myExtension.modifyCommentedText('<!-- howdoi query -->'), ['howdoi query', '<!--', '-->'] )
    // SQL, Haskell single line comment
    assert.deepEqual(myExtension.modifyCommentedText('-- howdoi query'), ['howdoi query', '--', ''] )
    // LaTex single line comment
    assert.deepEqual(myExtension.modifyCommentedText('% howdoi query'), ['howdoi query', '%', ''] )
    // clojure single line comment
    assert.deepEqual(myExtension.modifyCommentedText('; howdoi query'), ['howdoi query', ';', ''] ) 
  })
})
