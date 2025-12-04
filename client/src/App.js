import { Route, Routes } from "react-router-dom"
import Login from "./pages/auth/Login"
import Main from "./pages/Main"

function App() {
	return (
		<Routes>
			<Route path="/" element={<Main/>}/>
			<Route path="/login" element={<Login/>}/>
		</Routes>
	)
}

export default App