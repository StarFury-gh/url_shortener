import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { Segmented } from "antd";

import { AN_API_URL } from "../../constants";

import BarChart from "../../components/BarChart";
import styles from "./LinkAnalyticPage.module.css";

interface rawAgent {
  browser: string;
  clicks_count: number;
  device_type: string;
  os: string;
}

interface AgentInfo {
  browser: string;
  totalClicks: number;
  deviceType: string;
  os: string;
}

interface LinkStats {
  slug: string;
  totalClicks: number;
  agents: Array<AgentInfo>;
}

interface ChartValues {
  name: string;
  value: number;
}

function mapAgentsForChart(
  agents: Array<AgentInfo> | undefined,
): Array<ChartValues> {
  if (!agents) {
    return [];
  }
  const result = agents.map((agent) => {
    return {
      name: agent.browser,
      value: agent.totalClicks,
    };
  });
  return result;
}

const dataOptions = ["Browser", "OS", "Device"];

function LinkAnalyticPage() {
  const currentSlug = useParams().slug || "";
  const [stats, setStats] = useState<LinkStats>();
  const [infoOption, setInfoOption] = useState<string>(dataOptions[0]);

  useEffect(() => {
    console.log(infoOption);
  }, [infoOption]);

  useEffect(() => {
    const getSlugInfo = async (slug: string) => {
      const url = AN_API_URL + "/analytics/" + slug;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        const rawAgents = data.agents;

        const mappedAgents: Array<AgentInfo> = rawAgents.map(
          (agent: rawAgent) => {
            return {
              browser: agent.browser,
              totalClicks: agent.clicks_count,
              deviceType: agent.device_type,
              os: agent.os,
            };
          },
        );

        const result: LinkStats = {
          slug,
          totalClicks: data.clicked_times,
          agents: mappedAgents,
        };

        setStats(result);
      }
    };
    getSlugInfo(currentSlug);
  }, [currentSlug]);

  return (
    <div className={styles["container"]}>
      <h2>{currentSlug}</h2>
      <p>Total Clicks: {stats?.totalClicks}</p>

      <Segmented<string>
        options={dataOptions}
        onChange={(value) => setInfoOption(value)}
      ></Segmented>

      {<BarChart data={mapAgentsForChart(stats?.agents)} />}
    </div>
  );
}

export default LinkAnalyticPage;
