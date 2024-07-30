import React, { useState, useEffect } from "react";

interface FocusSessionProps {
	onStop: () => void;
}

const FocusSession: React.FC<FocusSessionProps> = ({ onStop }) => {
	const [sessionStartTime, setSessionStartTime] = useState<Date>(new Date());
	const [sessionElapsedTime, setSessionElapsedTime] = useState(0);

	useEffect(() => {
		const timer = setInterval(() => {
			const elapsedTime = Math.floor(
				(new Date().getTime() - sessionStartTime.getTime()) / 1000,
			);
			setSessionElapsedTime(elapsedTime);
		}, 1000);

		return () => clearInterval(timer);
	}, [sessionStartTime]);

	const handleStopFocusSession = () => {
		onStop();
	};

	return (
		<div className="p-4 bg-zinc-800 border border-yellow-300 rounded">
			<h2 className="text-xl font-semibold">Focus Session Active</h2>
			<p>Session will help you focus on your tasks.</p>
			<div className="mt-2">
				<p className="text-lg">
					Elapsed Time: {Math.floor(sessionElapsedTime / 60)}:
					{("0" + (sessionElapsedTime % 60)).slice(-2)}
				</p>
			</div>
			<button
				onClick={handleStopFocusSession}
				className="mt-4 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition w-full"
			>
				Stop Focus Session
			</button>
			<div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
				<div className="p-4 bg-gray-800 border border-gray-700 rounded">
					<h3 className="text-lg font-semibold">Focus Level</h3>
					<p className="text-2xl">80%</p>
					<p className="text-sm mt-2 text-gray-400">
						Keep up the good work!
					</p>
				</div>
				<div className="p-4 bg-gray-800 border border-gray-700 rounded">
					<h3 className="text-lg font-semibold">
						Average Brain Activity
					</h3>
					<p className="text-2xl">High</p>
					<p className="text-sm mt-2 text-gray-400">
						Your brain is highly active during this session.
					</p>
				</div>
			</div>
		</div>
	);
};

export default FocusSession;

