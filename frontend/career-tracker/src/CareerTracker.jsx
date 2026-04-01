import { useState } from "react";

const API_BASE = "http://localhost:8001";

const PRIORITY_CONFIG = {
  Beginner: { color: "#4ade80", bg: "rgba(74,222,128,0.12)", label: "Beginner" },
  Intermediate: { color: "#facc15", bg: "rgba(250,204,21,0.12)", label: "Intermediate" },
  Advanced: { color: "#f87171", bg: "rgba(248,113,113,0.12)", label: "Advanced" },
};

const SUGGESTED_ROLES = [
  "AI Engineer", "Data Scientist", "ML Engineer",
  "Software Engineer", "Frontend Developer", "Backend Developer",
  "Full Stack Developer", "DevOps Engineer", "Cloud Engineer", "Product Manager"
];

function Badge({ priority }) {
  const cfg = PRIORITY_CONFIG[priority] || { color: "#94a3b8", bg: "rgba(148,163,184,0.12)", label: priority };
  return (
    <span style={{
      background: cfg.bg,
      color: cfg.color,
      border: `1px solid ${cfg.color}33`,
      borderRadius: 4,
      padding: "2px 8px",
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.06em",
      fontFamily: "'Space Mono', monospace",
      textTransform: "uppercase",
    }}>
      {cfg.label}
    </span>
  );
}

function SkillPill({ skill }) {
  return (
    <span style={{
      background: "rgba(99,102,241,0.12)",
      color: "#a5b4fc",
      border: "1px solid rgba(99,102,241,0.25)",
      borderRadius: 20,
      padding: "4px 12px",
      fontSize: 12,
      fontWeight: 600,
      fontFamily: "'Space Mono', monospace",
      display: "inline-block",
      margin: "3px",
      letterSpacing: "0.02em",
    }}>
      {skill}
    </span>
  );
}

function RoadmapCard({ item, index }) {
  const [done, setDone] = useState(item.status === "Completed");
  return (
    <div
      onClick={() => setDone(d => !d)}
      style={{
        background: done ? "rgba(74,222,128,0.05)" : "rgba(255,255,255,0.03)",
        border: done ? "1px solid rgba(74,222,128,0.2)" : "1px solid rgba(255,255,255,0.06)",
        borderRadius: 8,
        padding: "12px 16px",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 14,
        transition: "all 0.2s",
        marginBottom: 6,
      }}
    >
      <div style={{
        width: 18,
        height: 18,
        borderRadius: 4,
        border: done ? "2px solid #4ade80" : "2px solid rgba(255,255,255,0.2)",
        background: done ? "#4ade80" : "transparent",
        flexShrink: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "all 0.2s",
      }}>
        {done && <svg width="10" height="8" viewBox="0 0 10 8" fill="none"><path d="M1 4L3.5 6.5L9 1" stroke="#0f172a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          color: done ? "rgba(255,255,255,0.4)" : "rgba(255,255,255,0.85)",
          fontSize: 13,
          fontFamily: "'DM Sans', sans-serif",
          textDecoration: done ? "line-through" : "none",
          transition: "all 0.2s",
          marginBottom: 4,
        }}>
          {item.task}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <span style={{ color: "#6366f1", fontSize: 11, fontFamily: "'Space Mono', monospace" }}>
            {item.skill}
          </span>
          <Badge priority={item.priority} />
        </div>
      </div>
    </div>
  );
}

