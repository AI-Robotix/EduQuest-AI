import { Link } from 'react-router-dom'

export default function StudentDashboard({ dashboard, loading, feedback = [] }) {
  if (loading) return <div className="panel">Loading dashboard...</div>
  if (!dashboard) return <div className="panel">No dashboard data available.</div>

  const { user, learner_state, total_attempts, accuracy, mastery, recommended_quests, recommended_courses, recent_activity } = dashboard

  return (
    <div className="page-grid">
      <section className="panel hero-panel wide-span">
        <h2>Welcome back, {user.name}</h2>
        <p>Track your progress, choose the next learning activity, collaborate with your team, and build shareable proof of your skills.</p>
        <div className="stats-grid">
          <div className="stat-card"><span>Coins</span><strong>{user.coins}</strong></div>
          <div className="stat-card"><span>Level</span><strong>{user.level}</strong></div>
          <div className="stat-card"><span>Streak</span><strong>{user.streak}</strong></div>
          <div className="stat-card"><span>Learner state</span><strong>{learner_state}</strong></div>
          <div className="stat-card"><span>Attempts</span><strong>{total_attempts}</strong></div>
          <div className="stat-card"><span>Accuracy</span><strong>{Math.round(accuracy * 100)}%</strong></div>
          <div className="stat-card"><span>Team</span><strong>{user.team_name || 'Independent'}</strong></div>
          <div className="stat-card"><span>Teacher notes</span><strong>{feedback.length}</strong></div>
        </div>
        <div className="info-box compact-note">
          <strong>What are coins for?</strong>
          <p>Coins unlock bonus course labs and advanced case studies.</p>
        </div>
      </section>

      <section className="panel">
        <h3>Recommended quests</h3>
        <div className="stack-list">
          {recommended_quests.map((quest) => (
            <div className="quest-mini readable-card" key={quest.id}>
              <strong>{quest.title}</strong>
              <span>{quest.track} · difficulty {quest.difficulty}</span>
              <p>{quest.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3>Recommended courses</h3>
        <div className="stack-list">
          {recommended_courses.map((course) => (
            <div className="quest-mini readable-card" key={course.id}>
              <strong>{course.title}</strong>
              <span>{course.category} · {course.level}</span>
              <p>{course.description}</p>
              <Link to={`/courses/${course.slug}`}>Open course</Link>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3>Collaboration and teacher support</h3>
        <div className="stack-list">
          <div className="quest-mini readable-card">
            <strong>Your team</strong>
            <span>{user.team_name || 'Independent'}</span>
            <p>Use Team Challenges to complete collaborative tasks inspired by digital-literacy design work.</p>
            <Link to="/teams">Open Team Challenges</Link>
          </div>
          <div className="quest-mini readable-card">
            <strong>Teacher feedback</strong>
            <span>{feedback.length} notes available</span>
            <p>Open your showcase to review teacher comments and endorsements attached to your learning progress.</p>
            <Link to="/portfolio">Open Showcase</Link>
          </div>
        </div>
      </section>

      <section className="panel">
        <h3>Skill mastery</h3>
        {mastery.length === 0 ? <p>Complete activities to initialize learner modelling.</p> : (
          <div className="stack-list">
            {mastery.map((item) => (
              <div className="mastery-row" key={item.skill_tag}>
                <div>
                  <strong>{item.skill_tag.replaceAll('_', ' ')}</strong>
                  <p>{item.attempts} attempts</p>
                </div>
                <div className="progress-wrapper">
                  <div className="progress-bar"><div style={{ width: `${item.mastery * 100}%` }} /></div>
                  <span>{Math.round(item.mastery * 100)}%</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="panel wide-span">
        <h3>Recent activity</h3>
        {recent_activity.length === 0 ? <p>No recent activity yet.</p> : (
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Title</th>
                <th>Correct</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {recent_activity.map((item) => (
                <tr key={`${item.item_type}-${item.id}-${item.created_at}`}>
                  <td>{item.item_type}</td>
                  <td>{item.item_title}</td>
                  <td>{item.is_correct ? 'Yes' : 'No'}</td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  )
}
