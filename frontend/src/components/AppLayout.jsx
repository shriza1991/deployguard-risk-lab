import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../services/AuthContext.jsx";

export function AppLayout() {
  const { logout } = useAuth();
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>DeployGuard</h1>
        <nav>
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/users">Users</NavLink>
          <NavLink to="/profile">My profile</NavLink>
        </nav>
        <button className="secondary" onClick={logout}>Sign out</button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
