import { Link } from 'react-router-dom'

export default function TeacherDashboard({ overview, courses, leaderboard, loading }) {
  if (loading) return <div className="panel">Loading teacher dashboard...</div>
  if (!overview) return <div className="panel">No analytics available yet.</div>

  return (
    <div className="page-grid">
      <section className="panel hero-panel wide-span">
        <h2>Teacher dashboard</h2>
        <p>Review learner progress, collaborative activity, and queue targeted educator feedback.</p>
        <div className="stats-grid">
          <div className="stat-card"><span>Total learners</span><strong>{overview.total_students}</strong></div>
          <div className="stat-card"><span>Total submissions</span><strong>{overview.total_submissions}</strong></div>
          <div className="stat-card"><span>Average accuracy</span><strong>{Math.round(overview.average_accuracy * 100)}%</strong></div>
          <div className="stat-card"><span>Courses</span><strong>{courses.length}</strong></div>
        </div>
        <div className="button-row top-gap">
          <Link className="secondary-btn" to="/feedback">Open review queue</Link>
        </div>
      </section>
      <section className="panel">
        <h3>Common misconceptions</h3>
        <div className="stack-list">{overview.common_misconceptions.map((item, idx) => <div className="quest-mini readable-card" key={`${item.label}-${idx}`}><strong>{item.label}</strong><span>{item.count} occurrences</span></div>)}</div>
      </section>
      <section className="panel">
        <h3>Course engagement</h3>
        <table><thead><tr><th>Course</th><th>Interactions</th></tr></thead><tbody>{overview.course_engagement.map((row) => <tr key={row.course}><td>{row.course}</td><td>{row.interactions}</td></tr>)}</tbody></table>
      </section>
      <section className="panel">
        <h3>Leaderboard snapshot</h3>
        <table><thead><tr><th>Name</th><th>Coins</th><th>Completed</th></tr></thead><tbody>{leaderboard.map((entry) => <tr key={entry.name}><td>{entry.name}</td><td>{entry.coins}</td><td>{entry.completed}</td></tr>)}</tbody></table>
      </section>
      <section className="panel">
        <h3>Skill mastery by learner</h3>
        <table><thead><tr><th>Learner</th><th>Skill</th><th>Mastery</th><th>Attempts</th></tr></thead><tbody>{overview.skill_mastery.map((row, idx) => <tr key={`${row.learner}-${row.skill_tag}-${idx}`}><td>{row.learner}</td><td>{row.skill_tag}</td><td>{Math.round(row.mastery * 100)}%</td><td>{row.attempts}</td></tr>)}</tbody></table>
      </section>
      <section className="panel wide-span">
        <h3>Team activity</h3>
        <table><thead><tr><th>Team</th><th>Members</th><th>Collaboration points</th><th>Completed challenges</th></tr></thead><tbody>{overview.team_activity.map((row) => <tr key={row.team_name}><td>{row.team_name}</td><td>{row.members}</td><td>{row.collaboration_points}</td><td>{row.completed_challenges}</td></tr>)}</tbody></table>
      </section>
    </div>
  )
}
