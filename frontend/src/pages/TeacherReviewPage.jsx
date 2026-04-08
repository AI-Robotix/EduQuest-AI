import { useEffect, useState } from 'react'
import { api } from '../api'

function FeedbackComposer({ item, onSaved }) {
  const [comment, setComment] = useState('')
  const [isEndorsement, setIsEndorsement] = useState(false)
  const [saving, setSaving] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.sendTeacherFeedback({
        student_id: item.student_id,
        target_type: item.target_type,
        target_id: item.target_id,
        title: item.title,
        comment,
        is_endorsement: isEndorsement,
      })
      setComment('')
      setIsEndorsement(false)
      onSaved()
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="stack-list top-gap" onSubmit={submit}>
      <label>
        Feedback comment
        <textarea rows="3" value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Add concise educator feedback" />
      </label>
      <label className="checkbox-row">
        <input type="checkbox" checked={isEndorsement} onChange={(e) => setIsEndorsement(e.target.checked)} />
        <span>Mark as teacher endorsement</span>
      </label>
      <button type="submit" disabled={saving || !comment.trim()}>{saving ? 'Saving...' : 'Send feedback'}</button>
    </form>
  )
}

export default function TeacherReviewPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const result = await api.teacherReviewQueue()
      setItems(result)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  if (loading) return <div className="panel">Loading review queue...</div>

  return (
    <div className="page-grid single-column">
      <section className="panel">
        <h2>Teacher review queue</h2>
        <p>Give direct educator feedback on incorrect answers and collaborative submissions. Endorsements appear in the learner’s public showcase.</p>
      </section>
      {items.map((item) => (
        <section className="panel" key={`${item.target_type}-${item.target_id}`}>
          <div className="quest-header">
            <div>
              <h3>{item.title}</h3>
              <p>{item.student_name}{item.team_name ? ` · ${item.team_name}` : ''}</p>
            </div>
            <div className="pill-row">
              <span className="pill">{item.target_type}</span>
              <span className="pill">{item.status}</span>
              <span className="pill">feedback {item.existing_feedback}</span>
            </div>
          </div>
          <div className="info-box top-gap">
            <strong>Submitted answer</strong>
            <p>{item.submitted_answer}</p>
          </div>
          <FeedbackComposer item={item} onSaved={load} />
        </section>
      ))}
      {items.length === 0 ? <section className="panel"><p>No items currently need review.</p></section> : null}
    </div>
  )
}
