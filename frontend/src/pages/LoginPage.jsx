import { useState } from 'react'

export default function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('maya@student.demo')
  const [password, setPassword] = useState('maya123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await onLogin({ email, password })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-shell">
      <section className="login-card">
        <div>
          <h1>EduQuest AI</h1>
          <p className="subtitle">Gamified and AI-Supported Digital Learning Platform</p>
        </div>
        <form className="stack-list" onSubmit={submit}>
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <button type="submit">{loading ? 'Signing in...' : 'Sign in'}</button>
          {error && <div className="error-box">{error}</div>}
        </form>
      </section>
      <section className="login-side panel">
        <h3>Demo accounts</h3>
        <div className="stack-list">
          <div className="quest-mini"><strong>Maya</strong><span>maya@student.demo / maya123</span></div>
          <div className="quest-mini"><strong>Leo</strong><span>leo@student.demo / leo123</span></div>
          <div className="quest-mini"><strong>Dr. Rivera</strong><span>rivera@teacher.demo / teacher123</span></div>
        </div>
      </section>
    </div>
  )
}
