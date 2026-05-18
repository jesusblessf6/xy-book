import { Table, Tag, Button, Space } from "antd";
import { PlayCircleOutlined, PauseCircleOutlined } from "@ant-design/icons";
import type { Agent } from "../lib/api";

interface AgentTableProps {
  agents: Agent[];
  loading: boolean;
  onStart: (id: string) => void;
  onStop: (id: string) => void;
}

const statusColors: Record<string, string> = {
  active: "green",
  idle: "default",
  paused: "orange",
};

export default function AgentTable({
  agents,
  loading,
  onStart,
  onStop,
}: AgentTableProps) {
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      render: (id: string) => id.slice(0, 8),
      width: 100,
    },
    {
      title: "原型",
      dataIndex: "persona_archetype",
      key: "archetype",
      width: 120,
    },
    {
      title: "变体",
      dataIndex: "persona_variant",
      key: "variant",
      width: 80,
    },
    {
      title: "状态",
      dataIndex: "status",
      key: "status",
      render: (status: string) => (
        <Tag color={statusColors[status] || "default"}>{status}</Tag>
      ),
      width: 100,
    },
    {
      title: "下次浏览",
      dataIndex: "next_browse_at",
      key: "next_browse",
      render: (v: string | null) => (v ? new Date(v).toLocaleString("zh-CN") : "-"),
      width: 180,
    },
    {
      title: "操作",
      key: "actions",
      render: (_: unknown, record: Agent) => (
        <Space>
          {record.status !== "active" ? (
            <Button
              type="link"
              icon={<PlayCircleOutlined />}
              onClick={() => onStart(record.id)}
              size="small"
            >
              启动
            </Button>
          ) : (
            <Button
              type="link"
              danger
              icon={<PauseCircleOutlined />}
              onClick={() => onStop(record.id)}
              size="small"
            >
              停止
            </Button>
          )}
        </Space>
      ),
      width: 120,
    },
  ];

  return (
    <Table
      dataSource={agents}
      columns={columns}
      rowKey="id"
      loading={loading}
      pagination={{ pageSize: 10 }}
      size="small"
    />
  );
}
