import { Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import PanelHome from "./pages/PanelHome";

function RequireAuth({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem("edunest_token");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/admin"
        element={
          <RequireAuth>
            <PanelHome path="/admin" />
          </RequireAuth>
        }
      />
      <Route
        path="/super-admin"
        element={
          <RequireAuth>
            <PanelHome path="/super-admin" />
          </RequireAuth>
        }
      />
      <Route
        path="/teacher"
        element={
          <RequireAuth>
            <PanelHome path="/teacher" />
          </RequireAuth>
        }
      />
      <Route
        path="/student"
        element={
          <RequireAuth>
            <PanelHome path="/student" />
          </RequireAuth>
        }
      />
      <Route
        path="/parent"
        element={
          <RequireAuth>
            <PanelHome path="/parent" />
          </RequireAuth>
        }
      />
    </Routes>
  );
}
