import { useEffect, useState } from "react";

import { getProfile, updateProfile } from "../services/api.js";

export function Profile() {
  const [profile, setProfile] = useState(null);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    getProfile().then((data) => {
      setProfile(data);
      setStatus("ready");
    }).catch(() => setStatus("error"));
  }, []);

  async function submit(event) {
    event.preventDefault();
    const updated = await updateProfile({
      full_name: event.target.full_name.value,
      profile_timezone: event.target.profile_timezone.value
    });
    setProfile(updated);
  }

  if (status === "loading") return <p>Loading profile...</p>;
  if (status === "error") return <p className="error">Could not load your profile.</p>;

  return (
    <section>
      <header className="page-header"><h2>My profile</h2><p>Manage your release workspace preferences.</p></header>
      <form className="profile-form" onSubmit={submit}>
        <label>Full name<input name="full_name" defaultValue={profile.full_name} required /></label>
        <label>Time zone<input name="profile_timezone" defaultValue={profile.profile_timezone || ""} /></label>
        <p className="muted-text">Signed in as {profile.email} ({profile.role})</p>
        <button type="submit">Save profile</button>
      </form>
    </section>
  );
}
