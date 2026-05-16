import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAuth } from "./hooks";

import {
  MainPage,
  LinksPage,
  LinkAnalyticPage,
  LoginPage,
  RegisterPage,
  ProfilePage,
} from "./pages";
import Header from "./components/Header";
import { ConfigProvider } from "antd";

function App() {
  const auth = useAuth();
  return (
    <ConfigProvider
      theme={{
        token: {
          fontSize: 16,
        },
      }}
    >
      <Router>
        <Header auth={auth} />
        <Routes>
          <Route path="/" element={<MainPage />}></Route>
          <Route
            path="/analytics"
            element={<LinksPage auth={auth.auth} userId={auth.user?.id} />}
          ></Route>
          <Route path="/analytics/:slug" element={<LinkAnalyticPage />}></Route>
          <Route path="/login" element={<LoginPage />}></Route>
          <Route path="/register" element={<RegisterPage />}></Route>
          <Route
            path="/profile"
            element={<ProfilePage user={auth.user} auth={auth.auth} />}
          ></Route>
        </Routes>
      </Router>
    </ConfigProvider>
  );
}

export default App;
