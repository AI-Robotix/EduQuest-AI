import { NavLink } from 'react-router-dom'

export default function NavBar({ user, onLogout }) {
  const studentLinks = [
    ['/', 'Dashboard'],
    ['/quests', 'Quest Board'],
    ['/quizzes', 'Quiz Hub'],
    ['/exercises', 'Exercise Lab'],
    ['/courses', 'Courses'],
    ['/teams', 'Team Challenges'],
    ['/portfolio', 'Showcase'],
    ['/tutor', 'Grounded Tutor'],
    ['/leaderboard', 'Leaderboard'],
  ]

  const teacherLinks = [
    ['/', 'Teacher Dashboard'],
    ['/feedback', 'Review Queue'],
    ['/leaderboard', 'Leaderboard'],
  ]

  const links = user.role === 'teacher' ? teacherLinks : studentLinks
  const workspaceLabel = user.role === 'teacher' ? 'Teacher workspace' : 'Learning workspace'

  return (
    <header className="topbar">
      <div>
        <h1>EduQuest AI</h1>
        <p className="subtitle">Gamified and AI-Supported Digital Learning Platform</p>
      </div>
      <div className="topbar-right">
        <div className="user-chip">
          <strong>{user.name}</strong>
          <span>{workspaceLabel}</span>
          {user.team_name ? <span>{user.team_name}</span> : null}
          {user.role === 'student' ? <span>{user.coins} coins · level {user.level}</span> : null}
          <button className="secondary-btn logout-btn" onClick={onLogout}>Log out</button>
        </div>
        <nav className="navlinks">
          {links.map(([to, label]) => (
            <NavLink key={to} to={to}>{label}</NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}
