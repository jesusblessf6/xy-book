import { useState } from "react";
import { Modal, Form, Select, InputNumber, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

const ARCHETYPES = [
  { value: "数据辩手", label: "数据辩手" },
  { value: "情绪化反驳者", label: "情绪化反驳者" },
  { value: "佛系旁观者", label: "佛系旁观者" },
];

interface AgentCreateFormProps {
  onCreate: (archetype: string, count: number) => Promise<void>;
}

export default function AgentCreateForm({ onCreate }: AgentCreateFormProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  async function handleOk() {
    const values = await form.validateFields();
    setLoading(true);
    try {
      await onCreate(values.archetype, values.count);
      setOpen(false);
      form.resetFields();
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Button
        type="primary"
        icon={<PlusOutlined />}
        onClick={() => setOpen(true)}
      >
        创建 Agent
      </Button>
      <Modal
        title="创建 Agent"
        open={open}
        onOk={handleOk}
        onCancel={() => setOpen(false)}
        confirmLoading={loading}
      >
        <Form form={form} layout="vertical" initialValues={{ count: 1 }}>
          <Form.Item
            name="archetype"
            label="人设原型"
            rules={[{ required: true, message: "请选择原型" }]}
          >
            <Select options={ARCHETYPES} placeholder="选择原型" />
          </Form.Item>
          <Form.Item
            name="count"
            label="数量"
            rules={[{ required: true }]}
          >
            <InputNumber min={1} max={20} style={{ width: "100%" }} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
