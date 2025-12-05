import { Route, Routes } from "react-router-dom"
import Login from "./pages/auth/Login"
import Register from "./pages/auth/Register"
import Main from "./pages/Main"

function App() {
	return (
		<Routes>
			<Route path="/" element={<Main/>}/>
			<Route path="/login" element={<Login/>}/>
			<Route path="/register" element={<Register/>}/>
		</Routes>
	)
}

export default App