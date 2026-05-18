import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout, Menu } from "antd";
import {
  DashboardOutlined,
  RobotOutlined,
  ThunderboltOutlined,
} from "@ant-design/icons";
import Dashboard from "./pages/Dashboard";
import Agents from "./pages/Agents";
import Events from "./pages/Events";

const { Content, Sider } = Layout;

const menuItems = [
  { key: "/", icon: <DashboardOutlined />, label: "概览" },
  { key: "/agents", icon: <RobotOutlined />, label: "Agent 管理" },
  { key: "/events", icon: <ThunderboltOutlined />, label: "事件管理" },
];

function AppLayout() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div
          style={{
            height: 32,
            margin: 16,
            color: "#fff",
            fontWeight: "bold",
            fontSize: 16,
            whiteSpace: "nowrap",
          }}
        >
          XY-Book 管理后台
        </div>
        <Menu
          theme="dark"
          mode="inline"
          items={menuItems}
          onClick={({ key }) => {
            window.location.href = key;
          }}
        />
      </Sider>
      <Layout>
        <Content style={{ margin: 24, padding: 24, background: "#fff" }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/events" element={<Events />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}
