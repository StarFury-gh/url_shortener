import { useState, type ChangeEvent } from "react";
import { Input, Button } from "antd";

import styles from "./MainPage.module.css";
import { API_URL } from "../../constants";

function MainPage() {
  const [longUrl, setLongUrl] = useState<string>("");
  const handleLongUrlChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLongUrl(e.target.value);
  };
  const handleShortify = async () => {
    try {
      const url = API_URL + "/sh/create";
      const body = { original_url: longUrl };
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-type": "Application/json",
        },
      });
      if (response.ok) {
        alert("Shortified");
      } else {
        console.log(response);
      }
    } catch (e) {
      console.error("Error:", e);
    }
  };
  return (
    <div className={styles["centered"]}>
      <div className={styles["items"]}>
        <Input
          size="large"
          type="primary"
          onChange={handleLongUrlChange}
          placeholder="Your long url"
        ></Input>
        <Button
          style={{ width: 300 }}
          size="large"
          onClick={handleShortify}
          type="primary"
        >
          Shortify
        </Button>
      </div>
    </div>
  );
}

export default MainPage;
