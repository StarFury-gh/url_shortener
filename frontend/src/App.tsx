import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { MainPage, LinksPage, LinkAnalyticPage } from "./pages";
import Header from "./components/Header";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<MainPage />}></Route>
        <Route path="/analytics" element={<LinksPage />}></Route>
        <Route path="/analytics/:slug" element={<LinkAnalyticPage />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
