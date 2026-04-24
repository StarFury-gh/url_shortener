import { Link } from "react-router-dom";
import { Button } from "antd";

import styles from "./Header.module.css";

function Header() {
  return (
    <header>
      <div className={styles["links"]}>
        <Button type="link" size="large">
          <Link to="/">Shortify</Link>
        </Button>
        <Button type="link" size="large">
          <Link to="/analytics">Analytics</Link>
        </Button>
      </div>
    </header>
  );
}

export default Header;
