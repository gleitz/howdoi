const spawn = require('.')

const main = async () => {
  const buf = await spawn('ls', ['-al'])
  console.log(buf.toString())
}

main()
