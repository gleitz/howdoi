var test = require("tape")

var cache = require("../index")

test("continuable-cache is a function", function (assert) {
    assert.equal(typeof cache, "function")
    assert.end()
})
