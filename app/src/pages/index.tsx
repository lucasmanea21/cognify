import React, { FC, useState } from "react";
import { Layout } from "../components/Layout";
import EEGChart from "../components/Charts/EEGChart";
import MetricsChart from "../components/Charts/MetricsChart";
import { WebSocketProvider } from "../providers/WebSocketsProvider";
import FocusSession from "../components/Focus";
import {
	startFocusSession,
	stopFocusSession,
	startMindControl,
	stopMindControl,
} from "../utils/api";

export const IndexPage: FC = () => {
	const [deviceConnected, setDeviceConnected] = useState(true);
	const [focusSessionActive, setFocusSessionActive] = useState(false);
	const [mindControlActive, setMindControlActive] = useState(false);
	const [sessionId, setSessionId] = useState<string | null>(null);

	const handleStartFocusSession = async () => {
		try {
			const newSessionId = await startFocusSession();
			setSessionId(newSessionId);
			setFocusSessionActive(true);
			console.log("Focus session started");
		} catch (error) {
			console.error(error);
		}
	};

	const handleStopFocusSession = async () => {
		try {
			await stopFocusSession();
			setFocusSessionActive(false);
			setSessionId(null);
			console.log("Focus session stopped");
		} catch (error) {
			console.error(error);
		}
	};

	const handleActivateMindControl = async () => {
		try {
			await startMindControl();
			setMindControlActive(true);
			console.log("Mind control activated");
		} catch (error) {
			console.error(error);
		}
	};

	const handleDeactivateMindControl = async () => {
		try {
			await stopMindControl();
			setMindControlActive(false);
			console.log("Mind control deactivated");
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<Layout>
			<WebSocketProvider>
				<div className="bg-zinc-900 text-white p-12 shadow-lg min-h-screen flex flex-col space-y-6 overflow-auto">
					{/* Device Connection Status */}
					<div className="mb-4">
						{deviceConnected ? (
							<div>
								<p className="text-green-500 text-xl font-medium">
									Connected
								</p>
								<p className="text-lg mt-1">
									Your 8-channel OpenBCI Headband
								</p>
							</div>
						) : (
							<div>
								<p className="text-red-500">Not Connected</p>
								<button
									onClick={() => setDeviceConnected(true)}
									className="mt-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 w-full transition"
								>
									Connect Device
								</button>
							</div>
						)}
					</div>

					{/* Actions Section */}
					<div className="flex space-x-4">
						<button
							onClick={handleStartFocusSession}
							className="px-4 py-2 bg-gray-800 text-white rounded hover:bg-blue-600 transition w-full"
							disabled={focusSessionActive}
						>
							Start Focus Session
						</button>
						<button
							onClick={
								mindControlActive
									? handleDeactivateMindControl
									: handleActivateMindControl
							}
							className={`px-4 py-2 ${
								mindControlActive ? "bg-red-600" : "bg-gray-800"
							} text-white rounded hover:bg-blue-600 transition w-full`}
							disabled={focusSessionActive}
						>
							{mindControlActive
								? "Deactivate Mind Control"
								: "Activate Mind Control"}
						</button>
					</div>

					{focusSessionActive && (
						<FocusSession onStop={handleStopFocusSession} />
					)}

					{/* Smaller Chart */}
					<div className="w-full h-64">
						<p className="text-gray-200 text-lg font-bold mb-5">
							Your realtime brain activity
						</p>
						<EEGChart />
					</div>

					{/* Metrics Charts */}
					<div className="mt-12 pt-16">
						<p className="text-gray-200 text-lg font-bold mb-5">
							Realtime insights
						</p>
						<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
							<div className="p-4 bg-zinc-800 border border-gray-700 rounded h-64 flex flex-col justify-wrap">
								<h3 className="text-lg font-semibold mb-2">
									Attention Level
								</h3>
								<MetricsChart
									metricKey="attention"
									maxValue={100}
								/>
							</div>
							<div className="p-4 bg-zinc-800 border border-gray-700 rounded h-64">
								<h3 className="text-lg font-semibold mb-2">
									Stress Level
								</h3>
								<MetricsChart
									metricKey="stress"
									maxValue={100}
								/>
							</div>
							<div className="p-4 bg-zinc-800 border border-gray-700 rounded h-64">
								<h3 className="text-lg font-semibold mb-2">
									Relaxation Level
								</h3>
								<MetricsChart
									metricKey="relaxation"
									maxValue={100}
								/>
							</div>
						</div>
					</div>
				</div>
			</WebSocketProvider>
		</Layout>
	);
};

export default IndexPage;

