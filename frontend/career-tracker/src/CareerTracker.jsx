import { useState } from "react";

const API_BASE = "http://localhost:8001";

const PRIORITY_CONFIG = {
  Beginner:     { color: "#4ade80", bg: "rgba(74,222,128,0.10)", border: "rgba(74,222,128,0.2)"  },
  Intermediate: { color: "#facc15", bg: "rgba(250,204,21,0.10)",  border: "rgba(250,204,21,0.2)"  },
  Advanced:     { color: "#f87171", bg: "rgba(248,113,113,0.10)", border: "rgba(248,113,113,0.2)" },
};

const SUGGESTED_ROLES = [
  "AI Engineer", "Data Scientist", "ML Engineer",
  "Software Engineer", "Frontend Developer", "Backend Developer",
  "Full Stack Developer", "DevOps Engineer", "Cloud Engineer", "Product Manager",
];

function Badge({ priority }) {
  const cfg = PRIORITY_CONFIG[priority] || { color: "#94a3b8", bg: "rgba(148,163,184,0.1)", border: "rgba(148,163,184,0.2)" };
  return (
    <span style={{
      background: cfg.bg, color: cfg.color,
      border: `1px solid ${cfg.border}`,
      borderRadius: 4, padding: "2px 8px",
      fontSize: 10, fontWeight: 700, letterSpacing: "0.08em",
      fontFamily: "'Space Mono', monospace", textTransform: "uppercase",
    }}>
      {priority}
    </span>
  );
}

function SkillPill({ skill }) {
  return (
    <span style={{
      background: "rgba(99,102,241,0.1)", color: "#a5b4fc",
      border: "1px solid rgba(99,102,241,0.2)",
      borderRadius: 20, padding: "5px 14px",
      fontSize: 12, fontWeight: 600,
      fontFamily: "'Space Mono', monospace",
      display: "inline-block", letterSpacing: "0.02em",
    }}>
      {skill}
    </span>
  );
}

