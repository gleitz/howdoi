import { assert} from 'chai'
import 'mocha'
import * as myExtension from '../plugin'

describe('Plugin Tests', function () {
  describe('#removeHowdoiPrefix test', function () {
    it('test 1', function () {
      assert.equal(myExtension.removeHowdoiPrefix('howdoi query'), 'query')
    })
    it('test 2', function () {
      assert.equal(myExtension.removeHowdoiPrefix(' howdoi query '), 'query')
    })
    it('test 3', function () {
      assert.equal(myExtension.removeHowdoiPrefix('query'), 'query')
    })
    it('test 4', function () {
      assert.equal(myExtension.removeHowdoiPrefix(' query '), 'query')
    })
  })
  describe('#modifyCommentedText test', function () {
    it('test 1', function () {
      // null
      assert.equal(myExtension.modifyCommentedText('howdoi query'), null)
    })
    it('test 2', function () {
      // JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
      assert.deepEqual(myExtension.modifyCommentedText('// howdoi query'), ['howdoi query', '//', ''])
      assert.deepEqual(myExtension.modifyCommentedText('//howdoi query'), ['howdoi query', '//', ''])
    })
    it('test 3', function () {
      // Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
      assert.deepEqual(myExtension.modifyCommentedText('# howdoi query'), ['howdoi query', '#', ''] )
      assert.deepEqual(myExtension.modifyCommentedText('#howdoi query'), ['howdoi query', '#', ''] )
    })
    it('test 4', function () {
      // C++, CSS single line comment 
      assert.deepEqual(myExtension.modifyCommentedText('/* howdoi query */'), ['howdoi query', '/*', '*/'] )
    })
    it('test 5', function () {
      // HTML, PHP, Markdown, Vue single line comment
      assert.deepEqual(myExtension.modifyCommentedText('<!-- howdoi query -->'), ['howdoi query', '<!--', '-->'] )
    })
    it('test 6', function () {
      // SQL, Haskell single line comment
      assert.deepEqual(myExtension.modifyCommentedText('-- howdoi query'), ['howdoi query', '--', ''] )
    })
    it('test 7', function () {
      // LaTex single line comment
      assert.deepEqual(myExtension.modifyCommentedText('% howdoi query'), ['howdoi query', '%', ''] )
    })
    it('test 8', function () {
      // clojure single line comment
      assert.deepEqual(myExtension.modifyCommentedText('; howdoi query'), ['howdoi query', ';', ''] ) 
    })
  })
})

  
