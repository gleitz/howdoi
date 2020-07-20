import * as assert from 'assert'
import * as vscode from 'vscode'
import * as Mocha from 'mocha'
import * as myExt from '../../extension'

suite('Extension Test Suite', () => {
  vscode.window.showInformationMessage('Start all tests.')
  
  suite('Find comment regex in string -> #findCommentChar', function () {
    test('String w/o comment regex', function () {
      // null example
      assert.equal(myExt.findCommentChar('howdoi query'), null)
    })
    test('Comment regex test: //', function () {
      // JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
      assert.deepEqual(myExt.findCommentChar('// howdoi query'), { frontComment: '//', endComment: '' })
      // W/o whitespace after comment regex
      assert.deepEqual(myExt.findCommentChar('//howdoi query'), { frontComment: '//', endComment: '' })
    })
    test('Comment regex test: #', function () {
      // Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
      assert.deepEqual(myExt.findCommentChar('# howdoi query'), { frontComment: '#', endComment: '' })
      // W/o whitespace 
      assert.deepEqual(myExt.findCommentChar('#howdoi query'), { frontComment: '#', endComment: '' })
    })
    test('Comment regex test: /* */', function () {
      // C++, CSS single line comment 
      assert.deepEqual(myExt.findCommentChar('/* howdoi query */'), { frontComment: '/*', endComment: '*/' })
      // W/o whitespace
      assert.deepEqual(myExt.findCommentChar('/*howdoi query*/'), { frontComment: '/*', endComment: '*/' })
    })
    test('Comment regex test: <!-- -->', function () {
      // HTML, PHP, Markdown, Vue single line comment
      assert.deepEqual(myExt.findCommentChar('<!-- howdoi query -->'), { frontComment: '<!--', endComment: '-->' })
      // W/o whitespace 
      assert.deepEqual(myExt.findCommentChar('<!--howdoi query-->'), { frontComment: '<!--', endComment: '-->' })
    })
    test('Comment regex test: --', function () {
      // SQL, Haskell single line comment
      assert.deepEqual(myExt.findCommentChar('-- howdoi query'), { frontComment: '--', endComment: '' })
      // W/o whitespace 
      assert.deepEqual(myExt.findCommentChar('--howdoi query'), { frontComment: '--', endComment: '' })
    })
    test('Comment regex test: %', function () {
      // LaTex single line comment
      assert.deepEqual(myExt.findCommentChar('% howdoi query'), { frontComment: '%', endComment: '' })
      // W/o whitespace
      assert.deepEqual(myExt.findCommentChar('%howdoi query'), { frontComment: '%', endComment: '' })
    })
    test('Comment regex test: ;', function () {
      // clojure single line comment
      assert.deepEqual(myExt.findCommentChar('; howdoi query'), { frontComment: ';', endComment: '' })
      // W/o whitespace
      assert.deepEqual(myExt.findCommentChar(';howdoi query'), { frontComment: ';', endComment: '' })
    })
  })
  
  suite('Removal of comment character from user command -> #removeCommentChar', function () {
    test('Removal of comment char: //', function () {
      const commentChar = {frontComment: '//', endComment: ''}
      // With space
      assert.deepEqual(myExt.removeCommentChar('// howdoi query', commentChar), 'howdoi query')
      // W/o whitespace after comment regex
      assert.deepEqual(myExt.removeCommentChar('//howdoi query', commentChar), 'howdoi query')
    })
    test('Removal of comment char: #', function () {
      const commentChar = { frontComment: '#', endComment: '' }
      // With space
      assert.deepEqual(myExt.removeCommentChar('# howdoi query', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(myExt.removeCommentChar('#howdoi query', commentChar), 'howdoi query')
    })
    test('Removal of comment char: /* */', function () {
      const commentChar = { frontComment: '/*', endComment: '*/' }
      // With space
      assert.deepEqual(myExt.removeCommentChar('/* howdoi query */', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(myExt.removeCommentChar('/*howdoi query*/', commentChar), 'howdoi query')
    })
    test('Removal of comment char: <!-- -->', function () {
      const commentChar = { frontComment: '<!--', endComment: '-->' }
      // With space
      assert.deepEqual(myExt.removeCommentChar('<!-- howdoi query -->', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(myExt.removeCommentChar('<!--howdoi query-->', commentChar), 'howdoi query')
    })
    test('Removal of comment char: --', function () {
      const commentChar = { frontComment: '--', endComment: '' }
      // With space
      assert.deepEqual(myExt.removeCommentChar('-- howdoi query', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(myExt.removeCommentChar('--howdoi query', commentChar), 'howdoi query')
    })
    test('Removal of comment char: %', function () {
      const commentChar = { frontComment: '%', endComment: '' }
      // LaTex single line comment
      assert.deepEqual(myExt.removeCommentChar('% howdoi query', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(myExt.removeCommentChar('%howdoi query', commentChar), 'howdoi query')
    })
    test('Removal of comment char: ;', function () {
      const commentChar = { frontComment: ';', endComment: '' }
      // clojure single line comment
      assert.deepEqual(myExt.removeCommentChar('; howdoi query', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(myExt.removeCommentChar(';howdoi query', commentChar), 'howdoi query')
    })
  })

  suite('Removal of howdoi prefix test -> #removeHowdoiPrefix', function () {
    test('Normal Query', function () {
      // Normal Query
      assert.equal(myExt.removeHowdoiPrefix('howdoi query'), 'query')
    })
    test('Query with whitespace', function () {
      // Query with whitespace
      assert.equal(myExt.removeHowdoiPrefix(' howdoi query '), 'query')
    })
    test('Query without howdoi prefix', function () {
      // Query without howdoi prefix
      assert.equal(myExt.removeHowdoiPrefix('query'), 'query')
    })
    test('Query without howdoi prefix and whitespace', function () {
      // Query without howdoi prefix and whitespace
      assert.equal(myExt.removeHowdoiPrefix(' query '), 'query')
    })
  })

  suite('Add comment character to a string -> #addComment', function () {
    test('Add comment with front/back chars to string', function () {
      // Add comment: '/*' '*/'
      const commentChar1 = { frontComment: '/*', endComment: '*/' }
      assert.equal(myExt.addComment('howdoi query', commentChar1), '/* howdoi query */')
      // Add comment with '<!--' '-->' 
      const commentChar2 = { frontComment: '<!--', endComment: '-->' }
      assert.equal(myExt.addComment('howdoi query', commentChar2), '<!-- howdoi query -->')
    })
    test('Add comment with front char to string', function () {
      // Add comment: #
      const commentChar1 = { frontComment: '#', endComment: '' }
      assert.equal(myExt.addComment('howdoi query', commentChar1), '# howdoi query')
      // Add comment: ;
      const commentChar2 = { frontComment: ';', endComment: '' }
      assert.equal(myExt.addComment('howdoi query', commentChar2), '; howdoi query')
      // Add comment: %
      const commentChar3 = { frontComment: '%', endComment: '' }
      // LaTex single line comment
      assert.equal(myExt.addComment('howdoi query', commentChar3), '% howdoi query')
      // Add coment: -- 
      const commentChar4 = { frontComment: '--', endComment: '' }
      assert.equal(myExt.addComment('howdoi query', commentChar4), '-- howdoi query')
      // Add comment: //
      const commentChar5 = { frontComment: '//', endComment: '' }
      assert.equal(myExt.addComment('howdoi query', commentChar5), '// howdoi query')
    })
  })
})
