# howdoi Packaged Visual Studio Code Extension

Locally install the howdoi Visual Studio Code Extension.

## Installation

- Head over [here](https://github.com/gleitz/howdoi#installation) to install howdoi on your machine.

- Open Visual Studio Code and open the Command Palette and run:

        Shell Command: Install ‘code’ command in PATH
    ![Image of Shell Command](https://github.com/gleitz/howdoi/tree/master/extension/vscode-pkg/img/code-command.png)
    
    Restart your terminal.
- Within the `extension/vscode-pkg` folder, run:

        code --install-extension howdoi-0.0.1.vsix

- Add the unpackaged files to your VS Code extensions folder (the path of the folder can be found [here](https://code.visualstudio.com/api/working-with-extensions/publishing-extension#your-extension-folder)). If no files were created within the `extension/vscode-pkg`, check if the files are in the extension folder path.

- Look over the README within the unpackaged files for more info on how to run howdoi within VS Code.


