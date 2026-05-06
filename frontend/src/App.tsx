import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAuth } from "./hooks";

import {
  MainPage,
  LinksPage,
  LinkAnalyticPage,
  LoginPage,
  RegisterPage,
} from "./pages";
import Header from "./components/Header";

function App() {
  const auth = useAuth();
  return (
    <Router>
      <Header auth={auth} />
      <Routes>
        <Route path="/" element={<MainPage />}></Route>
        <Route path="/analytics" element={<LinksPage />}></Route>
        <Route path="/analytics/:slug" element={<LinkAnalyticPage />}></Route>
        <Route path="/login" element={<LoginPage />}></Route>
        <Route path="/register" element={<RegisterPage />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
