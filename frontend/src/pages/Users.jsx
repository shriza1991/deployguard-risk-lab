import { useEffect, useState } from "react";

import { UserTable } from "../components/UserTable.jsx";
import { listUsers } from "../services/api.js";

export function Users() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    listUsers()
      .then((data) => {
        setUsers(data);
        setStatus("ready");
      })
      .catch(() => setStatus("error"));
  }, []);

  if (status === "loading") {
    return <p>Loading users...</p>;
  }
  if (status === "error") {
    return <p className="error">Could not load users.</p>;
  }
  return (
    <section>
      <header className="page-header">
        <h2>Users</h2>
        <p>Identity records synchronized from the API.</p>
      </header>
      <UserTable users={users} />
    </section>
  );
}

