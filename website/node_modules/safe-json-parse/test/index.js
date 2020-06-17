var test = require("tape")

var safeParse = require("../index")

test("safeParse is a function", function (assert) {
    assert.equal(typeof safeParse, "function")
    assert.end()
})

test("safeParse valid json", function (assert) {
    safeParse("{ \"foo\": true }", function (err, json) {
        assert.ifError(err)
        assert.equal(json.foo, true)

        assert.end()
    })
})

test("safeParse faulty", function (assert) {
    safeParse("WRONG", function (err) {
        assert.ok(err)
        assert.equal(err.message, "Unexpected token W")

        assert.end()
    })
})
