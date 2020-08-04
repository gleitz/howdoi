import { assert} from 'chai'
import 'mocha'
import * as plugin from '../plugin'

//  //: JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
const commentChar1 = {frontComment: '//', endComment: ''}
// #: Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
const commentChar2 = { frontComment: '#', endComment: '' }
// /* */: C++, CSS single line comment 
const commentChar3 = { frontComment: '--', endComment: '' }
// <!-- -->: HTML, PHP, Markdown, Vue single line comment
const commentChar4 = { frontComment: '%', endComment: '' }
// --: SQL, Haskell single line comment
const commentChar5 = { frontComment: ';', endComment: '' }
// %: LaTex single line comment
const commentChar6 = { frontComment: '/*', endComment: '*/' }
// ;: clojure single line comment
const commentChar7 = { frontComment: '<!--', endComment: '-->' }
/* eslint-disable prefer-const*/
const commentCharArr = [commentChar1, commentChar2, commentChar3, commentChar4, commentChar5, commentChar6, 
  commentChar7]

describe('Plugin Tests', function () {

  describe('Find comment regex in string -> #findCommentChar', function () {
    it('String w/o comment regex', function () {
      // null example
      assert.equal(plugin.findCommentChar('howdoi query'), null)
    })
    it('Comment regex test (w/ space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        assert.deepEqual(plugin.findCommentChar(commentedQuery), commentChar)
      }   
    })
    it('Comment regex test (w/o space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + 'howdoi query' + commentChar.endComment
        assert.deepEqual(plugin.findCommentChar(commentedQuery), commentChar)
      }   
    })
  })

  describe('Removal of comment character from user command -> #removeCommentChar', function () {
    it('Removal of front and front/back comment char (w/ space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        assert.equal(plugin.removeCommentChar(commentedQuery, commentChar), 'howdoi query')
      } 
    })
    it('Removal of front and front/back comment char (w/o space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + 'howdoi query' + commentChar.endComment
        assert.equal(plugin.removeCommentChar(commentedQuery, commentChar), 'howdoi query')
      } 
    })
  })

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

  describe('Add comment character to a string -> #addComment', function () {
    it('Add comment with front & front/back char to string: //, #, --, %, ;, /* */, <!-- -->', function () {
      let testString = ''
      for (let commentChar of commentCharArr) {
        if (commentChar.frontComment && (commentChar.endComment !== '')) {
          testString = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        }
        else {
          testString = commentChar.frontComment + ' howdoi query'
        }
        // let testString = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        assert.equal(plugin.addComment('howdoi query', commentChar), testString)
      }   
    })
  })
})
