# Changelog

### 1.4.0 | 2020-04-11

- Propagate signal when subprocess terminates. [#56](https://github.com/microsoft/vscode-test/pull/56).

### 1.3.0 | 2019-12-11

- Add `platform` option. By default, Windows/macOS/Linux defaults to use `win32-archive`, `darwin` and `linux-x64`.
  On Windows, `win32-x64-archive` is also available for using 64 bit version of VS Code. #18.
- Allow running offline when `version` is specified and a matching version is found locally. #51.
- Show error when failing to unzip downloaded vscode archive. #50.

### 1.2.3 | 2019-10-31

- Add `--no-sandbox` option to default `launchArgs` for https://github.com/microsoft/vscode/issues/84238.

### 1.2.2 | 2019-10-31

- Reject `downloadAndUnzipVSCode` when `https.get` fails to parse the JSON sent back from VS Code update server. #44.
- Reject `downloadAndUnzipVSCode` promise when download fails due to network error. #49.

### 1.2.1 | 2019-10-31

- Update https-proxy-agent for https://www.npmjs.com/advisories/1184.

### 1.2.0 | 2019-08-06

- Remove downloaded Insiders at `.vscode-test/vscode-insiders` if it's outdated. [#25](https://github.com/microsoft/vscode-test/issues/25).

### 1.1.0 | 2019-08-02

- Add `resolveCliPathFromVSCodeExecutablePath` that would resolve `vscodeExecutablePath` to VS Code CLI path, which can be used
for extension management features such as `--install-extension` and `--uninstall-extension`. [#31](https://github.com/microsoft/vscode-test/issues/31).

### 1.0.2 | 2019-07-17

- Revert faulty fix for #29.

### 1.0.1 | 2019-07-16

- Use correct CLI path for launching VS Code on macOS / Linux. [#29](https://github.com/Microsoft/vscode-test/issues/29).

### 1.0.0 | 2019-07-03

- Stable release for changes introduced in the `next` tags.

### 1.0.0-next.1 | 2019-06-24

- Improve console message for downloading VS Code. [microsoft/vscode#76090](https://github.com/microsoft/vscode/issues/76090).
- Improve logging. No more prefix `Spawn Error` and direct `stdout` and `stderr` of launched process to `console.log` and `console.error`.
- `stable` added as a download version option.

### 1.0.0-next.0 | 2019-06-24

- Updated API:
	- One single set of options.
	- `extensionPath` => `extensionDevelopmentPath` to align with VS Code launch flags
	- `testRunnerPath` => `extensionTestsPath` to align with VS Code launch flags
	- `testRunnerEnv` => `extensionTestsEnv` to align with VS Code launch flags
	- `additionalLaunchArgs` => `launchArgs`
	- `testWorkspace` removed. Pass path to file/folder/workspace as first argument to `launchArgs` instead.
	- `locale` removed. Pass `--locale` to `launchArgs` instead.

### 0.4.3 | 2019-05-30

- Improved API documentation.

### 0.4.2 | 2019-05-24

- `testWorkspace` is now optional.

### 0.4.1 | 2019-05-02

- Fix Linux crash because `testRunnerEnv` is not merged with `process.env` for spawning the
testing process. [#14](https://github.com/Microsoft/vscode-test/issues/14c).

### 0.4.0 | 2019-04-18

- Add `testRunnerEnv` option. [#13](https://github.com/Microsoft/vscode-test/issues/13).

### 0.3.5 | 2019-04-17

- Fix macOS Insiders incorrect url resolve.

### 0.3.4 | 2019-04-17

- One more fix for Insiders url resolver.

### 0.3.3 | 2019-04-17

- Correct Insiders download link.

### 0.3.2 | 2019-04-17

- Correctly resolve Insider exectuable. [#12](https://github.com/Microsoft/vscode-test/issues/12).

### 0.3.1 | 2019-04-16

- Log errors from stderr of the command to launch VS Code.

### 0.3.0 | 2019-04-13

- 🙌 Add TypeScript as dev dependency. [#9](https://github.com/Microsoft/vscode-test/pull/9).
- 🙌 Adding a simpler way of running tests with only `vscodeExecutablePath` and `launchArgs`. [#8](https://github.com/Microsoft/vscode-test/pull/8).

### 0.2.0 | 2019-04-12

- 🙌 Set `ExecutionPolicy` for Windows unzip command. [#6](https://github.com/Microsoft/vscode-test/pull/6).
- 🙌 Fix NPM http/https proxy handling. [#5](https://github.com/Microsoft/vscode-test/pull/5).
- Fix the option `vscodeLaunchArgs` so it's being used for launching VS Code. [#7](https://github.com/Microsoft/vscode-test/issues/7).

### 0.1.5 | 2019-03-21

- Log folder to download VS Code into.

### 0.1.4 | 2019-03-21

- Add `-NoProfile`, `-NonInteractive` and `-NoLogo` for using PowerShell to extract VS Code. [#2](https://github.com/Microsoft/vscode-test/issues/2).
- Use `Microsoft.PowerShell.Archive\Expand-Archive` to ensure using built-in `Expand-Archive`. [#2](https://github.com/Microsoft/vscode-test/issues/2).

### 0.1.3 | 2019-03-21

- Support specifying testing locale. [#1](https://github.com/Microsoft/vscode-test/pull/1).
- Fix zip extraction failure where `.vscode-test/vscode-<VERSION>` dir doesn't exist on Linux. [#3](https://github.com/Microsoft/vscode-test/issues/3).