const test = require('tape')
const spawn = require('..')

test('running none existent command throws ENOENT', async t => {
  try {
    await spawn('notexisting')
  } catch (err) {
    t.equal(err.message, 'spawn notexisting ENOENT')
    t.end()
  }
})

test('failed command throws error with code', async t => {
  try {
    await spawn('false')
  } catch (err) {
    t.equal(err.message, 'child exited with code 1')
    t.ok(err.stderr, '.stderr is set')
    t.is(err.stderr.length, 0, 'BufferList has 0 length in this case')
    t.end()
  }
})

test('running existent works fine', async t => {
  const promise = spawn('true')
  t.ok(promise.child, 'has child set')
  await promise
  t.end()
})

test('resolves to buffered stdout output', async t => {
  const files = [
    'index.js',
    'node_modules',
    'package.json',
    'README.md',
    'test'
  ]
  t.plan(files.length)
  const output = await spawn('ls')
  const lines = output.toString().split('\n')
  files.forEach(file => {
    t.ok(lines.includes(file), `found ${file}`)
  })
})

test('options.stdio === "inherit" resolves to empty string', async t => {
  const output = await spawn('ls', { stdio: 'inherit' })
  t.deepEqual(output, '', 'empty string')
  t.end()
})
