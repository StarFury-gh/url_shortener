import { Pie } from "@ant-design/charts";

interface PieChartProps {
  data?: Array<ChartValues>;
}

interface ChartValues {
  name: string;
  value: number;
}

function PieChart(props: PieChartProps) {
  const config = {
    data: props?.data,
    angleField: "value",
    colorField: "name",
    label: {
      text: "value",
      style: {
        fontWeight: "bold",
      },
    },
    legend: {
      color: {
        title: false,
        position: "right",
        rowPadding: 5,
      },
    },
  };
  return <Pie {...config}></Pie>;
}

export default PieChart;
