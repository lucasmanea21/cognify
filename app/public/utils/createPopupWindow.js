const { BrowserWindow } = require('electron');
const { join } = require('path');
const config = require('./config');
const remote = require('@electron/remote/main');

exports.createPopupWindow = async () => {
  const window = new BrowserWindow({
    width: 300,
    height: 500,
    show: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      devTools: config.isDev,
      contextIsolation: false,
    },
    icon: config.icon,
    title: config.appName,
  });

  remote.enable(window.webContents);

  await window.loadURL(
    config.isDev
      ? 'http://localhost:3000/#/popup'
      : `file://${join(__dirname, '..', '../build/index.html#/popup')}`
  );

  window.on('blur', () => {
    window.hide();
  });

  global.popupWindow = window; // Set the global reference for the tray to access

  return window;
};
