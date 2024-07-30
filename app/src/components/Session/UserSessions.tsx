import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { supabase } from "../../shared/supabase";

const Sessions: React.FC = () => {
	const [sessions, setSessions] = useState<any[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchSessions = async () => {
			const { data, error } = await supabase
				.from("focus_sessions")
				.select("session_id, timestamp");

			if (error) {
				console.error("Error fetching sessions:", error);
				setLoading(false);
				return;
			}

			// Process data to get unique sessions with start and end times
			const sessionMap: Record<
				string,
				{ start_time: string; end_time: string }
			> = {};

			data.forEach((session) => {
				if (!sessionMap[session.session_id]) {
					sessionMap[session.session_id] = {
						start_time: session.timestamp,
						end_time: session.timestamp,
					};
				} else {
					if (
						new Date(session.timestamp) <
						new Date(sessionMap[session.session_id].start_time)
					) {
						sessionMap[session.session_id].start_time =
							session.timestamp;
					}
					if (
						new Date(session.timestamp) >
						new Date(sessionMap[session.session_id].end_time)
					) {
						sessionMap[session.session_id].end_time =
							session.timestamp;
					}
				}
			});

			const processedSessions = Object.keys(sessionMap)
				.map((sessionId) => ({
					session_id: sessionId,
					start_time: sessionMap[sessionId].start_time,
					end_time: sessionMap[sessionId].end_time,
				}))
				.sort(
					(a, b) =>
						new Date(b.start_time).getTime() -
						new Date(a.start_time).getTime(),
				);

			setSessions(processedSessions);
			setLoading(false);
		};

		fetchSessions();
	}, []);

	const formatFriendlyDate = (date: Date) => {
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

	const calculateDuration = (startTime: string, endTime: string) => {
		const start = new Date(startTime);
		const end = new Date(endTime);
		const duration = Math.abs(end.getTime() - start.getTime());
		const minutes = Math.floor((duration / 1000 / 60) % 60);
		const seconds = Math.floor((duration / 1000) % 60);
		return `${minutes}m ${seconds}s`;
	};

	return (
		<div className="bg-zinc-900 text-white p-12 shadow-lg min-h-screen space-y-6">
			<h1 className="text-2xl font-semibold mb-4">My Sessions</h1>
			{loading ? (
				<p>Loading sessions...</p>
			) : sessions.length === 0 ? (
				<p>No sessions found.</p>
			) : (
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					{sessions.map((session) => (
						<Link
							to={`/session/${session.session_id}`}
							key={session.session_id}
						>
							<div className="p-4 bg-zinc-800 border border-gray-700 rounded">
								<h3 className="text-lg font-semibold">
									{formatFriendlyDate(
										new Date(session.start_time),
									)}
								</h3>
								<p className="text-sm">
									Duration:{" "}
									{calculateDuration(
										session.start_time,
										session.end_time,
									)}
								</p>
							</div>
						</Link>
					))}
				</div>
			)}
		</div>
	);
};

export default Sessions;

