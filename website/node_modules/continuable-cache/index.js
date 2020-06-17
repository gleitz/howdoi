var Nil = {}

module.exports = cache

// cache := (Continuable<T>) => Continuable<T>
function cache(source) {
    var _err = Nil
    var _value = Nil
    var _result = null
    var listeners = null

    return function continuable(callback) {
        if (_err !== Nil || _value !== Nil) {
            callback(_err, _value)
        } else if (listeners) {
            listeners.push(callback)
        } else {
            listeners = [callback]
            _result = source(function (err, value) {
                _err = err
                _value = value

                listeners.forEach(function (l) { l(err, value) })
            })
        }

        return _result
    }
}
