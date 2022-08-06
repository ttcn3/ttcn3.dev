---
title: Visual Studio Code
permalink: /docs/vscode/
---

![vscode TTCN-3 extension preview](/static/vscode-ttcn3-extension-preview.png)

The [VSCode Extension for TTCN-3](https://marketplace.visualstudio.com/items?itemName=Nokia.ttcn3)
is the part which directly faces the user, while most of heavy lifting is done by ntt
and the [language server protocol](https://microsoft.github.io/language-server-protocol/)
in the background.  

## Settings

Access VSCode settings by pressing `Ctrl` and `,` and then search for `ttcn3`:

![settings cast](/static/cast-enable-ntt.gif)

Contributed settings:

| Name                  | Description                                                                    | Default
| --------------------- | ------------------------------------------------------------------------------ | -------
| ttcn3.server.enabled  | Enable TTCN-3 language server for advanced features, like go to defintion, ... | false
| ttcn3.server.update   | Install and update TTCN-3 language server automatically                        | true
| ttcn3.server.codelens | Enable CodeLens for running tests from inside your editor.                     | false
| ttcn3.trace.server    | Trace communication between VS Code and the language server.                   | off


**Commands**

Access VSCode command by pressing `Ctrl`, `Shift`, `P` and then type `ttcn3`:

![commands cast](/static/cast-show-status.gif)

Contributed commands:

| Name                         | Description
| ---------------------------- | ----------------------------
| ttcn3.languageServer.restart | Restart language server
| ttcn3.languageServer.status  | Show language server status

