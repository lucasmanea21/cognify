import React, { useState } from "react";
import EEGChart from "../Charts/EEGChart";
import { WebSocketProvider } from "../../providers/WebSocketsProvider";

const PopupMenu: React.FC = () => {
	const [deviceConnected, setDeviceConnected] = useState(true);

	const handleConnectDevice = () => {
		setDeviceConnected(true);
	};

	const handleDisconnectDevice = () => {
		setDeviceConnected(false);
	};

	const handleStartFocusSession = () => {
		console.log("Starting focus session...");
	};

	const handleActivateMindControl = () => {
		console.log("Activating mind control...");
	};

	return (
		<WebSocketProvider>
			<div className="bg-zinc-900 text-white p-4 rounded-md shadow-lg h-full">
				<div className="mb-4">
					<h1 className="text-2xl font-semibold">Cognify</h1>
					{deviceConnected ? (
						<div>
							<p className="text-green-500 text-md mt-4">
								Connected
							</p>
							<p className="text-sm mt-1">
								Your 8-Channel OpenBCI Headband
							</p>
							{/* <button
                onClick={handleDisconnectDevice}
                className="mt-4 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 w-full transition"
              >
                Disconnect Device
              </button> */}
						</div>
					) : (
						<div>
							<p className="text-red-500">Not Connected</p>
							<button
								onClick={handleConnectDevice}
								className="mt-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 w-full transition"
							>
								Connect Device
							</button>
						</div>
					)}
				</div>
				{deviceConnected && (
					<>
						<div className="flex-grow mb-16 my-5 h-[120px] pt-2">
							<p className="text-gray-200 text-md font-bold mb-2">
								Your real-time brain activity
							</p>
							<EEGChart />
						</div>
						<div className="mt-12 pt-3">
							<h2 className="text-lg font-semibold">Actions</h2>
							<button
								onClick={handleStartFocusSession}
								className="mt-4 bg-zinc-800 text-white py-2 px-4 rounded hover:bg-blue-600 w-full transition"
							>
								Start Focus Session
							</button>
							<button
								onClick={handleActivateMindControl}
								className="mt-4 bg-zinc-800 text-white py-2 px-4 rounded hover:bg-blue-600 w-full transition"
							>
								Activate Mind Control
							</button>
						</div>
					</>
				)}
			</div>
		</WebSocketProvider>
	);
};

export default PopupMenu;

