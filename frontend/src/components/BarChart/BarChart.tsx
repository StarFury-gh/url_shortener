import { Column } from "@ant-design/charts";

import styles from "./BarChart.module.css";

interface BarChartProps {
  data: Array<Stats>;
}

interface Stats {
  name: string;
  value: number;
}

function BarChart(props: BarChartProps) {
  const config = {
    data: props.data,
    xField: "name",
    yField: "value",
    shapeField: "column25D",
    scale: {
      x: { padding: 0.5 },
    },
    style: {
      maxWidth: 100,
    },
  };
  return (
    <div className={styles["chart"]}>
      <Column {...config}></Column>
    </div>
  );
}

export default BarChart;
