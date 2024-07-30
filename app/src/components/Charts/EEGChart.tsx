import React, { useContext } from "react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer,
} from "recharts";
import { WebSocketContext } from "../../providers/WebSocketsProvider";

const EEGChart = () => {
	const { eegData } = useContext(WebSocketContext) || { eegData: [] };

	return (
		<div className="w-full h-full bg-zinc-800 rounded-lg p-4">
			{eegData.length ? (
				<ResponsiveContainer width="100%" height="100%">
					<LineChart
						data={eegData}
						margin={{ top: 20, right: 20, left: 0, bottom: 0 }}
					>
						<Line
							type="monotone"
							dataKey="channel_1"
							stroke="#8884d8"
							strokeWidth={2}
							dot={false}
						/>
						<Line
							type="monotone"
							dataKey="channel_2"
							stroke="#82ca9d"
							strokeWidth={2}
							dot={false}
						/>
						<Line
							type="monotone"
							dataKey="channel_3"
							stroke="#ffc658"
							strokeWidth={2}
							dot={false}
						/>
						<Line
							type="monotone"
							dataKey="channel_4"
							stroke="#ff7300"
							strokeWidth={2}
							dot={false}
						/>
					</LineChart>
				</ResponsiveContainer>
			) : (
				<div className="text-center text-gray-500">Loading data...</div>
			)}
		</div>
	);
};

export default EEGChart;

