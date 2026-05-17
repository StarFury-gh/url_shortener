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

  const handleOriginClick = () => {
    window.location.href = `${SH_API_URL}/sh/${props.slug}`;
  };

  return (
    <Card
      key={props.slug}
      className={styles["card"]}
      size="medium"
      title={
        <Button type="link" onClick={handleOriginClick}>
          {props.slug}
        </Button>
      }
    >
      <div className={styles["info"]}>
        <p>{props.original_url}</p>
        <Button
          onClick={() => {
            navigate(`/analytic/${props.slug}`);
          }}
        >
          Get analytics
        </Button>
      </div>
    </Card>
  );
}

export default LinkCard;
