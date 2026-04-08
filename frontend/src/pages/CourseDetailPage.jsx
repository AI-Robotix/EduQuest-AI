import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

function LessonView({ lesson }) {
  if (!lesson) return <p>Select a lesson to view the content.</p>
  return (
    <div className="lesson-view">
      <h3>{lesson.title}</h3>
      <span className="lesson-topic">{lesson.topic}</span>
      <p>{lesson.summary}</p>
      <div className="info-box"><strong>Lesson content</strong><p>{lesson.content}</p></div>
      {lesson.key_points?.length ? (
        <div className="lesson-section">
          <strong>Key points</strong>
          <ul>
            {lesson.key_points.map((point) => <li key={point}>{point}</li>)}
          </ul>
        </div>
      ) : null}
      {lesson.activity ? (
        <div className="lesson-section">
          <strong>Practice activity</strong>
          <p>{lesson.activity}</p>
        </div>
      ) : null}
    </div>
  )
}

export default function CourseDetailPage({ courses, onUnlockBonus }) {
  const { slug } = useParams()
  const [error, setError] = useState('')
  const [unlocking, setUnlocking] = useState(false)
  const course = courses.find((item) => item.slug === slug)

  const lessons = useMemo(() => {
    try {
      return course?.lessons_json ? JSON.parse(course.lessons_json) : []
    } catch {
      return []
    }
  }, [course])
  const [selectedLessonIndex, setSelectedLessonIndex] = useState(0)

  if (!course) return <div className="panel">Course not found.</div>

  const unlock = async () => {
    setError('')
    setUnlocking(true)
    try {
      await onUnlockBonus(course.slug)
    } catch (err) {
      setError(err.message || 'Unable to unlock bonus module.')
    } finally {
      setUnlocking(false)
    }
  }

  const selectedLesson = lessons[selectedLessonIndex] || lessons[0]

  return (
    <div className="page-grid">
      <section className="panel wide-span">
        <div className="pill-row">
          <span className="pill">{course.category}</span>
          <span className="pill">{course.level}</span>
          <span className="pill">{course.duration}</span>
          {course.bonus_unlocked ? <span className="pill highlighted">bonus unlocked</span> : null}
        </div>
        <h2>{course.title}</h2>
        <p>{course.description}</p>
        <p><strong>Learning outcomes:</strong> {course.learning_outcomes}</p>
        <div className="course-actions">
          <Link className="secondary-btn" to={`/quizzes?courseId=${course.id}`}>Go to quizzes</Link>
          <Link className="secondary-btn" to={`/exercises?courseId=${course.id}`}>Go to exercises</Link>
          <Link className="secondary-btn" to="/courses">Back to courses</Link>
        </div>
      </section>

      <section className="panel">
        <h3>Course roadmap</h3>
        <div className="stack-list lesson-list">
          {lessons.map((lesson, index) => (
            <button
              key={lesson.title}
              type="button"
              className={`lesson-item ${index === selectedLessonIndex ? 'active' : ''}`}
              onClick={() => setSelectedLessonIndex(index)}
            >
              <strong>{lesson.title}</strong>
              <span>{lesson.topic}</span>
              <p>{lesson.summary}</p>
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <LessonView lesson={selectedLesson} />
      </section>

      <section className="panel wide-span">
        <h3>Bonus lab</h3>
        {course.bonus_module_title ? (
          course.bonus_unlocked ? (
            <div className="quest-mini unlocked-box">
              <strong>{course.bonus_module_title}</strong>
              <p>{course.bonus_module_content}</p>
            </div>
          ) : (
            <div className="quest-mini locked-box">
              <strong>{course.bonus_module_title}</strong>
              <p>{course.bonus_module_content}</p>
              <p><strong>Unlock cost:</strong> {course.bonus_reward_cost} coins</p>
              <button onClick={unlock} disabled={unlocking}>{unlocking ? 'Unlocking...' : 'Redeem coins to unlock'}</button>
              {error ? <p className="error-text">{error}</p> : null}
            </div>
          )
        ) : <p>No bonus lab configured for this course.</p>}
      </section>
    </div>
  )
}
