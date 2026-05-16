import { useState, useEffect } from "react";

import LinkCard from "../../components/LinkCard";
import { AuthMessage } from "../../components";

import { SH_API_URL, ACCESS_TOKEN } from "../../constants";
import styles from "./LinksPage.module.css";

interface LinkInfo {
  slug: string;
  original_url: string;
}

interface LinksPageProps {
  auth: boolean;
  userId?: number;
}

function LinkStatsPage(props: LinksPageProps) {
  const [links, setLinks] = useState<Array<LinkInfo>>([]);
  useEffect(() => {
    const fetchLinks = async () => {
      if (props.auth) {
        try {
          const url = SH_API_URL + "/sh/";
          const token = localStorage.getItem(ACCESS_TOKEN);
          const response = await fetch(url, {
            headers: {
              Authorization: token || "",
            },
          });
          if (response.ok) {
            const data = await response.json();
            setLinks(data.links);
          }
        } catch (e) {
          console.error("Error:", e);
        }
      }
    };
    fetchLinks();
  }, []);
  return (
    <div className={styles["container"]}>
      {props.auth ? (
        <div className={styles["links"]}>
          {links.length !== 0 ? (
            links.map((link) => (
              <LinkCard
                key={link.slug}
                original_url={link.original_url}
                slug={link.slug}
              />
            ))
          ) : (
            <p>No links created...</p>
          )}
        </div>
      ) : (
        <AuthMessage />
      )}
    </div>
  );
}

export default LinkStatsPage;
