import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'

export default function PublicShowcase() {
  const { userId } = useParams()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getPublicShowcase(userId).then(setData).catch((err) => setError(err.message || 'Unable to load showcase'))
  }, [userId])

  if (error) return <div className="content-wrap"><div className="panel">{error}</div></div>
  if (!data) return <div className="content-wrap"><div className="panel">Loading showcase...</div></div>

  return (
    <main className="content-wrap">
      <div className="page-grid">
        <section className="panel wide-span">
          <h1>{data.owner_name}'s EduQuest AI Showcase</h1>
          <p>{data.headline}</p>
        </section>
        <section className="panel wide-span">
          <div className="credential-grid">
            {data.achievements.map((item) => (
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
              </article>
            ))}
            {data.achievements.length === 0 && <p>No public credentials available yet.</p>}
          </div>
        </section>
      </div>
    </main>
  )
}
