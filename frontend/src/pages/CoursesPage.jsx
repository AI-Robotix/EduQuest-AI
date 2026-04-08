import { Link } from 'react-router-dom'

export default function CoursesPage({ courses, dashboard }) {
  const recommendedIds = new Set((dashboard?.recommended_courses || []).map((course) => course.id))

  return (
    <div className="page-grid">
      {courses.map((course) => (
        <section className="panel course-card" key={course.id}>
          <div className="pill-row">
            <span className="pill">{course.category}</span>
            <span className="pill">{course.level}</span>
            <span className="pill">{course.duration}</span>
            {recommendedIds.has(course.id) && <span className="pill highlighted">recommended</span>}
          </div>
          <h2>{course.title}</h2>
          <p>{course.description}</p>
          <div>
            <strong>Learning outcomes</strong>
            <p>{course.learning_outcomes}</p>
          </div>
          <div className="course-actions">
            <Link className="secondary-btn" to={`/courses/${course.slug}`}>Go to course</Link>
            <Link className="secondary-btn" to={`/quizzes?courseId=${course.id}`}>Quizzes</Link>
            <Link className="secondary-btn" to={`/exercises?courseId=${course.id}`}>Exercises</Link>
          </div>
          {course.bonus_reward_cost ? (
            <p className="coin-note">Bonus lab unlock: {course.bonus_reward_cost} coins</p>
          ) : null}
        </section>
      ))}
    </div>
  )
}
