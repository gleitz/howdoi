<p>
  <h1 align="center">vscode-test</h1>
</p>

<p align="center">
  <a href="https://dev.azure.com/vscode/vscode-test/_build?definitionId=15">
    <img src="https://img.shields.io/azure-devops/build/vscode/350ef5c4-15fc-411a-9a5e-0622da4da69c/15.svg?label=Azure%20DevOps&logo=Azure%20Devops&style=flat-square">
  </a>
  <a href="https://travis-ci.org/microsoft/vscode-test">
    <img src="https://img.shields.io/travis/microsoft/vscode-test.svg?label=Travis&logo=Travis&style=flat-square">
  </a>
</p>

This module helps you test VS Code extensions.

Supported:

- Node >= 8.x
- Windows >= Windows Server 2012+ / Win10+ (anything with Powershell >= 5.0)
- macOS
- Linux

## Usage

See [./sample](./sample) for a runnable sample, with [Azure DevOps Pipelines](https://github.com/microsoft/vscode-test/blob/master/sample/azure-pipelines.yml) and [Travis CI](https://github.com/microsoft/vscode-test/blob/master/.travis.yml) configuration.

```ts
async function go() {
	try {
		const extensionDevelopmentPath = path.resolve(__dirname, '../../../')
		const extensionTestsPath = path.resolve(__dirname, './suite')

		/**
		 * Basic usage
		 */
		await runTests({
			extensionDevelopmentPath,
			extensionTestsPath
		})

		const extensionTestsPath2 = path.resolve(__dirname, './suite2')
		const testWorkspace = path.resolve(__dirname, '../../../test-fixtures/fixture1')

		/**
		 * Running another test suite on a specific workspace
		 */
		await runTests({
			extensionDevelopmentPath,
			extensionTestsPath: extensionTestsPath2,
			launchArgs: [testWorkspace]
		})

		/**
		 * Use 1.36.1 release for testing
		 */
		await runTests({
			version: '1.36.1',
			extensionDevelopmentPath,
			extensionTestsPath,
			launchArgs: [testWorkspace]
		})

		/**
		 * Use Insiders release for testing
		 */
		await runTests({
			version: 'insiders',
			extensionDevelopmentPath,
			extensionTestsPath,
			launchArgs: [testWorkspace]
		})

		/**
		 * Noop, since 1.36.1 already downloaded to .vscode-test/vscode-1.36.1
		 */
		await downloadAndUnzipVSCode('1.36.1')

		/**
		 * Manually download VS Code 1.35.0 release for testing.
		 */
		const vscodeExecutablePath = await downloadAndUnzipVSCode('1.35.0')
		await runTests({
			vscodeExecutablePath,
			extensionDevelopmentPath,
			extensionTestsPath,
			launchArgs: [testWorkspace]
		})

		/**
		 * Install Python extension
		 */
		const cliPath = resolveCliPathFromVSCodeExecutablePath(vscodeExecutablePath)
		cp.spawnSync(cliPath, ['--install-extension', 'ms-python.python'], {
			encoding: 'utf-8',
			stdio: 'inherit'
		})

		/**
		 * - Add additional launch flags for VS Code
		 * - Pass custom environment variables to test runner
		 */
		await runTests({
			vscodeExecutablePath,
			extensionDevelopmentPath,
			extensionTestsPath,
			launchArgs: [
				testWorkspace,
				// This disables all extensions except the one being testing
				'--disable-extensions'
			],
			// Custom environment variables for extension test script
			extensionTestsEnv: { foo: 'bar' }
		})

		/**
		 * Use win64 instead of win32 for testing Windows
		 */
		if (process.platform === 'win32') {
			await runTests({
				extensionDevelopmentPath,
				extensionTestsPath,
				version: '1.40.0',
				platform: 'win32-x64-archive'
			});
		}

	} catch (err) {
		console.error('Failed to run tests')
		process.exit(1)
	}
}

go()
```

## Development

- `yarn install`
- Make necessary changes in [`lib`](./lib)
- `yarn compile` (or `yarn watch`)
- In [`sample`](./sample), run `yarn install`, `yarn compile` and `yarn test` to make sure integration test can run successfully

## License

[MIT](LICENSE)

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
