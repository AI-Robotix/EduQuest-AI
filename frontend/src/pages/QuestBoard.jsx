import { useEffect, useMemo, useState } from 'react'

function FeedbackBlock({ feedback }) {
  if (!feedback) return null
  return (
    <div className={`feedback-box ${feedback.is_correct ? 'good' : 'warn'}`}>
      <strong>{feedback.is_correct ? 'Correct' : 'Needs revision'}</strong>
      <p>{feedback.rule_feedback}</p>
      <p><strong>Answer explanation:</strong> {feedback.llm_feedback}</p>
      <p>Mastery {feedback.mastery_before} → {feedback.mastery_after} · Level {feedback.level} · Coins {feedback.coins}</p>
    </div>
  )
}

function SubmissionCard({ item, onSubmit, typeLabel }) {
  const [form, setForm] = useState({ user_answer: '', confidence: 3, helpfulness: 3 })
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [startedAt, setStartedAt] = useState(Date.now())

  useEffect(() => {
    setStartedAt(Date.now())
    setShowHint(false)
    setFeedback(null)
    setForm({ user_answer: '', confidence: 3, helpfulness: 3 })
  }, [item.id])

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const result = await onSubmit(item.id, {
        ...form,
        hints_used: showHint ? 1 : 0,
        time_spent_sec: Math.round((Date.now() - startedAt) / 1000),
      })
      setFeedback(result)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="quest-card">
      <div className="quest-header">
        <div>
          <h3>{item.title}</h3>
          <p>{item.description || item.topic}</p>
        </div>
        <div className="pill-row">
          <span className="pill">{typeLabel}</span>
          <span className="pill">difficulty {item.difficulty}</span>
          {item.reward_coins && <span className="pill">+{item.reward_coins} coins</span>}
        </div>
      </div>
      <div className="prompt-text">{item.prompt}</div>
      <div className="button-row top-gap">
        <button type="button" className="secondary-btn" onClick={() => setShowHint((v) => !v)}>
          {showHint ? 'Hide hint' : 'Show hint'}
        </button>
      </div>
      {showHint ? <div className="info-box">{item.hint}</div> : null}
      <form className="quest-form" onSubmit={submit}>
        <label>
          Your answer
          <textarea rows="3" value={form.user_answer} onChange={(e) => setForm({ ...form, user_answer: e.target.value })} />
        </label>
        <div className="grid-2">
          <label>Confidence<input type="range" min="1" max="5" value={form.confidence} onChange={(e) => setForm({ ...form, confidence: Number(e.target.value) })} /><span className="range-value">{form.confidence}/5</span></label>
          <label>Helpfulness<input type="range" min="1" max="5" value={form.helpfulness} onChange={(e) => setForm({ ...form, helpfulness: Number(e.target.value) })} /><span className="range-value">{form.helpfulness}/5</span></label>
        </div>
        <button type="submit">{loading ? 'Submitting...' : 'Submit'}</button>
      </form>
      <FeedbackBlock feedback={feedback} />
    </div>
  )
}

export default function QuestBoard({ quests, onSubmit }) {
  const grouped = useMemo(() => {
    const result = {}
    quests.forEach((quest) => {
      if (!result[quest.track]) result[quest.track] = []
      result[quest.track].push(quest)
    })
    return result
  }, [quests])

  return (
    <div className="stack-list">
      {Object.entries(grouped).map(([track, items]) => (
        <section className="panel" key={track}>
          <h2>{track}</h2>
          <div className="stack-list">
            {items.map((item) => <SubmissionCard key={item.id} item={item} onSubmit={onSubmit} typeLabel="Quest" />)}
          </div>
        </section>
      ))}
    </div>
  )
}
