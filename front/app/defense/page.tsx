"use client";

import { useState } from "react";

export default function AdminPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState("");

  const ADMIN_PASSWORD = "omen"; // change this

  const handleLogin = () => {
    if (password === ADMIN_PASSWORD) {
      setAuthenticated(true);
    } else {
      alert("Access Denied");
    }
  };

  if (!authenticated) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h1 style={styles.title}>🔒 Admin Access</h1>
          <p style={styles.subtitle}>
            This area is restricted. Authorized humans only.
          </p>

          <input
            type="password"
            placeholder="Enter admin password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />

          <button onClick={handleLogin} style={styles.button}>
            Unlock Panel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>🧠 Admin Panel</h1>
        <p style={styles.subtitle}>
          Welcome to the control center. Try not to break production 😌
        </p>

        <div style={styles.section}>
          <h3>System Status</h3>
          <p style={styles.text}>✔ Backend: Online</p>
          <p style={styles.text}>✔ AI Engine: Active</p>
          <p style={styles.text}>✔ Scanner: Operational</p>
        </div>

        <div style={styles.section}>
          <h3>Danger Zone</h3>
          <button style={styles.dangerButton}>
            Reset Everything (Not Really)
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "black",
    color: "white",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  card: {
    width: "420px",
    background: "#020617",
    borderRadius: "14px",
    padding: "30px",
    border: "1px solid #1e293b",
    boxShadow: "0 0 40px rgba(59,130,246,0.15)",
  },

  title: {
    marginBottom: "10px",
  },

  subtitle: {
    color: "#94a3b8",
    fontSize: "14px",
    marginBottom: "20px",
  },

  input: {
    width: "100%",
    padding: "12px",
    background: "black",
    border: "1px solid #334155",
    color: "white",
    borderRadius: "8px",
    marginBottom: "15px",
  },

  button: {
    width: "100%",
    padding: "12px",
    background: "#3b82f6",
    border: "none",
    color: "white",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "bold",
  },

  section: {
    marginTop: "25px",
    paddingTop: "15px",
    borderTop: "1px solid #1e293b",
  },

  text: {
    color: "#cbd5f5",
    fontSize: "14px",
    marginTop: "6px",
  },

  dangerButton: {
    marginTop: "10px",
    padding: "10px 15px",
    background: "#ef4444",
    border: "none",
    color: "white",
    borderRadius: "8px",
    cursor: "pointer",
  },
};
