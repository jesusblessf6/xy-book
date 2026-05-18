import { useEffect, useState } from "react";
import { Table, Tag, Button, Space, message } from "antd";
import { ThunderboltOutlined } from "@ant-design/icons";
import EventForm from "../components/EventForm";
import {
  listEvents,
  activateEvent,
  createEvent,
  type Event,
} from "../lib/api";

const statusColors: Record<string, string> = {
  draft: "default",
  scheduled: "blue",
  active: "green",
  expired: "red",
};

export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEvents();
  }, []);

  async function loadEvents() {
    setLoading(true);
    try {
      const data = await listEvents();
      setEvents(data);
    } catch {
      message.error("加载事件列表失败");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(data: {
    category: string;
    operator_id: string;
    direct_content?: string;
    source_content?: string;
    source_author?: string;
    source_platform?: string;
    post_type?: string;
    tags?: string[];
    intensity?: string;
  }) {
    try {
      await createEvent(data);
      message.success("事件创建成功");
      await loadEvents();
    } catch {
      message.error("创建事件失败");
    }
  }

  async function handleActivate(id: string) {
    try {
      await activateEvent(id);
      message.success("事件已激活，帖子已发布到社区");
      await loadEvents();
    } catch {
      message.error("激活事件失败");
    }
  }

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      render: (id: string) => id.slice(0, 8),
      width: 100,
    },
    {
      title: "类型",
      dataIndex: "post_type",
      key: "type",
      width: 80,
    },
    {
      title: "分类",
      dataIndex: "category",
      key: "category",
      width: 80,
    },
    {
      title: "强度",
      dataIndex: "intensity",
      key: "intensity",
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
      title: "内容预览",
      dataIndex: "direct_content",
      key: "content",
      render: (v: string | null) =>
        v ? (v.length > 40 ? v.slice(0, 40) + "..." : v) : "-",
      ellipsis: true,
    },
    {
      title: "操作",
      key: "actions",
      render: (_: unknown, record: Event) => (
        <Space>
          {(record.status === "draft" || record.status === "scheduled") && (
            <Button
              type="link"
              icon={<ThunderboltOutlined />}
              onClick={() => handleActivate(record.id)}
              size="small"
            >
              激活
            </Button>
          )}
        </Space>
      ),
      width: 100,
    },
  ];

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
        <h2 style={{ margin: 0 }}>事件管理</h2>
        <EventForm onCreate={handleCreate} />
      </div>
      <Table
        dataSource={events}
        columns={columns}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
        size="small"
      />
    </div>
  );
}
