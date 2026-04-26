export interface AgentBrowser {
  browser: string;
  clicks_count: number;
}

export interface AgentOs {
  os: string;
  clicks_count: number;
}

export interface AgentDevice {
  device_type: string;
  clicks_count: number;
}

export interface ServerResponse {
  agents: Array<AgentBrowser>;
  devices: Array<AgentDevice>;
  os: Array<AgentOs>;
  clicks_count: number;
  slug: string;
}

export interface ChartValues {
  name: string;
  value: number;
}

export interface MappedServerResponse {
  agents: Array<ChartValues>;
  os: Array<ChartValues>;
  devices: Array<ChartValues>;
  totalClicks: number;
  slug: string;
}
