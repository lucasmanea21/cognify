import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { supabase } from "../shared/supabase";
import RecordedEEGChart from "../components/Charts/SessionChart";
import SessionMetricsChart from "../components/Charts/SessionMetricsChart";
import { Layout } from "../components/Layout";

const SessionPage: React.FC = () => {
	const { id } = useParams<{ id: string }>();
	const [sessionData, setSessionData] = useState<any>([]);
	const [loading, setLoading] = useState(true);
	const [latestEEGData, setLatestEEGData] = useState<number[][] | null>(null);
	const [metricsData, setMetricsData] = useState<
		{ stress: number; attention: number; relaxation: number }[]
	>([]);

	useEffect(() => {
		const fetchSessionData = async () => {
			const { data, error } = await supabase
				.from("focus_sessions")
				.select("session_id, id, timestamp, eeg_data, metrics")
				.eq("session_id", id)
				.order("timestamp", { ascending: true });

			if (error) {
				console.error("Error fetching session data:", error);
				setLoading(false);
				return;
			}

			setSessionData(data);
			if (data.length > 0) {
				setLatestEEGData(data[data.length - 1].eeg_data); // Use EEG data from the last entry
				const metrics = data.map((entry: any) => entry.metrics);
				setMetricsData(metrics.flat()); // Use metrics data from all entries
			}
			setLoading(false);
		};

		fetchSessionData();
	}, [id]);

	const calculateSessionDuration = () => {
		if (sessionData.length > 0) {
			const startTime = new Date(sessionData[0].timestamp);
			const endTime = new Date(
				sessionData[sessionData.length - 1].timestamp,
			);
			const duration = Math.abs(endTime.getTime() - startTime.getTime());
			const minutes = Math.floor((duration / 1000 / 60) % 60);
			const seconds = Math.floor((duration / 1000) % 60);
			return `${minutes}m ${seconds}s`;
		}
		return "N/A";
	};

	const formatSessionTitle = (timestamp: string) => {
		const date = new Date(timestamp);
		const now = new Date();
		const yesterday = new Date(now);
		yesterday.setDate(yesterday.getDate() - 1);

		if (date.toDateString() === now.toDateString()) {
			return `Today at ${date.toLocaleTimeString()}`;
		} else if (date.toDateString() === yesterday.toDateString()) {
			return `Yesterday at ${date.toLocaleTimeString()}`;
		} else {
			return date.toLocaleString();
		}
	};

	const handleDownload = () => {
		const element = document.createElement("a");
		const file = new Blob([JSON.stringify(sessionData, null, 2)], {
			type: "application/json",
		});
		element.href = URL.createObjectURL(file);
		element.download = `session_${id}.json`;
		document.body.appendChild(element);
		element.click();
	};

	return (
		<Layout>
			<div className="bg-zinc-900 text-white p-12 shadow-lg min-h-screen space-y-6">
				<h1 className="text-2xl font-semibold mb-4">
					{sessionData.length > 0 &&
						formatSessionTitle(sessionData[0].timestamp)}
				</h1>
				{loading ? (
					<p>Loading session data...</p>
				) : sessionData.length === 0 ? (
					<p>No session data found.</p>
				) : (
					<div>
						<div className="mb-4">
							<p className="text-sm">
								Duration: {calculateSessionDuration()}
							</p>
						</div>
						<div className="w-full h-64">
							<p className=" text-xl font-semibold mb-3">
								Your brain activity
							</p>
							{latestEEGData && (
								<RecordedEEGChart
									eegData={latestEEGData}
									startTime={sessionData[0].timestamp}
								/>
							)}
						</div>
						<div className="w-full h-64 mt-8 pt-10">
							<p className=" text-xl font-semibold mb-3">
								Session Metrics
							</p>
							{metricsData && (
								<SessionMetricsChart
									metricsData={metricsData}
									startTime={sessionData[0].timestamp}
								/>
							)}
						</div>
						{/* Insights Section */}
						<div className="mt-8 pt-60">
							<h3 className="text-xl font-semibold mb-4">
								Insights
							</h3>
							<p className="text-sm">Focus Level: TBD</p>
							<p className="text-sm">Stress Level: TBD</p>
						</div>
						{/* Download Button */}
						<div className="mt-8">
							<button
								onClick={handleDownload}
								className="px-4 py-2 bg-zinc-800 text-white rounded hover:bg-blue-600 transition"
							>
								Download Raw Data
							</button>
						</div>
					</div>
				)}
			</div>
		</Layout>
	);
};

export default SessionPage;

