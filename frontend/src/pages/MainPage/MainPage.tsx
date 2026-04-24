import { useState, type ChangeEvent } from "react";
import { Input, Button } from "antd";

import CopyBtn from "../../components/CopyBtn";

import styles from "./MainPage.module.css";
import { SH_API_URL } from "../../constants";

function MainPage() {
  const [longUrl, setLongUrl] = useState<string>("");
  const [shortUrl, setShortUrl] = useState<string>("");
  const [error, setError] = useState<string>("");
  const handleLongUrlChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLongUrl(e.target.value);
  };

  const handleShortify = async () => {
    try {
      const url = SH_API_URL + "/sh/create";
      const body = JSON.stringify({ original_url: longUrl });
      const response = await fetch(url, {
        method: "POST",
        body,
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("data", data);
        const slug = data.slug;
        const resultUrl = SH_API_URL + "/sh/" + slug;
        setShortUrl(resultUrl);
      } else {
        const message = await response.text();
        setError(message);
        console.log(response);
      }
    } catch (e) {
      console.error("Error:", e);
    }
  };

  return (
    <div className={styles["centered"]}>
      <div className={styles["items"]}>
        {shortUrl ? (
          <>
            <div className={styles["horizontal"]}>
              <p className={styles["shortifiedUrl"]}>{shortUrl}</p>
              <CopyBtn textToCopy={shortUrl} />
            </div>
            <Button onClick={() => setShortUrl("")} type="primary">
              Create new
            </Button>
          </>
        ) : (
          <>
            <p>{error}</p>
            <Input
              size="large"
              type="primary"
              onChange={handleLongUrlChange}
              placeholder="Your long url"
              status={error ? "error" : ""}
            ></Input>
            <Button
              style={{ width: 300 }}
              size="large"
              onClick={handleShortify}
              type="primary"
            >
              Shortify
            </Button>
          </>
        )}
      </div>
    </div>
  );
}

export default MainPage;
