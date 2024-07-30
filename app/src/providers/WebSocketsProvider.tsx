import React, { createContext, useEffect, useState, ReactNode } from "react";
import io from "socket.io-client";

const socket = io("ws://127.0.0.1:5000/");

interface WebSocketContextType {
	eegData: any[];
	metricsData: { attention: number; stress: number; relaxation: number }[];
}

export const WebSocketContext = createContext<WebSocketContextType | undefined>(
	undefined,
);

export const WebSocketProvider: React.FC<{ children: ReactNode }> = ({
	children,
}) => {
	const [eegData, setEegData] = useState<any[]>([]);
	const [metricsData, setMetricsData] = useState<any[]>([]);
	const [isDataReady, setIsDataReady] = useState(false);

	useEffect(() => {
		socket.on("connect", () => {
			console.log("Connected to server");
			socket.emit("start_data_stream");
		});

		socket.on(
			"eeg_data",
			(data: {
				data: number[][];
				metrics: {
					attention: number;
					stress: number;
					relaxation: number;
				};
			}) => {
				// console.log("Received eeg_data", data);
				const newEntry = {
					time: new Date().toLocaleTimeString(),
					channel_1: data.data[0][0],
					channel_2: data.data[0][1],
					channel_3: data.data[0][2],
					channel_4: data.data[0][3],
				};

				setEegData((prevData) => {
					const newData = [...prevData, newEntry];
					if (newData.length > 750) newData.shift();
					return newData;
				});

				const newMetricsEntry = {
					time: new Date().toLocaleTimeString(),
					attention: data.metrics.attention,
					stress: data.metrics.stress,
					relaxation: data.metrics.relaxation,
				};

				setMetricsData((prevData) => {
					const newData = [...prevData, newMetricsEntry];
					if (newData.length > 750) newData.shift();
					return newData;
				});

				if (!isDataReady) {
					setIsDataReady(true);
				}
			},
		);

		return () => {
			socket.off("eeg_data");
		};
	}, [isDataReady]);

	return (
		<WebSocketContext.Provider value={{ eegData, metricsData }}>
			{children}
		</WebSocketContext.Provider>
	);
};

