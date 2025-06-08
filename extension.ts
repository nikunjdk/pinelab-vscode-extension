import * as vscode from 'vscode';
import { ChatPanel } from './chatPanel';

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('chatbot-extension.startChat', () => {
      ChatPanel.createOrShow(context.extensionUri);
    })
  );
}