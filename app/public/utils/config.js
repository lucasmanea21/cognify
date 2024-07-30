const { join } = require("path");
const isDev = require("electron-is-dev");

let config = {
	appName: "Cognify",
	icon: join(__dirname, "..", "/brain.png"),
	tray: null,
	isQuiting: false,
	mainWindow: null,
	popupWindow: null,
	isDev,
};

module.exports = config;
