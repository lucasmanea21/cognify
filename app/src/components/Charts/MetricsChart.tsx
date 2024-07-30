import React, { useContext, useEffect, useState } from "react";
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

interface MetricsChartProps {
	metricKey: "attention" | "stress" | "relaxation";
	maxValue: number;
}

const MetricsChart: React.FC<MetricsChartProps> = ({ metricKey, maxValue }) => {
	const { metricsData } = useContext(WebSocketContext) || { metricsData: [] };
	const [latestPercentage, setLatestPercentage] = useState<number>(0);

	useEffect(() => {
		const calculatePercentage = () => {
			if (metricsData.length) {
				const latestValue =
					metricsData[metricsData.length - 1][metricKey];
				const percentage = (latestValue / maxValue) * 100;
				// console.log(
				// 	`Latest Value: ${latestValue}, Percentage: ${percentage}`,
				// );
				setLatestPercentage(percentage);
			}
		};

		// console.log(metricsData); // Log metricsData to inspect its structure

		calculatePercentage();

		const intervalId = setInterval(calculatePercentage, 2000);

		return () => clearInterval(intervalId);
	}, [metricsData, metricKey, maxValue]);

	const getMessage = (percentage: number) => {
		if (percentage > 75) return "Excellent";
		if (percentage > 50) return "Good";
		if (percentage > 25) return "Fair";
		return "Needs Improvement";
	};

	return (
		<div className="w-full h-[60%] bg-zinc-800 rounded-lg p-4">
			{metricsData.length ? (
				<>
					<ResponsiveContainer width="100%" height="70%">
						<LineChart
							data={metricsData}
							margin={{ top: 20, right: 20, left: 0, bottom: 0 }}
						>
							<Line
								type="monotone"
								dataKey={metricKey}
								stroke="#8884d8"
								strokeWidth={2}
								dot={false}
							/>
						</LineChart>
					</ResponsiveContainer>
					<div className="mt-2 text-center text-gray-200">
						<p>{`Percentage: ${latestPercentage.toFixed(2)}%`}</p>
						<p>{getMessage(latestPercentage)}</p>
					</div>
				</>
			) : (
				<div className="text-center text-gray-500">Loading data...</div>
			)}
		</div>
	);
};

export default MetricsChart;

