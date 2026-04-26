import { useState, useEffect } from "react";

import LinkCard from "../../components/LinkCard";

import { SH_API_URL } from "../../constants";
import styles from "./LinksPage.module.css";

interface LinkInfo {
  slug: string;
  original_url: string;
}

function LinkStatsPage() {
  const [links, setLinks] = useState<Array<LinkInfo>>([]);
  useEffect(() => {
    const fetchLinks = async () => {
      try {
        const url = SH_API_URL + "/sh/";
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          setLinks(data.links);
        }
      } catch (e) {
        console.error("Error:", e);
      }
    };
    fetchLinks();
  }, []);
  return (
    <div className={styles["container"]}>
      <div className={styles["links"]}>
        {links.length !== 0 ? (
          links.map((link) => (
            <LinkCard original_url={link.original_url} slug={link.slug} />
          ))
        ) : (
          <p>No links created...</p>
        )}
      </div>
    </div>
  );
}

export default LinkStatsPage;
