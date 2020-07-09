import { assert} from 'chai'
import 'mocha'
import * as plugin from '../plugin'


describe('Plugin Tests', function () {

  // describe('main-> #runhowdoi', function () {
  //   it('', function () {
  //   })
  // })
  
  describe('Find comment regex in string -> #findCommentChar', function () {
    it('String w/o comment regex', function () {
      // null example
      assert.equal(plugin.findCommentChar('howdoi query'), null)
    })
    it('Comment regex test: //', function () {
      // JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
      assert.deepEqual(plugin.findCommentChar('// howdoi query'), { frontComment: '//', endComment: '' })
      // W/o whitespace after comment regex
      assert.deepEqual(plugin.findCommentChar('//howdoi query'), { frontComment: '//', endComment: '' })
    })
    it('Comment regex test: #', function () {
      // Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
      assert.deepEqual(plugin.findCommentChar('# howdoi query'), { frontComment: '#', endComment: '' })
      // W/o whitespace 
      assert.deepEqual(plugin.findCommentChar('#howdoi query'), { frontComment: '#', endComment: '' })
    })
    it('Comment regex test: /* */', function () {
      // C++, CSS single line comment 
      assert.deepEqual(plugin.findCommentChar('/* howdoi query */'), { frontComment: '/*', endComment: '*/' })
      // W/o whitespace
      assert.deepEqual(plugin.findCommentChar('/*howdoi query*/'), { frontComment: '/*', endComment: '*/' })
    })
    it('Comment regex test: <!-- -->', function () {
      // HTML, PHP, Markdown, Vue single line comment
      assert.deepEqual(plugin.findCommentChar('<!-- howdoi query -->'), { frontComment: '<!--', endComment: '-->' })
      // W/o whitespace 
      assert.deepEqual(plugin.findCommentChar('<!--howdoi query-->'), { frontComment: '<!--', endComment: '-->' })
    })
    it('Comment regex test: --', function () {
      // SQL, Haskell single line comment
      assert.deepEqual(plugin.findCommentChar('-- howdoi query'), { frontComment: '--', endComment: '' })
      // W/o whitespace 
      assert.deepEqual(plugin.findCommentChar('--howdoi query'), { frontComment: '--', endComment: '' })
    })
    it('Comment regex test: %', function () {
      // LaTex single line comment
      assert.deepEqual(plugin.findCommentChar('% howdoi query'), { frontComment: '%', endComment: '' })
      // W/o whitespace
      assert.deepEqual(plugin.findCommentChar('%howdoi query'), { frontComment: '%', endComment: '' })
    })
    it('Comment regex test: ;', function () {
      // clojure single line comment
      assert.deepEqual(plugin.findCommentChar('; howdoi query'), { frontComment: ';', endComment: '' })
      // W/o whitespace
      assert.deepEqual(plugin.findCommentChar(';howdoi query'), { frontComment: ';', endComment: '' })
    })
  })

  describe('Removal of comment character from user command -> #removeCommentChar', function () {
    it('Removal of comment char: //', function () {
      const commentChar = {frontComment: '//', endComment: ''}
      // With space
      assert.deepEqual(plugin.removeCommentChar('// howdoi query', commentChar), 'howdoi query')
      // W/o whitespace after comment regex
      assert.deepEqual(plugin.removeCommentChar('//howdoi query', commentChar), 'howdoi query')
    })
    it('Removal of comment char: #', function () {
      const commentChar = { frontComment: '#', endComment: '' }
      // With space
      assert.deepEqual(plugin.removeCommentChar('# howdoi query', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(plugin.removeCommentChar('#howdoi query', commentChar), 'howdoi query')
    })
    it('Removal of comment char: /* */', function () {
      const commentChar = { frontComment: '/*', endComment: '*/' }
      // With space
      assert.deepEqual(plugin.removeCommentChar('/* howdoi query */', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(plugin.removeCommentChar('/*howdoi query*/', commentChar), 'howdoi query')
    })
    it('Removal of comment char: <!-- -->', function () {
      const commentChar = { frontComment: '<!--', endComment: '-->' }
      // With space
      assert.deepEqual(plugin.removeCommentChar('<!-- howdoi query -->', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(plugin.removeCommentChar('<!--howdoi query-->', commentChar), 'howdoi query')
    })
    it('Removal of comment char: --', function () {
      const commentChar = { frontComment: '--', endComment: '' }
      // With space
      assert.deepEqual(plugin.removeCommentChar('-- howdoi query', commentChar), 'howdoi query')
      // W/o whitespace 
      assert.deepEqual(plugin.removeCommentChar('--howdoi query', commentChar), 'howdoi query')
    })
    it('Removal of comment char: %', function () {
      const commentChar = { frontComment: '%', endComment: '' }
      // LaTex single line comment
      assert.deepEqual(plugin.removeCommentChar('% howdoi query', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(plugin.removeCommentChar('%howdoi query', commentChar), 'howdoi query')
    })
    it('Removal of comment char: ;', function () {
      const commentChar = { frontComment: ';', endComment: '' }
      // clojure single line comment
      assert.deepEqual(plugin.removeCommentChar('; howdoi query', commentChar), 'howdoi query')
      // W/o whitespace
      assert.deepEqual(plugin.removeCommentChar(';howdoi query', commentChar), 'howdoi query')
    })
  })

  // describe('retrieveHowdoiOutput function-> #retrieveHowdoiOutput', function () {
  //   it('', function () {
  //   })
  // })

  describe('Removal of howdoi prefix test -> #removeHowdoiPrefix', function () {
    it('Normal Query', function () {
      // Normal Query
      assert.equal(plugin.removeHowdoiPrefix('howdoi query'), 'query')
    })
    it('Query with whitespace', function () {
      // Query with whitespace
      assert.equal(plugin.removeHowdoiPrefix(' howdoi query '), 'query')
    })
    it('Query without howdoi prefix', function () {
      // Query without howdoi prefix
      assert.equal(plugin.removeHowdoiPrefix('query'), 'query')
    })
    it('Query without howdoi prefix and whitespace', function () {
      // Query without howdoi prefix and whitespace
      assert.equal(plugin.removeHowdoiPrefix(' query '), 'query')
    })
  })

  // describe('HowdoiObj interface creation test -> #createHowdoiObj', function () {
  //   it('', function () {
  //   })
  // })

  describe('Add comment character to a string -> #addComment', function () {
    it('Add comment with front/back chars to string', function () {
      // Add comment: '/*' '*/'
      const commentChar1 = { frontComment: '/*', endComment: '*/' }
      assert.equal(plugin.addComment('howdoi query', commentChar1), '/* howdoi query */')
      // Add comment with '<!--' '-->' 
      const commentChar2 = { frontComment: '<!--', endComment: '-->' }
      assert.equal(plugin.addComment('howdoi query', commentChar2), '<!-- howdoi query -->')
    })
    it('Add comment with front char to string', function () {
      // Add comment: #
      const commentChar1 = { frontComment: '#', endComment: '' }
      assert.equal(plugin.addComment('howdoi query', commentChar1), '# howdoi query')
      // Add comment: ;
      const commentChar2 = { frontComment: ';', endComment: '' }
      assert.equal(plugin.addComment('howdoi query', commentChar2), '; howdoi query')
      // Add comment: %
      const commentChar3 = { frontComment: '%', endComment: '' }
      // LaTex single line comment
      assert.equal(plugin.addComment('howdoi query', commentChar3), '% howdoi query')
      // Add coment: -- 
      const commentChar4 = { frontComment: '--', endComment: '' }
      assert.equal(plugin.addComment('howdoi query', commentChar4), '-- howdoi query')
      // Add comment: //
      const commentChar5 = { frontComment: '//', endComment: '' }
      assert.equal(plugin.addComment('howdoi query', commentChar5), '// howdoi query')
    })
  })

})

  
