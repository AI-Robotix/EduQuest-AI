import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

function ExerciseCard({ item, onSubmit }) {
  const [form, setForm] = useState({ user_answer: '', confidence: 3, helpfulness: 3 })
  const [feedback, setFeedback] = useState(null)
  const [showHint, setShowHint] = useState(false)
  const [showSolution, setShowSolution] = useState(false)
  const [startedAt, setStartedAt] = useState(Date.now())

  useEffect(() => {
    setStartedAt(Date.now())
    setFeedback(null)
    setShowHint(false)
    setShowSolution(false)
    setForm({ user_answer: '', confidence: 3, helpfulness: 3 })
  }, [item.id])

  const submit = async (e) => {
    e.preventDefault()
    const result = await onSubmit(item.id, {
      ...form,
      hints_used: showHint ? 1 : 0,
      time_spent_sec: Math.round((Date.now() - startedAt) / 1000),
    })
    setFeedback(result)
  }

  return (
    <div className="quest-card">
      <div className="quest-header">
        <div>
          <h3>{item.title}</h3>
          <p>{item.topic}</p>
        </div>
        <div className="pill-row"><span className="pill">Exercise</span><span className="pill">difficulty {item.difficulty}</span><span className="pill">+{item.reward_coins} coins</span></div>
      </div>
      <div className="prompt-text">{item.prompt}</div>
      <div className="button-row top-gap">
        <button type="button" className="secondary-btn" onClick={() => setShowHint((v) => !v)}>{showHint ? 'Hide hint' : 'Show hint'}</button>
        <button type="button" className="secondary-btn" onClick={() => setShowSolution((v) => !v)}>{showSolution ? 'Hide answer' : 'Show answer'}</button>
      </div>
      {showHint && <div className="info-box">{item.hint}</div>}
      {showSolution && <div className="info-box">{item.solution}</div>}
      <form className="quest-form" onSubmit={submit}>
        <label>Your answer<textarea rows="3" value={form.user_answer} onChange={(e) => setForm({ ...form, user_answer: e.target.value })} /></label>
        <div className="grid-2">
          <label>Confidence<input type="range" min="1" max="5" value={form.confidence} onChange={(e) => setForm({ ...form, confidence: Number(e.target.value) })} /><span className="range-value">{form.confidence}/5</span></label>
          <label>Helpfulness<input type="range" min="1" max="5" value={form.helpfulness} onChange={(e) => setForm({ ...form, helpfulness: Number(e.target.value) })} /><span className="range-value">{form.helpfulness}/5</span></label>
        </div>
        <button type="submit">Submit exercise</button>
      </form>
      {feedback && <div className={`feedback-box ${feedback.is_correct ? 'good' : 'warn'}`}><p>{feedback.rule_feedback}</p><p><strong>Answer explanation:</strong> {feedback.llm_feedback}</p></div>}
    </div>
  )
}

export default function ExerciseLab({ exercises, courses, onSubmit }) {
  const [searchParams, setSearchParams] = useSearchParams()
  const [courseFilter, setCourseFilter] = useState(searchParams.get('courseId') || 'all')
  const [topicFilter, setTopicFilter] = useState(searchParams.get('topic') || 'all')
  const topics = [...new Set(exercises.map((item) => item.topic))]
  const filtered = exercises.filter((item) => (courseFilter === 'all' || String(item.course_id) === courseFilter) && (topicFilter === 'all' || item.topic === topicFilter))

  const syncCourse = (value) => {
    setCourseFilter(value)
    const next = new URLSearchParams(searchParams)
    value === 'all' ? next.delete('courseId') : next.set('courseId', value)
    setSearchParams(next)
  }

  const syncTopic = (value) => {
    setTopicFilter(value)
    const next = new URLSearchParams(searchParams)
    value === 'all' ? next.delete('topic') : next.set('topic', value)
    setSearchParams(next)
  }

  return (
    <div className="stack-list">
      <section className="panel filter-panel">
        <h2>Exercise Lab</h2>
        <div className="grid-3">
          <label>Course<select value={courseFilter} onChange={(e) => syncCourse(e.target.value)}><option value="all">All courses</option>{courses.map((course) => <option key={course.id} value={course.id}>{course.title}</option>)}</select></label>
          <label>Topic<select value={topicFilter} onChange={(e) => syncTopic(e.target.value)}><option value="all">All topics</option>{topics.map((topic) => <option key={topic} value={topic}>{topic}</option>)}</select></label>
          <div className="summary-box"><strong>{filtered.length}</strong><span>available lecturer exercises</span></div>
        </div>
      </section>
      {filtered.map((item) => <ExerciseCard key={item.id} item={item} onSubmit={onSubmit} />)}
    </div>
  )
}
