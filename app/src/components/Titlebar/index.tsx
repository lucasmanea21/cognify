import { FC, useEffect } from "react";

const { getCurrentWindow } = window.require("@electron/remote");

export const Titlebar: FC = () => {
	const currentWindow = getCurrentWindow();

	useEffect(() => {
		const icon = document.getElementById("icon") as HTMLElement;
		if (icon) {
			icon.ondragstart = () => false;
		}
	}, []);

	return (
		<div className="sticky top-0 select-none bg-gray-900 h-10 flex items-center justify-center px-4">
			<div className="select-none">
				<p className="text-white font-semibold text-md">Cognify</p>
			</div>
		</div>
	);
};