function RoadmapCard({ item }) {
  const [done, setDone] = useState(false);
  return (
    <div
      onClick={() => setDone(d => !d)}
      style={{
        background: done ? "rgba(74,222,128,0.04)" : "rgba(255,255,255,0.02)",
        border: done ? "1px solid rgba(74,222,128,0.15)" : "1px solid rgba(255,255,255,0.06)",
        borderRadius: 10, padding: "12px 16px", cursor: "pointer",
        display: "flex", alignItems: "flex-start", gap: 12,
        transition: "all 0.15s", marginBottom: 6,
      }}
    >
      <div style={{
        marginTop: 2, width: 16, height: 16, borderRadius: 4, flexShrink: 0,
        border: done ? "2px solid #4ade80" : "2px solid rgba(255,255,255,0.15)",
        background: done ? "#4ade80" : "transparent",
        display: "flex", alignItems: "center", justifyContent: "center",
        transition: "all 0.15s",
      }}>
        {done && (
          <svg width="9" height="7" viewBox="0 0 9 7" fill="none">
            <path d="M1 3.5L3 5.5L8 1" stroke="#0f172a" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          color: done ? "rgba(255,255,255,0.3)" : "rgba(255,255,255,0.8)",
          fontSize: 13, lineHeight: 1.5, marginBottom: 6,
          textDecoration: done ? "line-through" : "none", transition: "all 0.15s",
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

function StatCard({ label, value, color }) {
  return (
    <div style={{
      background: "rgba(255,255,255,0.03)",
      border: "1px solid rgba(255,255,255,0.06)",
      borderRadius: 10, padding: "14px 20px", textAlign: "center", flex: 1,
    }}>
      <div style={{ color, fontFamily: "'Space Mono', monospace", fontWeight: 700, fontSize: 22, marginBottom: 4 }}>
        {value}
      </div>
      <div style={{ color: "rgba(255,255,255,0.3)", fontSize: 10, textTransform: "uppercase", letterSpacing: "0.08em" }}>
        {label}
      </div>
    </div>
  );
}

export default function CareerTracker() {
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("roadmap");
  const [filter, setFilter] = useState("All");

  async function analyze() {
    if (!role.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role: role.trim() }),
      });
      if (!res.ok) { const err = await res.json(); throw new Error(err.detail || "Server error"); }
      const data = await res.json();
      setResult(data); setActiveTab("roadmap"); setFilter("All");
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
      minHeight: "100vh", width: "100vw", background: "#09090f",
      color: "#fff", fontFamily: "'DM Sans', sans-serif",
      display: "flex", overflow: "hidden",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=Space+Mono:wght@400;700&family=Fraunces:ital,opsz,wght@0,9..144,700;1,9..144,700&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html, body, #root { width: 100%; height: 100%; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.25); border-radius: 4px; }
        input::placeholder { color: rgba(255,255,255,0.18); }
        button { font-family: 'DM Sans', sans-serif; }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
      `}</style>

      {/* ── LEFT PANEL ── */}
      <div style={{
        width: 360, flexShrink: 0,
        borderRight: "1px solid rgba(255,255,255,0.06)",
        padding: "48px 32px",
        display: "flex", flexDirection: "column", gap: 0,
        height: "100vh", overflowY: "auto",
      }}>
        <div style={{
          display: "inline-flex", alignSelf: "flex-start",
          background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)",
          borderRadius: 20, padding: "3px 12px", color: "#a5b4fc",
          fontSize: 10, fontFamily: "'Space Mono', monospace",
          letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 24,
        }}>
          Tech-Tsunami
        </div>

        <h1 style={{
          fontSize: 34, fontFamily: "'Fraunces', serif", fontWeight: 700,
          lineHeight: 1.15, letterSpacing: "-0.02em", marginBottom: 12,
        }}>
          Map your path to{" "}
          <span style={{ fontStyle: "italic", color: "#818cf8" }}>any role</span>
        </h1>

        <p style={{ color: "rgba(255,255,255,0.4)", fontSize: 13, lineHeight: 1.7, marginBottom: 28 }}>
          Enter a career role and get a structured learning roadmap with skills, tasks, and priorities.
        </p>

        {/* Input row */}
        <div style={{
          background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: 12, padding: 4, display: "flex", gap: 4, marginBottom: 10,
        }}>
          <input
            value={role}
            onChange={e => setRole(e.target.value)}
            onKeyDown={e => e.key === "Enter" && analyze()}
            placeholder="e.g. AI Engineer..."
            style={{
              flex: 1, background: "transparent", border: "none", outline: "none",
              color: "#fff", fontSize: 13, padding: "9px 12px",
            }}
          />
          <button
            onClick={analyze}
            disabled={loading || !role.trim()}
            style={{
              background: loading ? "rgba(99,102,241,0.4)" : "#6366f1",
              color: "#fff", border: "none", borderRadius: 8,
              padding: "9px 16px", fontSize: 13, fontWeight: 600,
              cursor: loading || !role.trim() ? "not-allowed" : "pointer",
              transition: "background 0.2s", whiteSpace: "nowrap",
              display: "flex", alignItems: "center", gap: 6,
            }}
          >
            {loading ? (
              <>
                <svg width="12" height="12" viewBox="0 0 12 12" style={{ animation: "spin 1s linear infinite" }}>
                  <circle cx="6" cy="6" r="4" stroke="rgba(255,255,255,0.25)" strokeWidth="2" fill="none"/>
                  <path d="M6 2a4 4 0 0 1 4 4" stroke="white" strokeWidth="2" strokeLinecap="round" fill="none"/>
                </svg>
                Analyzing…
              </>
            ) : "Analyze →"}
          </button>
        </div>

        {/* Quick picks */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
          {SUGGESTED_ROLES.map(r => (
            <button key={r} onClick={() => setRole(r)} style={{
              background: role === r ? "rgba(99,102,241,0.18)" : "rgba(255,255,255,0.03)",
              border: role === r ? "1px solid rgba(99,102,241,0.35)" : "1px solid rgba(255,255,255,0.07)",
              color: role === r ? "#a5b4fc" : "rgba(255,255,255,0.35)",
              borderRadius: 20, padding: "3px 10px", fontSize: 11, cursor: "pointer", transition: "all 0.15s",
            }}>
              {r}
            </button>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div style={{
            background: "rgba(248,113,113,0.08)", border: "1px solid rgba(248,113,113,0.2)",
            borderRadius: 10, padding: "12px 14px", color: "#fca5a5",
            fontSize: 12, fontFamily: "'Space Mono', monospace", lineHeight: 1.6,
          }}>
            ⚠ {error}
            {(error.toLowerCase().includes("fetch") || error.toLowerCase().includes("network")) && (
              <div style={{ marginTop: 6, color: "rgba(255,255,255,0.3)", fontFamily: "'DM Sans', sans-serif", fontSize: 11 }}>
                Make sure uvicorn is running on port 8001 with CORS configured.
              </div>
            )}
          </div>
        )}

        {/* Stats */}
        {result && stats && (
          <div style={{ marginTop: "auto", paddingTop: 24 }}>
            <div style={{
              color: "rgba(255,255,255,0.2)", fontSize: 10,
              fontFamily: "'Space Mono', monospace", textTransform: "uppercase",
              letterSpacing: "0.1em", marginBottom: 10,
            }}>
              Overview
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <StatCard label="Total" value={stats.total} color="#a5b4fc" />
              <StatCard label="Begin" value={stats.beginner} color="#4ade80" />
              <StatCard label="Mid" value={stats.intermediate} color="#facc15" />
              <StatCard label="Adv" value={stats.advanced} color="#f87171" />
            </div>
          </div>
        )}

        {!result && !error && (
          <div style={{ marginTop: "auto", color: "rgba(255,255,255,0.08)", fontSize: 10, fontFamily: "'Space Mono', monospace" }}>
            backend → localhost:8001
          </div>
        )}
      </div>

      {/* ── RIGHT PANEL ── */}
      <div style={{ flex: 1, height: "100vh", overflowY: "auto", padding: "48px 52px 80px" }}>

        {/* Empty */}
        {!result && !loading && !error && (
          <div style={{
            height: "100%", display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center", gap: 14,
            color: "rgba(255,255,255,0.07)", fontFamily: "'Space Mono', monospace", fontSize: 13, textAlign: "center",
          }}>
            <div style={{ fontSize: 56 }}>🗺</div>
            <div>Select a role and click Analyze</div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div style={{
            height: "100%", display: "flex", alignItems: "center", justifyContent: "center",
            flexDirection: "column", gap: 16,
            color: "rgba(255,255,255,0.3)", fontFamily: "'Space Mono', monospace", fontSize: 13,
          }}>
            <svg width="36" height="36" viewBox="0 0 36 36" style={{ animation: "spin 1s linear infinite" }}>
              <circle cx="18" cy="18" r="14" stroke="rgba(99,102,241,0.15)" strokeWidth="3" fill="none"/>
              <path d="M18 4a14 14 0 0 1 14 14" stroke="#6366f1" strokeWidth="3" strokeLinecap="round" fill="none"/>
            </svg>
            Analyzing {role}…
          </div>
        )}

        {/* Results */}
        {result && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ marginBottom: 32 }}>
              <div style={{
                color: "rgba(255,255,255,0.25)", fontSize: 11,
                fontFamily: "'Space Mono', monospace", textTransform: "uppercase",
                letterSpacing: "0.1em", marginBottom: 6,
              }}>
                Career roadmap for
              </div>
              <h2 style={{ fontFamily: "'Fraunces', serif", fontSize: 32, fontWeight: 700, letterSpacing: "-0.02em" }}>
                {result.role}
              </h2>
            </div>

            {/* Tabs */}
            <div style={{
              display: "flex", gap: 2,
              background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)",
              borderRadius: 10, padding: 3, marginBottom: 24, width: "fit-content",
            }}>
              {[{ key: "roadmap", label: "🗺 Roadmap" }, { key: "skills", label: "⚡ Skills" }, { key: "notion", label: "📓 Notion" }].map(tab => (
                <button key={tab.key} onClick={() => setActiveTab(tab.key)} style={{
                  background: activeTab === tab.key ? "rgba(99,102,241,0.2)" : "transparent",
                  color: activeTab === tab.key ? "#a5b4fc" : "rgba(255,255,255,0.3)",
                  border: "none", borderRadius: 7, padding: "7px 18px",
                  cursor: "pointer", fontSize: 13, fontWeight: 600, transition: "all 0.15s",
                }}>
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Roadmap */}
            {activeTab === "roadmap" && (
              <div>
                <div style={{ display: "flex", gap: 6, marginBottom: 16, flexWrap: "wrap", alignItems: "center" }}>
                  {priorities.map(p => (
                    <button key={p} onClick={() => setFilter(p)} style={{
                      background: filter === p ? "rgba(99,102,241,0.15)" : "transparent",
                      color: filter === p ? "#a5b4fc" : "rgba(255,255,255,0.25)",
                      border: filter === p ? "1px solid rgba(99,102,241,0.3)" : "1px solid rgba(255,255,255,0.06)",
                      borderRadius: 20, padding: "4px 14px", cursor: "pointer",
                      fontSize: 12, fontFamily: "'Space Mono', monospace", transition: "all 0.15s",
                    }}>
                      {p}
                    </button>
                  ))}
                  <span style={{ marginLeft: "auto", color: "rgba(255,255,255,0.15)", fontSize: 11, fontFamily: "'Space Mono', monospace" }}>
                    click to mark done
                  </span>
                </div>
                {filteredRoadmap.map((item, i) => <RoadmapCard key={i} item={item} />)}
              </div>
            )}

            {/* Skills */}
            {activeTab === "skills" && (
              <div>
                <div style={{ color: "rgba(255,255,255,0.3)", fontSize: 12, fontFamily: "'Space Mono', monospace", marginBottom: 20 }}>
                  {result.skills.length} skills identified
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {result.skills.map((s, i) => <SkillPill key={i} skill={s} />)}
                </div>
              </div>
            )}

            {/* Notion */}
            {activeTab === "notion" && (
              <div>
                <div style={{
                  background: "rgba(99,102,241,0.07)", border: "1px solid rgba(99,102,241,0.18)",
                  borderRadius: 12, padding: "20px 24px", marginBottom: 16,
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: result.notion_sync.success ? "#4ade80" : "#f87171" }} />
                    <span style={{ color: "#a5b4fc", fontSize: 11, fontFamily: "'Space Mono', monospace", fontWeight: 700, letterSpacing: "0.08em" }}>
                      NOTION SYNC
                    </span>
                  </div>
                  <div style={{ color: "rgba(255,255,255,0.55)", fontSize: 14, marginBottom: 10 }}>
                    {result.notion_sync.message}
                  </div>
                  <div style={{ color: "#4ade80", fontSize: 12, fontFamily: "'Space Mono', monospace" }}>
                    {result.notion_sync.tasks_created} tasks created for <strong>{result.notion_sync.role}</strong>
                  </div>
                </div>
                <div style={{
                  background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)",
                  borderRadius: 10, padding: "14px 18px", fontSize: 12,
                  color: "rgba(255,255,255,0.25)", fontFamily: "'Space Mono', monospace", lineHeight: 1.8,
                }}>
                  ℹ Notion sync is mocked. Add NOTION_API_KEY and DATABASE_ID to notion_service.py to connect your real workspace.
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
