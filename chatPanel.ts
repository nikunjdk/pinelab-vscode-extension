
import * as vscode from 'vscode';
import axios from 'axios';

export class ChatPanel {
  public static currentPanel: ChatPanel | undefined;
  private readonly panel: vscode.WebviewPanel;
  private readonly extensionUri: vscode.Uri;

  private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
    this.panel = panel;
    this.extensionUri = extensionUri;

    this.panel.webview.html = this.getHtmlForWebview(panel.webview);

    this.panel.webview.onDidReceiveMessage(
      async message => {
        if (message.type === 'query') {
          const userQuery = message.text;
          const response = await this.queryBackend(userQuery);
          this.panel.webview.postMessage({ type: 'response', text: response });
        }
      },
      undefined,
      []
    );
  }

  public static createOrShow(extensionUri: vscode.Uri) {
    const column = vscode.window.activeTextEditor?.viewColumn;
    const panel = vscode.window.createWebviewPanel(
      'chatbot',
      'Pine Labs Chatbot',
      column || vscode.ViewColumn.One,
      {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
      }
    );
    ChatPanel.currentPanel = new ChatPanel(panel, extensionUri);
  }

  private getHtmlForWebview(webview: vscode.Webview): string {
    const htmlPath = vscode.Uri.joinPath(this.extensionUri, 'media', 'chat.html');
    return require('fs').readFileSync(htmlPath.fsPath, 'utf8');
  }

  private async queryBackend(query: string): Promise<string> {
    try {
      const res = await axios.post('http://192.168.1.7:5000/generate-prompt', { query });
      console.log(res)
      return res.data.prompt || '[No response]';
    } catch (err) {
      return 'Error contacting backend.';
    }
  }
}