import { StatusBadge } from "./StatusBadge.jsx";

export function UserTable({ users }) {
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {users.map((user) => (
          <tr key={user.id}>
            <td>{user.full_name}</td>
            <td>{user.email}</td>
            <td>{user.role}</td>
            <td><StatusBadge active={user.is_active} /></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

