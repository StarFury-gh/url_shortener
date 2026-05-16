import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { Select } from "antd";

import styles from "./LinkAnalyticPage.module.css";

import { AuthMessage } from "../../components";
import { BarChart, PieChart } from "../../components/charts/";
import { AN_API_URL, ACCESS_TOKEN } from "../../constants";

import MapServerResponse from "../../utils/analytics";
import type {
  ServerResponse,
  MappedServerResponse,
} from "../../utils/analytics";

interface ChartValues {
  name: string;
  value: number;
}

const SelectDataOptions = [
  { value: "Browser", label: "Browser" },
  { value: "OS", label: "OS" },
  { value: "Device", label: "Device" },
];

const SelectChartType = [
  { value: "Bar", label: "Bar" },
  { value: "Pie", label: "Pie" },
];

interface AnalyticsPageProps {
  auth: boolean;
}

const dataOptions = ["Browser", "OS", "Devices"];

function LinkAnalyticPage(props: AnalyticsPageProps) {
  const currentSlug = useParams().slug || "";
  const [allStats, setAllStats] = useState<MappedServerResponse>();
  const [infoOption, setInfoOption] = useState<string>(dataOptions[0]);
  const [optionStats, setOptionStats] = useState<Array<ChartValues>>();
  const [chartType, setChartType] = useState<string>(SelectChartType[0].value);

  const chartComponents: Record<string, React.ElementType> = {
    Bar: BarChart,
    Pie: PieChart,
  };

  const ChartComponent = chartComponents[chartType];

  useEffect(() => {
    if (props.auth) {
      const getSlugInfo = async (slug: string) => {
        const url = AN_API_URL + "/analytics/" + slug;
        const token = localStorage.getItem(ACCESS_TOKEN);
        const response = await fetch(url, {
          headers: {
            Authorization: token || "",
          },
        });
        if (response.ok) {
          const data: ServerResponse = await response.json();

          const mapped: MappedServerResponse = await MapServerResponse(data);

          setAllStats(mapped);
        }
      };
      getSlugInfo(currentSlug);
    }
  }, [currentSlug, props.auth]);

  useEffect(() => {
    const handleOptionChange = () => {
      if (infoOption === "Browser") {
        setOptionStats(allStats?.agents);
      } else if (infoOption === "OS") {
        setOptionStats(allStats?.os);
      } else if (infoOption === "Device") {
        setOptionStats(allStats?.devices);
      } else {
        setOptionStats([]);
      }
    };
    handleOptionChange();
  }, [infoOption, allStats]);

  return (
    <div className={styles["container"]}>
      {props.auth ? (
        <>
          <div className={styles["settings"]}>
            <h2>{currentSlug}</h2>
            <p>Total Clicks: {allStats?.totalClicks}</p>
            <div className={styles["option"]}>
              <p>Info about:</p>
              <Select
                defaultValue="Browser"
                style={{ width: 120 }}
                onChange={(value) => setInfoOption(value)}
                options={SelectDataOptions}
              />
            </div>
            <div className={styles["option"]}>
              <p>Chart:</p>
              <Select
                defaultValue="Bar"
                style={{ width: 120 }}
                onChange={(value) => setChartType(value)}
                options={SelectChartType}
              />
            </div>
          </div>
          <ChartComponent data={optionStats || []} />
        </>
      ) : (
        <AuthMessage />
      )}
    </div>
  );
}

export default LinkAnalyticPage;
