import { useState } from "react";
import { Modal, Form, Input, Select, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

interface EventFormProps {
  onCreate: (data: {
    category: string;
    operator_id: string;
    direct_content?: string;
    source_content?: string;
    source_author?: string;
    source_platform?: string;
    post_type?: string;
    tags?: string[];
    intensity?: string;
  }) => Promise<void>;
}

const CATEGORIES = [
  { value: "social", label: "社会" },
  { value: "tech", label: "科技" },
  { value: "entertainment", label: "娱乐" },
  { value: "health", label: "健康" },
  { value: "politics", label: "政治" },
  { value: "gender", label: "性别" },
];

const INTENSITIES = [
  { value: "low", label: "低" },
  { value: "medium", label: "中" },
  { value: "high", label: "高" },
];

export default function EventForm({ onCreate }: EventFormProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  async function handleOk() {
    const values = await form.validateFields();
    setLoading(true);
    try {
      await onCreate(values);
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
        创建事件
      </Button>
      <Modal
        title="创建事件"
        open={open}
        onOk={handleOk}
        onCancel={() => setOpen(false)}
        confirmLoading={loading}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ intensity: "medium", post_type: "original" }}
        >
          <Form.Item
            name="category"
            label="分类"
            rules={[{ required: true, message: "请选择分类" }]}
          >
            <Select options={CATEGORIES} placeholder="选择分类" />
          </Form.Item>
          <Form.Item
            name="operator_id"
            label="操作者 ID"
            rules={[{ required: true, message: "请输入操作者 ID" }]}
          >
            <Input placeholder="UUID" />
          </Form.Item>
          <Form.Item name="post_type" label="类型">
            <Select
              options={[
                { value: "original", label: "原创" },
                { value: "repost", label: "转载" },
                { value: "mixed", label: "混合" },
              ]}
            />
          </Form.Item>
          <Form.Item name="direct_content" label="直接内容">
            <Input.TextArea rows={3} placeholder="直接发布的内容" />
          </Form.Item>
          <Form.Item name="source_content" label="来源内容">
            <Input.TextArea rows={3} placeholder="转载的原始内容" />
          </Form.Item>
          <Form.Item name="source_author" label="来源作者">
            <Input placeholder="原文作者" />
          </Form.Item>
          <Form.Item name="source_platform" label="来源平台">
            <Input placeholder="微博/豆瓣/知乎等" />
          </Form.Item>
          <Form.Item name="intensity" label="强度">
            <Select options={INTENSITIES} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
