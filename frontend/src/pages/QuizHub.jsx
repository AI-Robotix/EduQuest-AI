import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

function stripPromptOptions(prompt) {
  return prompt
    .split('\n')
    .filter((line) => !/^[A-D]\)/.test(line.trim()))
    .join('\n')
}

function optionLetter(option) {
  const match = option.match(/^([A-D])\)/i)
  return match ? match[1].toLowerCase() : option
}

function QuizCard({ item, onSubmit }) {
  const [form, setForm] = useState({ user_answer: '', confidence: 3, helpfulness: 3 })
  const [feedback, setFeedback] = useState(null)
  const [showHint, setShowHint] = useState(false)
  const [startedAt, setStartedAt] = useState(Date.now())

  const options = useMemo(() => {
    try {
      return item.options_json ? JSON.parse(item.options_json) : []
    } catch {
      return []
    }
  }, [item.options_json])

  useEffect(() => {
    setStartedAt(Date.now())
    setShowHint(false)
    setFeedback(null)
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
        <div className="pill-row">
          <span className="pill">Quiz</span>
          <span className="pill">difficulty {item.difficulty}</span>
          <span className="pill">+{item.reward_coins} coins</span>
        </div>
      </div>
      <div className="prompt-text">{options.length > 0 ? stripPromptOptions(item.prompt) : item.prompt}</div>
      <div className="button-row top-gap">
        <button type="button" className="secondary-btn" onClick={() => setShowHint((v) => !v)}>{showHint ? 'Hide hint' : 'Show hint'}</button>
      </div>
      {showHint ? <div className="info-box">{item.hint}</div> : null}
      <form className="quest-form" onSubmit={submit}>
        {options.length > 0 ? (
          <div className="options-list radio-list">
            {options.map((option) => (
              <label key={option} className="option-item">
                <input type="radio" name={`quiz-${item.id}`} checked={form.user_answer === optionLetter(option)} onChange={() => setForm({ ...form, user_answer: optionLetter(option) })} />
                <span>{option}</span>
              </label>
            ))}
          </div>
        ) : (
          <label>Your answer<input value={form.user_answer} onChange={(e) => setForm({ ...form, user_answer: e.target.value })} /></label>
        )}
        <div className="grid-2">
          <label>Confidence<input type="range" min="1" max="5" value={form.confidence} onChange={(e) => setForm({ ...form, confidence: Number(e.target.value) })} /><span className="range-value">{form.confidence}/5</span></label>
          <label>Helpfulness<input type="range" min="1" max="5" value={form.helpfulness} onChange={(e) => setForm({ ...form, helpfulness: Number(e.target.value) })} /><span className="range-value">{form.helpfulness}/5</span></label>
        </div>
        <button type="submit">Check answer</button>
      </form>
      {feedback && (
        <div className={`feedback-box ${feedback.is_correct ? 'good' : 'warn'}`}>
          <p>{feedback.rule_feedback}</p>
          <p><strong>Answer explanation:</strong> {feedback.llm_feedback}</p>
        </div>
      )}
    </div>
  )
}

export default function QuizHub({ quizzes, courses, onSubmit }) {
  const [searchParams, setSearchParams] = useSearchParams()
  const [courseFilter, setCourseFilter] = useState(searchParams.get('courseId') || 'all')
  const [topicFilter, setTopicFilter] = useState(searchParams.get('topic') || 'all')

  const topics = [...new Set(quizzes.map((item) => item.topic))]
  const filtered = quizzes.filter((item) => (courseFilter === 'all' || String(item.course_id) === courseFilter) && (topicFilter === 'all' || item.topic === topicFilter))

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
        <h2>Quiz Hub</h2>
        <div className="grid-3">
          <label>Course<select value={courseFilter} onChange={(e) => syncCourse(e.target.value)}><option value="all">All courses</option>{courses.map((course) => <option key={course.id} value={course.id}>{course.title}</option>)}</select></label>
          <label>Topic<select value={topicFilter} onChange={(e) => syncTopic(e.target.value)}><option value="all">All topics</option>{topics.map((topic) => <option key={topic} value={topic}>{topic}</option>)}</select></label>
          <div className="summary-box"><strong>{filtered.length}</strong><span>available quiz questions</span></div>
        </div>
      </section>
      {filtered.map((item) => <QuizCard key={item.id} item={item} onSubmit={onSubmit} />)}
    </div>
  )
}
