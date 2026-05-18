import { useEffect, useState } from "react";
import { Row, Col, Spin } from "antd";
import StatCard from "../components/StatCard";
import { getDashboardStats, type DashboardStats } from "../lib/api";

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    setLoading(true);
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch {
      setStats(null);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: 48 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!stats) {
    return <div style={{ textAlign: "center", padding: 48 }}>加载失败</div>;
  }

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>概览</h2>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <StatCard title="Agent 总数" value={stats.total_agents} icon="robot" />
        </Col>
        <Col span={6}>
          <StatCard
            title="活跃 Agent"
            value={stats.active_agents}
            icon="thunderbolt"
          />
        </Col>
        <Col span={6}>
          <StatCard title="事件总数" value={stats.total_events} icon="schedule" />
        </Col>
        <Col span={6}>
          <StatCard
            title="活跃事件"
            value={stats.active_events}
            icon="fire"
          />
        </Col>
      </Row>
    </div>
  );
}
