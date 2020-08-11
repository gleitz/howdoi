import { assert, expect} from 'chai'
import {suite, test} from 'mocha'
import {CommentChars} from '../plugin_interfaces'
import * as removeRegex from '../remove_regexes'
import * as findAttr from '../find_attributes'
import * as createAttr from '../create_attributes'

suite('Plugin Tests', function () {
  //  //: JS, TS, C/ C++/ C#, Java, GO, Rust, Scala, Swift, J#, Dlang single line comment
  const commentChar1: CommentChars = {frontComment: '//', endComment: ''}
  // #: Python, Ruby, powershell, Julia, R, prolog, Crystal, Dockerfile, Diff single line comment
  const commentChar2: CommentChars = { frontComment: '#', endComment: '' }
  // /* */: C++, CSS single line comment 
  const commentChar3: CommentChars = { frontComment: '--', endComment: '' }
  // <!-- -->: HTML, PHP, Markdown, Vue single line comment
  const commentChar4: CommentChars = { frontComment: '%', endComment: '' }
  // --: SQL, Haskell single line comment
  const commentChar5: CommentChars = { frontComment: ';', endComment: '' }
  // %: LaTex single line comment
  const commentChar6: CommentChars = { frontComment: '/*', endComment: '*/' }
  // ;: clojure single line comment
  const commentChar7: CommentChars = { frontComment: '<!--', endComment: '-->' }
  /* eslint-disable prefer-const*/
  const commentCharArr: CommentChars[] = [commentChar1, commentChar2, commentChar3, commentChar4, commentChar5, 
    commentChar6, commentChar7]

  // Global function used for #findNumFlagVal and #removeNumFlag
  function getRandomInt(max: number): number {
    return Math.floor(Math.random() * Math.floor(max))
  }

  suite('Find comment regex in string -> #findCommentChar', function () {
    test('String w/o comment regex', function () {
      // error example
      const err = 'Invalid line comment. Please use single line comment for howdoi.' 
      expect(function(){
        findAttr.findCommentChar('howdoi query')
      }).to.throw(err)
    })
    test('Comment regex test (w/ space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        assert.deepEqual(findAttr.findCommentChar(commentedQuery), commentChar)
      }   
    })
    test('Comment regex test (w/o space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + 'howdoi query' + commentChar.endComment
        assert.deepEqual(findAttr.findCommentChar(commentedQuery), commentChar)
      }   
    })
  })

  suite('Find the Num Flag value from the user command -> #findNumFlagVal', function () {
    test('error examples', function () {
      const err = 'Invalid num flag value' 
      expect(function(){
        findAttr.findNumFlagVal('query -n')
      }).to.throw(err)
      expect(function(){
        findAttr.findNumFlagVal('query -nzl')
      }).to.throw(err)
    })
    test('testing default num 3', function () {
      assert.equal(findAttr.findNumFlagVal('query -n3'), 3)
      assert.equal(findAttr.findNumFlagVal('query -n 3'), 3)
    })
    test('testing non-default numbers', function () {
      const maxNum = 25
      for (let i = 0; i < maxNum; i++) {
        const randomNum = getRandomInt(maxNum)
        const query1 = 'query -n' + String(randomNum)
        const query2 = 'query -n ' + String(randomNum)
        if (randomNum === 0) {
          const err = 'Invalid num flag value'
          expect(function(){
            findAttr.findNumFlagVal(query1)
          }).to.throw(err)
        }
        else {
          assert.equal(findAttr.findNumFlagVal(query1), randomNum)
          assert.equal(findAttr.findNumFlagVal(query2), randomNum)
        }
      }
    })
  })

  suite('Removal of comment character from user command -> #removeCommentChar', function () {
    test('Removal of front and front/back comment char (w/ space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        assert.equal(removeRegex.removeCommentChar(commentedQuery, commentChar), 'howdoi query')
      } 
    })
    test('Removal of front and front/back comment char (w/o space): //, #, --, %, ;, /* */, <!-- -->', function () {
      for (let commentChar of commentCharArr) {
        let commentedQuery = commentChar.frontComment + 'howdoi query' + commentChar.endComment
        assert.equal(removeRegex.removeCommentChar(commentedQuery, commentChar), 'howdoi query')
      } 
    })
  })

  suite('Removal of howdoi prefix test -> #removeHowdoiPrefix', function () {
    test('Normal Query', function () {
      // Normal Query
      assert.equal(removeRegex.removeHowdoiPrefix('howdoi query'), 'query')
    })
    test('Query with whitespace', function () {
      // Query with whitespace
      assert.equal(removeRegex.removeHowdoiPrefix(' howdoi query '), 'query')
    })
    test('Query without howdoi prefix', function () {
      // Query without howdoi prefix
      const err = 'Place "howdoi" in front of query' 
      expect(function(){
        removeRegex.removeHowdoiPrefix('query')
      }).to.throw(err)
    })
    test('Query without howdoi prefix and whitespace', function () {
      // Query without howdoi prefix and whitespace
      const err = 'Place "howdoi" in front of query'
      expect(function(){
        removeRegex.removeHowdoiPrefix(' query ')
      }).to.throw(err)
    })
  })

  suite('Remove the Num Flag and value from the user command -> #removeNumFlag', function () {
    test('testing default num 3', function () {
      assert.equal(removeRegex.removeNumFlag('query -n3'), 'query')
      assert.equal(removeRegex.removeNumFlag('query -n 3'), 'query')
    })
    test('testing non-default numbers', function () {
      const maxNum = 25
      for (let i = 0; i < maxNum; i++) {
        const randomNum = getRandomInt(maxNum)
        const query1 = 'query -n' + String(randomNum)
        const query2 = 'query -n ' + String(randomNum)
        assert.equal(removeRegex.removeNumFlag(query1), 'query')
        assert.equal(removeRegex.removeNumFlag(query2), 'query')
      }
    })
  })

  suite('Create comment character to a string -> #createComment', function () {
    test('Creare comment with front & front/back char to string: //, #, --, %, ;, /* */, <!-- -->', function () {
      let testString = ''
      for (let commentChar of commentCharArr) {
        if (commentChar.frontComment && (commentChar.endComment !== '')) {
          testString = commentChar.frontComment + ' howdoi query ' + commentChar.endComment
        }
        else {
          testString = commentChar.frontComment + ' howdoi query'
        }
        assert.equal(createAttr.createComment('howdoi query', commentChar), testString)
      }   
    })
  })
})
