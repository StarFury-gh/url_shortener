import { useNavigate } from "react-router-dom";
import { Button } from "antd";

import styles from "./Header.module.css";

interface UserInfo {
  id: number;
  email: string;
}

interface AuthState {
  auth: boolean;
  user: UserInfo | null;
}

interface HeaderProps {
  auth: AuthState;
}

function Header(props: HeaderProps) {
  const navigate = useNavigate();

  return (
    <header>
      <div className={styles["links"]}>
        <Button type="link" size="large" onClick={() => navigate("/")}>
          Shortify
        </Button>
        <Button type="link" size="large" onClick={() => navigate("/analytics")}>
          Analytics
        </Button>
        {props.auth.auth ? (
          <Button type="link" size="large" onClick={() => navigate("/profile")}>
            Profile
          </Button>
        ) : (
          <Button type="link" size="large" onClick={() => navigate("/login")}>
            Login
          </Button>
        )}
      </div>
    </header>
  );
}

export default Header;
