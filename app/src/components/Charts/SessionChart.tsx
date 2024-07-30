import React, { useEffect, useState } from "react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	Tooltip,
	ResponsiveContainer,
} from "recharts";

interface RecordedEEGChartProps {
	eegData: number[][];
	startTime: string;
}

const RecordedEEGChart: React.FC<RecordedEEGChartProps> = ({
	eegData,
	startTime,
}) => {
	const [data, setData] = useState<any[]>([]);

	useEffect(() => {
		if (eegData && eegData.length > 0) {
			const startDate = new Date(startTime);
			const formattedData = eegData[0].map((_, index) => {
				const time = new Date(startDate.getTime() + index * 1000); // Assuming each entry is 1 second apart
				return {
					time: time.toLocaleTimeString([], {
						hour: "2-digit",
						minute: "2-digit",
						second: "2-digit",
					}),
					channel_1: eegData[0][index],
					channel_2: eegData[1][index],
					channel_3: eegData[2][index],
					channel_4: eegData[3][index],
				};
			});

			setData(formattedData);
		}
	}, [eegData, startTime]);

	return (
		<div className="w-full h-full bg-zinc-800 rounded-lg p-4">
			{data.length ? (
				<ResponsiveContainer width="100%" height="100%">
					<LineChart
						data={data}
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
						<XAxis dataKey="time" />
						{/* <YAxis /> */}
						<Tooltip />
					</LineChart>
				</ResponsiveContainer>
			) : (
				<div className="text-center text-gray-500">
					No data available
				</div>
			)}
		</div>
	);
};

export default RecordedEEGChart;

