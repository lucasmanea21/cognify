const { app, Tray, Menu, shell, nativeImage } = require("electron");
const { showNotification } = require("./showNotification");
const config = require("./config");

exports.createTray = () => {
	const trayIcon = nativeImage.createFromPath(config.icon);

	const t = new Tray(trayIcon.resize({ width: 16, height: 16 }));


	t.setToolTip(config.appName);
	// t.setContextMenu(
	// 	Menu.buildFromTemplate([
	// 		{
	// 			label: "Show App",
	// 			click: () => {
	// 				if (!config.mainWindow.isVisible())
	// 					config.mainWindow.show();
	// 			},
	// 		},
	// 		{
	// 			label: "Creator",
	// 			submenu: [
	// 				{
	// 					label: "GitHub @barisbored",
	// 					click: () => {
	// 						shell.openExternal("https://github.com/barisbored");
	// 					},
	// 				},
	// 				{
	// 					label: "E-Mail hi@338.rocks",
	// 					click: () => {
	// 						shell.openExternal("mailto:hi@338.rocks");
	// 					},
	// 				},
	// 				{
	// 					label: "Website",
	// 					click: () => {
	// 						shell.openExternal("https://338.rocks");
	// 					},
	// 				},
	// 			],
	// 		},
	// 		{
	// 			label: "Send Notification",
	// 			click: () =>
	// 				showNotification(
	// 					"This Notification Comes From Tray",
	// 					"Hello, world!",
	// 				),
	// 		},
	// 		{
	// 			label: "Quit",
	// 			click: () => {
	// 				config.isQuiting = true;

	// 				app.quit();
	// 			},
	// 		},
	// 	]),
	// );

	t.on('click', (event, bounds) => {
		const { x, y } = bounds;
		const { width, height } = config.popupWindow.getBounds();
		const yPosition = process.platform === 'darwin' ? y : y - height;
	
		config.popupWindow.setBounds({
		  x: x - width / 2,
		  y: yPosition,
		  width,
		  height,
		});
	
		config.popupWindow.isVisible() ? config.popupWindow.hide() : config.popupWindow.show();
	  });
	

	return t;
};
