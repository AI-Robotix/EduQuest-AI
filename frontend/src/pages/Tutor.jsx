import { useState } from 'react'

export default function Tutor({ onAsk, courses }) {
  const [question, setQuestion] = useState('Why is a retrieval-grounded tutor useful in education?')
  const [courseSlug, setCourseSlug] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const result = await onAsk({ question, course_slug: courseSlug || null })
      setResponse(result)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-grid single-column">
      <section className="panel">
        <h2>Grounded tutor</h2>
        <p>Ask a course-related question. The tutor retrieves indexed notes and returns evidence with citations.</p>
        <form className="stack-list" onSubmit={submit}>
          <label>Course context<select value={courseSlug} onChange={(e) => setCourseSlug(e.target.value)}><option value="">All courses</option>{courses.map((course) => <option key={course.id} value={course.slug}>{course.title}</option>)}</select></label>
          <label>Question<textarea rows="4" value={question} onChange={(e) => setQuestion(e.target.value)} /></label>
          <button type="submit">{loading ? 'Asking...' : 'Ask tutor'}</button>
        </form>
      </section>
      {response && (
        <section className="panel">
          <div className="pill-row"><span className="pill">Mode: {response.mode}</span></div>
          <h3>Answer</h3>
          <p>{response.answer}</p>
          <h3>Citations</h3>
          <div className="stack-list">{response.citations.map((citation, idx) => <div className="quest-mini" key={`${citation.title}-${idx}`}><strong>{citation.title}</strong><span>{citation.source} · score {citation.score}</span></div>)}</div>
        </section>
      )}
    </div>
  )
}
