import { Card, Button } from "antd";
import { Link } from "react-router-dom";

import styles from "./LinkCard.module.css";
import { SH_API_URL } from "../../constants";

interface LinkCardProps {
  slug: string;
  original_url: string;
}

function LinkCard(props: LinkCardProps) {
  return (
    <Card
      title={
        <Button type="link">
          <Link to={`${SH_API_URL}/sh/${props.slug}`}>{props.slug}</Link>
        </Button>
      }
    >
      <div className={styles["info"]}>
        <p>{props.original_url}</p>
        <Button>
          <Link to={`/analytics/${props.slug}`}>More</Link>
        </Button>
      </div>
    </Card>
  );
}

export default LinkCard;
