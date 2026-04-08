import { useMemo } from 'react'

function copyToClipboard(text) {
  navigator.clipboard?.writeText(text)
}

export default function Portfolio({ showcase, userId, feedback = [] }) {
  const shareUrl = useMemo(() => `${window.location.origin}/showcase/${userId}`, [userId])

  if (!showcase) return <div className="panel">Loading showcase...</div>

  return (
    <div className="page-grid">
      <section className="panel wide-span">
        <h2>Credential Showcase</h2>
        <p>Share earned badges, collaboration credentials, and teacher endorsements as proof of your learning progress.</p>
        <div className="credential-share-box">
          <div>
            <strong>Public showcase link</strong>
            <p>{shareUrl}</p>
          </div>
          <button className="secondary-btn" onClick={() => copyToClipboard(shareUrl)}>Copy share link</button>
        </div>
      </section>

      <section className="panel wide-span">
        <h3>Earned badges and certificates</h3>
        <div className="credential-grid">
          {showcase.achievements.map((item) => (
            <article className="credential-card" key={item.id}>
              <div className="pill-row">
                <span className="pill highlighted">{item.kind}</span>
                <span className="pill">{item.issuer}</span>
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <div className="credential-meta">
                <span><strong>Skill:</strong> {item.skill_tag.replaceAll('_', ' ')}</span>
                <span><strong>Issued:</strong> {item.issued_on}</span>
              </div>
              <button className="secondary-btn" onClick={() => copyToClipboard(`${window.location.origin}${item.share_path}`)}>Copy public credential link</button>
            </article>
          ))}
          {showcase.achievements.length === 0 && <p>No credentials earned yet. Complete quests, team challenges, quizzes, and exercises to unlock badges.</p>}
        </div>
      </section>

      <section className="panel wide-span">
        <h3>Teacher feedback and endorsements</h3>
        <div className="stack-list">
          {feedback.map((item) => (
            <div className="quest-mini readable-card" key={item.id}>
              <strong>{item.title}</strong>
              <span>{item.teacher_name} · {new Date(item.created_at).toLocaleDateString()}</span>
              <p>{item.comment}</p>
              {item.is_endorsement ? <span className="pill highlighted">Teacher endorsement</span> : null}
            </div>
          ))}
          {feedback.length === 0 ? <p>No teacher feedback yet. Collaborative submissions and review-queue items will appear here after educator comments.</p> : null}
        </div>
      </section>
    </div>
  )
}
