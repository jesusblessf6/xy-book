const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_API_KEY || "xybook-dev-key";

const headers = {
  "Content-Type": "application/json",
  "x-api-key": API_KEY,
};

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...headers, ...options?.headers },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

// --- Agents ---

export interface Agent {
  id: string;
  user_id: string;
  persona_archetype: string;
  persona_variant: number;
  status: string;
  last_browsed_at: string | null;
  last_posted_at: string | null;
  next_browse_at: string | null;
  created_at: string;
}

export async function listAgents(): Promise<Agent[]> {
  return fetchAPI<Agent[]>("/api/agents/");
}

export async function createAgent(archetype: string, count: number = 1): Promise<Agent[]> {
  if (count > 1) {
    return fetchAPI<Agent[]>("/api/agents/batch-create", {
      method: "POST",
      body: JSON.stringify({ persona_archetype: archetype, count }),
    });
  }
  const result = await fetchAPI<Agent>("/api/agents/", {
    method: "POST",
    body: JSON.stringify({ persona_archetype: archetype }),
  });
  return [result];
}

export async function startAgent(agentId: string): Promise<Agent> {
  return fetchAPI<Agent>(`/api/agents/${agentId}/start`, { method: "POST" });
}

export async function stopAgent(agentId: string): Promise<Agent> {
  return fetchAPI<Agent>(`/api/agents/${agentId}/stop`, { method: "POST" });
}

// --- Events ---

export interface Event {
  id: string;
  post_type: string | null;
  source_author: string | null;
  source_platform: string | null;
  source_url: string | null;
  source_content: string | null;
  direct_content: string | null;
  operator_id: string;
  operator_comment: string | null;
  category: string;
  tags: string[];
  intensity: string;
  status: string;
  scheduled_at: string | null;
  activated_at: string | null;
  created_at: string;
}

export async function listEvents(status?: string): Promise<Event[]> {
  const params = status ? `?status_filter=${status}` : "";
  return fetchAPI<Event[]>(`/api/pipeline/events${params}`);
}

export async function createEvent(data: {
  category: string;
  operator_id: string;
  direct_content?: string;
  source_content?: string;
  source_author?: string;
  source_platform?: string;
  post_type?: string;
  tags?: string[];
  intensity?: string;
}): Promise<Event> {
  return fetchAPI<Event>("/api/pipeline/events", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function activateEvent(eventId: string): Promise<Event> {
  return fetchAPI<Event>(`/api/pipeline/events/${eventId}/activate`, {
    method: "POST",
  });
}

// --- Stats ---

export interface DashboardStats {
  total_agents: number;
  active_agents: number;
  total_events: number;
  active_events: number;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const [agents, events] = await Promise.all([listAgents(), listEvents()]);
  return {
    total_agents: agents.length,
    active_agents: agents.filter((a) => a.status === "active").length,
    total_events: events.length,
    active_events: events.filter((e) => e.status === "active").length,
  };
}