function NotionSyncCard({ data }) {
  return (
    <div style={{
      background: "rgba(99,102,241,0.08)",
      border: "1px solid rgba(99,102,241,0.2)",
      borderRadius: 10,
      padding: "16px 20px",
      marginTop: 8,
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
        <div style={{ width: 8, height: 8, borderRadius: "50%", background: data.success ? "#4ade80" : "#f87171" }} />
        <span style={{ color: "#a5b4fc", fontSize: 12, fontFamily: "'Space Mono', monospace", fontWeight: 700 }}>
          NOTION SYNC
        </span>
      </div>
      <div style={{ color: "rgba(255,255,255,0.6)", fontSize: 13, fontFamily: "'DM Sans', sans-serif" }}>
        {data.message}
      </div>
      <div style={{ marginTop: 8, color: "#4ade80", fontSize: 12, fontFamily: "'Space Mono', monospace" }}>
        {data.tasks_created} tasks created for <strong>{data.role}</strong>
      </div>
    </div>
  );
}

export default function App() {
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("roadmap");
  const [filter, setFilter] = useState("All");

  async function analyze() {
    if (!role.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role: role.trim() }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error");
      }
      const data = await res.json();
      setResult(data);
      setActiveTab("roadmap");
      setFilter("All");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const priorities = ["All", "Beginner", "Intermediate", "Advanced"];
  const filteredRoadmap = result
    ? (filter === "All" ? result.roadmap : result.roadmap.filter(t => t.priority === filter))
    : [];

  const stats = result ? {
    total: result.roadmap.length,
    beginner: result.roadmap.filter(t => t.priority === "Beginner").length,
    intermediate: result.roadmap.filter(t => t.priority === "Intermediate").length,
    advanced: result.roadmap.filter(t => t.priority === "Advanced").length,
  } : null;

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0f",
      fontFamily: "'DM Sans', sans-serif",
      color: "#fff",
      padding: "0 16px 60px",
    }}>
      {/* Google Fonts */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&family=Fraunces:ital,wght@0,700;1,700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 4px; }
        input::placeholder { color: rgba(255,255,255,0.2); }
      `}</style>

      {/* Header */}
      <div style={{ maxWidth: 760, margin: "0 auto", paddingTop: 56 }}>
        <div style={{
          display: "inline-block",
          background: "rgba(99,102,241,0.15)",
          border: "1px solid rgba(99,102,241,0.3)",
          borderRadius: 20,
          padding: "3px 12px",
          color: "#a5b4fc",
          fontSize: 11,
          fontFamily: "'Space Mono', monospace",
          letterSpacing: "0.1em",
          marginBottom: 18,
          textTransform: "uppercase",
        }}>
          Tech-Tsunami Career Tracker
        </div>

        <h1 style={{
          fontSize: "clamp(28px, 5vw, 48px)",
          fontFamily: "'Fraunces', serif",
          fontWeight: 700,
          lineHeight: 1.15,
          margin: "0 0 10px",
          letterSpacing: "-0.02em",
        }}>
          Map your path to{" "}
          <span style={{ fontStyle: "italic", color: "#818cf8" }}>any role</span>
        </h1>

        <p style={{
          color: "rgba(255,255,255,0.45)",
          fontSize: 15,
          marginBottom: 36,
          maxWidth: 480,
          lineHeight: 1.6,
        }}>
          Enter a career role and get a structured learning roadmap with skills, tasks, and priorities — powered by your FastAPI backend.
        </p>

        {/* Input */}
        <div style={{
          background: "rgba(255,255,255,0.04)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: 12,
          padding: 4,
          display: "flex",
          gap: 4,
          marginBottom: 14,
        }}>
          <input
            value={role}
            onChange={e => setRole(e.target.value)}
            onKeyDown={e => e.key === "Enter" && analyze()}
            placeholder="e.g. AI Engineer, Data Scientist, DevOps Engineer..."
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              outline: "none",
              color: "#fff",
              fontSize: 14,
              padding: "10px 14px",
              fontFamily: "'DM Sans', sans-serif",
            }}
          />
          <button
            onClick={analyze}
            disabled={loading || !role.trim()}
            style={{
              background: loading ? "rgba(99,102,241,0.5)" : "#6366f1",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              padding: "10px 22px",
              fontSize: 14,
              fontWeight: 600,
              cursor: loading || !role.trim() ? "not-allowed" : "pointer",
              transition: "background 0.2s",
              fontFamily: "'DM Sans', sans-serif",
              whiteSpace: "nowrap",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            {loading ? (
              <>
                <svg width="14" height="14" viewBox="0 0 14 14" style={{ animation: "spin 1s linear infinite" }}>
                  <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
                  <circle cx="7" cy="7" r="5" stroke="rgba(255,255,255,0.3)" strokeWidth="2" fill="none"/>
                  <path d="M7 2a5 5 0 0 1 5 5" stroke="white" strokeWidth="2" strokeLinecap="round" fill="none"/>
                </svg>
                Analyzing…
              </>
            ) : "Analyze Role →"}
          </button>
        </div>

        {/* Quick picks */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 40 }}>
          {SUGGESTED_ROLES.map(r => (
            <button
              key={r}
              onClick={() => { setRole(r); }}
              style={{
                background: role === r ? "rgba(99,102,241,0.2)" : "rgba(255,255,255,0.04)",
                border: role === r ? "1px solid rgba(99,102,241,0.4)" : "1px solid rgba(255,255,255,0.08)",
                color: role === r ? "#a5b4fc" : "rgba(255,255,255,0.4)",
                borderRadius: 20,
                padding: "4px 12px",
                fontSize: 12,
                cursor: "pointer",
                fontFamily: "'DM Sans', sans-serif",
                transition: "all 0.15s",
              }}
            >
              {r}
            </button>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div style={{
            background: "rgba(248,113,113,0.1)",
            border: "1px solid rgba(248,113,113,0.25)",
            borderRadius: 10,
            padding: "14px 18px",
            color: "#fca5a5",
            fontSize: 13,
            fontFamily: "'Space Mono', monospace",
            marginBottom: 24,
          }}>
            ⚠ {error}
            {error.toLowerCase().includes("fetch") || error.toLowerCase().includes("network") ? (
              <div style={{ marginTop: 8, color: "rgba(255,255,255,0.4)", fontFamily: "'DM Sans', sans-serif", fontSize: 12 }}>
                Make sure your backend is running: <code style={{ color: "#f87171" }}>uvicorn app.main:app --port 8001 --reload</code>
              </div>
            ) : null}
          </div>
        )}

        {/* Results */}
        {result && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }`}</style>

            {/* Role header */}
            <div style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              marginBottom: 24,
              flexWrap: "wrap",
              gap: 12,
            }}>
              <div>
                <div style={{ color: "rgba(255,255,255,0.35)", fontSize: 11, fontFamily: "'Space Mono', monospace", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.1em" }}>
                  Results for
                </div>
                <h2 style={{ margin: 0, fontFamily: "'Fraunces', serif", fontSize: 24, fontWeight: 700 }}>
                  {result.role}
                </h2>
              </div>
              {/* Stats */}
              <div style={{ display: "flex", gap: 16 }}>
                {[
                  { label: "Total", value: stats.total, color: "#a5b4fc" },
                  { label: "Beginner", value: stats.beginner, color: "#4ade80" },
                  { label: "Mid", value: stats.intermediate, color: "#facc15" },
                  { label: "Advanced", value: stats.advanced, color: "#f87171" },
                ].map(s => (
                  <div key={s.label} style={{ textAlign: "center" }}>
                    <div style={{ color: s.color, fontFamily: "'Space Mono', monospace", fontWeight: 700, fontSize: 18 }}>{s.value}</div>
                    <div style={{ color: "rgba(255,255,255,0.3)", fontSize: 10, textTransform: "uppercase", letterSpacing: "0.06em" }}>{s.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Tabs */}
            <div style={{
              display: "flex",
              gap: 2,
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.07)",
              borderRadius: 8,
              padding: 3,
              marginBottom: 20,
              width: "fit-content",
            }}>
              {["roadmap", "skills", "notion"].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  style={{
                    background: activeTab === tab ? "rgba(99,102,241,0.25)" : "transparent",
                    color: activeTab === tab ? "#a5b4fc" : "rgba(255,255,255,0.35)",
                    border: "none",
                    borderRadius: 6,
                    padding: "7px 16px",
                    cursor: "pointer",
                    fontSize: 13,
                    fontWeight: 600,
                    fontFamily: "'DM Sans', sans-serif",
                    transition: "all 0.15s",
                    textTransform: "capitalize",
                  }}
                >
                  {tab === "roadmap" ? `🗺 Roadmap` : tab === "skills" ? `⚡ Skills` : `📓 Notion`}
                </button>
              ))}
            </div>

            {/* Roadmap Tab */}
            {activeTab === "roadmap" && (
              <div>
                {/* Filter */}
                <div style={{ display: "flex", gap: 6, marginBottom: 14 }}>
                  {priorities.map(p => (
                    <button
                      key={p}
                      onClick={() => setFilter(p)}
                      style={{
                        background: filter === p ? "rgba(99,102,241,0.2)" : "transparent",
                        color: filter === p ? "#a5b4fc" : "rgba(255,255,255,0.3)",
                        border: filter === p ? "1px solid rgba(99,102,241,0.35)" : "1px solid rgba(255,255,255,0.07)",
                        borderRadius: 20,
                        padding: "4px 12px",
                        cursor: "pointer",
                        fontSize: 12,
                        fontFamily: "'Space Mono', monospace",
                        transition: "all 0.15s",
                      }}
                    >
                      {p}
                    </button>
                  ))}
                </div>
                <div style={{ color: "rgba(255,255,255,0.25)", fontSize: 11, fontFamily: "'Space Mono', monospace", marginBottom: 10 }}>
                  Click tasks to mark as done
                </div>
                {filteredRoadmap.map((item, i) => (
                  <RoadmapCard key={i} item={item} index={i} />
                ))}
              </div>
            )}

            {/* Skills Tab */}
            {activeTab === "skills" && (
              <div>
                <div style={{ color: "rgba(255,255,255,0.35)", fontSize: 12, fontFamily: "'Space Mono', monospace", marginBottom: 16 }}>
                  {result.skills.length} skills identified
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                  {result.skills.map((s, i) => <SkillPill key={i} skill={s} />)}
                </div>
              </div>
            )}

            {/* Notion Tab */}
            {activeTab === "notion" && (
              <div>
                <div style={{ color: "rgba(255,255,255,0.35)", fontSize: 12, fontFamily: "'Space Mono', monospace", marginBottom: 12 }}>
                  Notion sync status
                </div>
                <NotionSyncCard data={result.notion_sync} />
                <div style={{
                  marginTop: 16,
                  background: "rgba(255,255,255,0.02)",
                  border: "1px solid rgba(255,255,255,0.06)",
                  borderRadius: 8,
                  padding: "12px 16px",
                  fontSize: 12,
                  color: "rgba(255,255,255,0.3)",
                  fontFamily: "'Space Mono', monospace",
                  lineHeight: 1.7,
                }}>
                  ℹ Notion sync is currently mocked. To connect your real Notion workspace, add your NOTION_API_KEY and DATABASE_ID to <code>notion_service.py</code>.
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer hint */}
        {!result && !loading && !error && (
          <div style={{
            color: "rgba(255,255,255,0.12)",
            fontSize: 12,
            fontFamily: "'Space Mono', monospace",
            textAlign: "center",
            marginTop: 60,
            lineHeight: 1.8,
          }}>
            Backend must be running at localhost:8001<br />
            <code style={{ color: "rgba(99,102,241,0.5)" }}>uvicorn app.main:app --port 8001 --reload</code>
          </div>
        )}
      </div>
    </div>
  );
}
