import { Card, Button } from "antd";
import { useNavigate } from "react-router-dom";

import styles from "./LinkCard.module.css";
import { SH_API_URL } from "../../constants";

interface LinkCardProps {
  slug: string;
  original_url: string;
}

function LinkCard(props: LinkCardProps) {
  const navigate = useNavigate();
  return (
    <Card
      key={props.slug}
      className={styles["card"]}
      size="medium"
      title={
        <Button
          type="link"
          onClick={() => {
            navigate(`${SH_API_URL}/sh/${props.slug}`);
          }}
        >
          {props.slug}
        </Button>
      }
    >
      <div className={styles["info"]}>
        <p>{props.original_url}</p>
        <Button
          onClick={() => {
            navigate(`/analytics/${props.slug}`);
          }}
        >
          Get analytics
        </Button>
      </div>
    </Card>
  );
}

export default LinkCard;
