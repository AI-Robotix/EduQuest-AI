import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Leaderboard({ entries, loading }) {
  const [teams, setTeams] = useState([])

  useEffect(() => {
    api.getTeamLeaderboard().then(setTeams).catch(() => setTeams([]))
  }, [])

  if (loading) return <div className="panel">Loading leaderboard...</div>
  return (
    <div className="page-grid">
      <section className="panel">
        <h2>Individual leaderboard</h2>
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Coins</th>
              <th>Level</th>
              <th>Streak</th>
              <th>Completed</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry, index) => (
              <tr key={`${entry.name}-${index}`}>
                <td>{index + 1}</td>
                <td>{entry.name}</td>
                <td>{entry.coins}</td>
                <td>{entry.level}</td>
                <td>{entry.streak}</td>
                <td>{entry.completed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="panel">
        <h2>Team leaderboard</h2>
        <table>
          <thead><tr><th>Team</th><th>Members</th><th>Points</th><th>Completed challenges</th></tr></thead>
          <tbody>{teams.map((row) => <tr key={row.team_name}><td>{row.team_name}</td><td>{row.members}</td><td>{row.collaboration_points}</td><td>{row.completed_challenges}</td></tr>)}</tbody>
        </table>
      </section>
    </div>
  )
}
