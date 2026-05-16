import { Button } from "antd";
import { useNavigate } from "react-router-dom";

import { Typography } from "antd";

const { Title, Text } = Typography;

import styles from "./AuthMessage.module.css";

function AuthMessage() {
  const navigate = useNavigate();

  return (
    <div className={styles["content"]}>
      <Title>Not authorized</Title>
      <Text style={{ fontSize: "20px" }}>
        To use analytics, please, register or sign in
      </Text>
      <div className={styles["links"]}>
        <Button onClick={() => navigate("/register")}>Register now</Button>
        <Text>or</Text>
        <Button onClick={() => navigate("/login")}>Sign in</Button>
      </div>
    </div>
  );
}

export default AuthMessage;
