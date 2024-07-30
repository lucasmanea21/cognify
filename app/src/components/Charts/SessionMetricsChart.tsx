import React from "react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer,
} from "recharts";

interface SessionMetricsChartProps {
	metricsData: { stress: number; attention: number; relaxation: number }[];
	startTime: string;
}

const SessionMetricsChart: React.FC<SessionMetricsChartProps> = ({
	metricsData,
	startTime,
}) => {
	const formattedData = metricsData.map((metric, index) => ({
		time: new Date(
			new Date(startTime).getTime() + index * 1000,
		).toLocaleTimeString(),
		...metric,
	}));

	return (
		<div className="bg-zinc-800 p-4 rounded-md">
			<ResponsiveContainer width="100%" height={400}>
				<LineChart data={formattedData}>
					{/* <CartesianGrid strokeDasharray="3 3" /> */}
					<XAxis dataKey="time" />
					<YAxis />
					<Tooltip />
					<Line type="monotone" dataKey="stress" stroke="#ff7300" />
					<Line
						type="monotone"
						dataKey="attention"
						stroke="#387908"
					/>
					<Line
						type="monotone"
						dataKey="relaxation"
						stroke="#8884d8"
					/>
				</LineChart>
			</ResponsiveContainer>
		</div>
	);
};

export default SessionMetricsChart;

