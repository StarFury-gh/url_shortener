import { Button } from "antd";
import { useNavigate } from "react-router-dom";

import styles from "./AuthMessage.module.css";

function AuthMessage() {
  const navigate = useNavigate();

  return (
    <div className="">
      <h1>Not authorized</h1>
      <p>To use analytics, please, register or authorize</p>
      <div className={styles["links"]}>
        <Button onClick={() => navigate("/register")}>Register now</Button>
        <p>or</p>
        <Button onClick={() => navigate("/login")}>Sign in</Button>
      </div>
    </div>
  );
}

export default AuthMessage;
