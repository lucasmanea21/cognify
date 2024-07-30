import React from "react";
import { Link } from "react-router-dom";
import { FaHome, FaBook, FaCog } from "react-icons/fa";

const Sidebar: React.FC = () => {
	return (
		<div className="h-screen bg-zinc-800 text-white p-5 flex flex-col justify-between">
			<div>
				<h1 className="text-2xl font-bold mb-8">Cognify</h1>
				<ul className="space-y-4">
					<li>
						<Link
							to="/"
							className="flex items-center text-white hover:text-gray-300"
						>
							{/* <FaHome className="mr-2" /> Home */}
							Home
						</Link>
					</li>
					<li>
						<Link
							to="/sessions"
							className="flex items-center text-white hover:text-gray-300"
						>
							My Sessions
						</Link>
					</li>
				</ul>
			</div>
			<div>
				<Link
					to="/settings"
					className="flex items-center text-white hover:text-gray-300"
				>
					<FaCog className="mr-2" /> Settings
				</Link>
			</div>
		</div>
	);
};

export default Sidebar;

