import { Card, Statistic } from "antd";
import {
  RobotOutlined,
  ThunderboltOutlined,
  ScheduleOutlined,
  FireOutlined,
} from "@ant-design/icons";

interface StatCardProps {
  title: string;
  value: number;
  icon: "robot" | "thunderbolt" | "schedule" | "fire";
}

const iconMap = {
  robot: <RobotOutlined style={{ fontSize: 24 }} />,
  thunderbolt: <ThunderboltOutlined style={{ fontSize: 24 }} />,
  schedule: <ScheduleOutlined style={{ fontSize: 24 }} />,
  fire: <FireOutlined style={{ fontSize: 24 }} />,
};

export default function StatCard({ title, value, icon }: StatCardProps) {
  return (
    <Card>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ color: "#1677ff" }}>{iconMap[icon]}</div>
        <Statistic title={title} value={value} />
      </div>
    </Card>
  );
}
