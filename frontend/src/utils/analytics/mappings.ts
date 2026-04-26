import type {
  ChartValues,
  AgentBrowser,
  AgentDevice,
  AgentOs,
  ServerResponse,
  MappedServerResponse,
} from "./interfaces";

function MapAgentsBrowser(agents: Array<AgentBrowser>): Array<ChartValues> {
  if (!agents) {
    return [];
  }
  const result: Array<ChartValues> = agents.map((agent) => {
    return {
      name: agent.browser,
      value: agent.clicks_count,
    };
  });
  return result;
}

function MapAgentsDevices(devices: Array<AgentDevice>): Array<ChartValues> {
  if (!devices) {
    return [];
  }
  const result: Array<ChartValues> = devices.map((device) => {
    return {
      name: device.device_type,
      value: device.clicks_count,
    };
  });
  return result;
}

function MapAgentsOs(os: Array<AgentOs>): Array<ChartValues> {
  if (!os) {
    return [];
  }
  const result: Array<ChartValues> = os.map((system) => {
    return {
      name: system.os,
      value: system.clicks_count,
    };
  });
  return result;
}

export async function MapServerResponse(
  response: ServerResponse,
): Promise<MappedServerResponse> {
  if (!response) {
    throw "Cannot map undefined object.";
  }
  const mappedAgentsBrowsers: Array<ChartValues> = MapAgentsBrowser(
    response.agents,
  );
  const mappedAgentsOs: Array<ChartValues> = MapAgentsOs(response.os);
  const mappedAgentsDevices: Array<ChartValues> = MapAgentsDevices(
    response.devices,
  );
  const result: MappedServerResponse = {
    agents: mappedAgentsBrowsers,
    os: mappedAgentsOs,
    devices: mappedAgentsDevices,
    totalClicks: response.clicks_count,
    slug: response.slug,
  };
  return result;
}
