import { AuthMessage } from "../../components";

import { Typography, Button } from "antd";

const { Text, Title } = Typography;

import styles from "./ProfilePage.module.css";

interface UserInfo {
  id: number;
  email: string;
}

interface ProfilePageProps {
  auth: boolean;
  user?: UserInfo | null;
}

function ProfilePage(props: ProfilePageProps) {
  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <div className={styles["container"]}>
      <Title>User profile</Title>
      {props.auth ? (
        <div className={styles["content"]}>
          <Text>{props.user?.email}</Text>
          <Text>
            {props.user?.id === null ? null : `User id: #${props.user?.id}`}
          </Text>
          <Button onClick={handleLogout} color="danger" variant="solid">
            Logout
          </Button>
        </div>
      ) : (
        <AuthMessage />
      )}
    </div>
  );
}

export default ProfilePage;
