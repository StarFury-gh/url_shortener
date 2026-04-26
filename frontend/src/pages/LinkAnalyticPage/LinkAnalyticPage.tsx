import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { Segmented } from "antd";

import styles from "./LinkAnalyticPage.module.css";

import BarChart from "../../components/BarChart";
import { AN_API_URL } from "../../constants";

import MapServerResponse from "../../utils/analytics";
import type {
  ServerResponse,
  MappedServerResponse,
} from "../../utils/analytics";

interface ChartValues {
  name: string;
  value: number;
}

const dataOptions = ["Browser", "OS", "Devices"];

function LinkAnalyticPage() {
  const currentSlug = useParams().slug || "";
  const [allStats, setAllStats] = useState<MappedServerResponse>();
  const [infoOption, setInfoOption] = useState<string>(dataOptions[0]);
  const [optionStats, setOptionStats] = useState<Array<ChartValues>>();

  useEffect(() => {
    const getSlugInfo = async (slug: string) => {
      const url = AN_API_URL + "/analytics/" + slug;
      const response = await fetch(url);
      if (response.ok) {
        const data: ServerResponse = await response.json();

        console.log("server_response:", data);
        const mapped: MappedServerResponse = await MapServerResponse(data);
        console.log("mapped:", mapped);

        setAllStats(mapped);
      }
    };
    getSlugInfo(currentSlug);
  }, [currentSlug]);

  useEffect(() => {
    const handleOptionChange = () => {
      if (infoOption === "Browser") {
        setOptionStats(allStats?.agents);
      } else if (infoOption === "OS") {
        setOptionStats(allStats?.os);
      } else if (infoOption === "Devices") {
        setOptionStats(allStats?.devices);
      } else {
        setOptionStats([]);
      }
    };
    handleOptionChange();
  }, [infoOption, allStats]);

  return (
    <div className={styles["container"]}>
      <h2>{currentSlug}</h2>
      <p>Total Clicks: {allStats?.totalClicks}</p>

      <Segmented<string>
        options={dataOptions}
        onChange={(value) => setInfoOption(value)}
      ></Segmented>

      {<BarChart data={optionStats || []} />}
    </div>
  );
}

export default LinkAnalyticPage;
