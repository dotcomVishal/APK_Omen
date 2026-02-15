export default function IntelPage() {
  return (
    <main style={styles.page}>
      <h1 style={styles.title}>INTELLIGENCE NODE</h1>
      <p style={styles.text}>
        AI reasoning & threat classification engine.
      </p>
      <div style={styles.card}>
        <p style={styles.status}>STATUS: ONLINE</p>
        <p style={styles.subtext}>Awaiting input stream...</p>
      </div>
    </main>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#000000",
    color: "#e5e5e5",
    fontFamily: "'Courier New', Courier, monospace",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
  },
  title: {
    fontSize: "2.5rem",
    fontWeight: "700",
    letterSpacing: "2px",
    marginBottom: "10px",
    color: "#ffffff",
  },
  text: {
    color: "#888",
    fontSize: "1.1rem",
    marginBottom: "30px",
  },
  card: {
    backgroundColor: "#050505",
    border: "1px solid #333",
    padding: "30px",
    textAlign: "center",
    width: "100%",
    maxWidth: "500px",
  },
  status: {
    color: "#22c55e", // Green
    fontWeight: "bold",
    fontSize: "1.2rem",
    marginBottom: "10px",
  },
  subtext: {
    color: "#666",
    fontSize: "0.9rem",
  }
};
