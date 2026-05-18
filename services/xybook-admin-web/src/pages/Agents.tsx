import { useEffect, useState } from "react";
import { message } from "antd";
import AgentTable from "../components/AgentTable";
import AgentCreateForm from "../components/AgentCreateForm";
import {
  listAgents,
  createAgent,
  startAgent,
  stopAgent,
  type Agent,
} from "../lib/api";

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
  }, []);

  async function loadAgents() {
    setLoading(true);
    try {
      const data = await listAgents();
      setAgents(data);
    } catch {
      message.error("加载 Agent 列表失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(archetype: string, count: number) {
    try {
      await createAgent(archetype, count);
      message.success(`成功创建 ${count} 个 Agent`);
      await loadAgents();
    } catch {
      message.error("创建 Agent 失败");
    }
  }

  async function handleStart(id: string) {
    try {
      await startAgent(id);
      message.success("Agent 已启动");
      await loadAgents();
    } catch {
      message.error("启动 Agent 失败");
    }
  }

  async function handleStop(id: string) {
    try {
      await stopAgent(id);
      message.success("Agent 已停止");
      await loadAgents();
    } catch {
      message.error("停止 Agent 失败");
    }
  }

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h2 style={{ margin: 0 }}>Agent 管理</h2>
        <AgentCreateForm onCreate={handleCreate} />
      </div>
      <AgentTable
        agents={agents}
        loading={loading}
        onStart={handleStart}
        onStop={handleStop}
      />
    </div>
  );
}
