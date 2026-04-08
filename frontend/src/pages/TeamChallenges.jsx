import { useEffect, useState } from 'react'
import { api } from '../api'

function FeedbackBlock({ feedback }) {
  if (!feedback) return null
  return (
    <div className={`feedback-box ${feedback.is_correct ? 'good' : 'warn'}`}>
      <strong>{feedback.is_correct ? 'Team challenge completed' : 'Needs revision'}</strong>
      <p>{feedback.rule_feedback}</p>
      <p><strong>Answer explanation:</strong> {feedback.llm_feedback}</p>
      <p>Mastery {feedback.mastery_before} → {feedback.mastery_after} · Coins {feedback.coins}</p>
    </div>
  )
}

function TeamChallengeCard({ item, onSubmit, teamName }) {
  const [userAnswer, setUserAnswer] = useState('')
  const [collaboratorNote, setCollaboratorNote] = useState('')
  const [showHint, setShowHint] = useState(false)
  const [feedback, setFeedback] = useState(null)
  const [startedAt, setStartedAt] = useState(Date.now())

  useEffect(() => {
    setStartedAt(Date.now())
    setUserAnswer('')
    setCollaboratorNote('')
    setShowHint(false)
    setFeedback(null)
  }, [item.id])

  const submit = async (e) => {
    e.preventDefault()
    const result = await onSubmit(item.id, {
      user_answer: userAnswer,
      collaborator_note: collaboratorNote,
      hints_used: showHint ? 1 : 0,
      time_spent_sec: Math.round((Date.now() - startedAt) / 1000),
    })
    setFeedback(result)
  }

  return (
    <section className="quest-card">
      <div className="quest-header">
        <div>
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </div>
        <div className="pill-row">
          <span className="pill">{item.theme}</span>
          <span className="pill">difficulty {item.difficulty}</span>
          <span className="pill">+{item.reward_coins} coins</span>
        </div>
      </div>
      <div className="prompt-text">{item.prompt}</div>
      <div className="info-box compact-note top-gap">
        <strong>Team</strong>
        <p>{teamName || 'Independent'}</p>
      </div>
      <div className="button-row top-gap">
        <button type="button" className="secondary-btn" onClick={() => setShowHint((v) => !v)}>{showHint ? 'Hide hint' : 'Show hint'}</button>
      </div>
      {showHint ? <div className="info-box top-gap">{item.hint}</div> : null}
      <form className="quest-form" onSubmit={submit}>
        <label>
          Team response
          <textarea rows="4" value={userAnswer} onChange={(e) => setUserAnswer(e.target.value)} />
        </label>
        <label>
          Team collaboration note
          <textarea rows="3" value={collaboratorNote} onChange={(e) => setCollaboratorNote(e.target.value)} placeholder="How did your team discuss or divide the task?" />
        </label>
        <button type="submit">Submit team challenge</button>
      </form>
      <FeedbackBlock feedback={feedback} />
    </section>
  )
}

export default function TeamChallenges({ challenges, onSubmit, teamName }) {
  const [leaderboard, setLeaderboard] = useState([])

  useEffect(() => {
    api.getTeamLeaderboard().then(setLeaderboard).catch(() => setLeaderboard([]))
  }, [])

  return (
    <div className="page-grid">
      <section className="panel wide-span">
        <h2>Team Challenges</h2>
      </section>
      <section className="panel">
        <h3>Team leaderboard</h3>
        <table>
          <thead><tr><th>Team</th><th>Members</th><th>Points</th><th>Completed</th></tr></thead>
          <tbody>{leaderboard.map((row) => <tr key={row.team_name}><td>{row.team_name}</td><td>{row.members}</td><td>{row.collaboration_points}</td><td>{row.completed_challenges}</td></tr>)}</tbody>
        </table>
      </section>
      <section className="panel wide-span">
        <div className="stack-list">
          {challenges.map((item) => <TeamChallengeCard key={item.id} item={item} onSubmit={onSubmit} teamName={teamName} />)}
        </div>
      </section>
    </div>
  )
}
