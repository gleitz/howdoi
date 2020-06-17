import buble from 'rollup-plugin-buble'
import typescript from 'rollup-plugin-typescript2'

const pkg = require('./package.json')

function getConfig (type) {
  return {
    input: 'src/truncate.ts',
    output: {
      name: 'truncate-html',
      banner: `/*!
 * trancate-html v${pkg.version}
 * Copyright© ${new Date().getFullYear()} Saiya ${pkg.homepage}
 */`,
      format: type,
      file: `dist/truncate.${type}.js`
    },
    plugins: [
      typescript({
        tsconfigOverride: {
          compilerOptions: { module: 'esnext' }
        },
        typescript: require('typescript')
      }),
      buble()
    ],
    external: ['cheerio']
  }
}

export default [
  getConfig('cjs'),
  getConfig('es')
]
