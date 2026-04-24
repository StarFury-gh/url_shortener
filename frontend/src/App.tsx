import { BrowserRouter as Router, Routes, Route } from "react-router-dom"

import { MainPage, LinkStatsPage } from "./pages"

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MainPage/>}></Route>
                <Route path="/stats" element={<LinkStatsPage/>}></Route>
            </Routes>
        </Router>
    )
}

export default App