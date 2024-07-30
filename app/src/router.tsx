import { FC } from "react";
import { HashRouter, Route, Routes } from "react-router-dom";
import { IndexPage } from "./pages";
import { PopupPage } from "./pages/popup";
import PopupMenu from "./components/Menu";
import MySessions from "./pages/sessions";
import SessionPage from "./pages/session";
import Settings from "./pages/settings";

export const Router: FC = () => {
	return (
		<HashRouter>
			<Routes>
				<Route path="/">
					<Route index element={<IndexPage />} />
					<Route path="sessions" element={<MySessions />} />
					<Route path="popup" element={<PopupMenu />} />
					<Route path="settings" element={<Settings />} />
					<Route path="/session/:id" element={<SessionPage />} />
				</Route>
			</Routes>
		</HashRouter>
	);
};

