const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
const TOKEN_KEY = 'eduquest_token'

function getHeaders(extra = {}) {
  const token = localStorage.getItem(TOKEN_KEY)
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...extra,
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: getHeaders(options.headers || {}),
    ...options,
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || 'Request failed')
  }
  return response.json()
}

export { TOKEN_KEY }

export const api = {
  login: (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  me: () => request('/auth/me'),
  getDashboard: () => request('/dashboard/me'),
  getCourses: () => request('/courses'),
  unlockCourseBonus: (courseSlug) => request(`/courses/${courseSlug}/unlock-bonus`, { method: 'POST' }),
  getQuests: () => request('/quests'),
  submitQuest: (questId, payload) => request(`/quests/${questId}/submit`, { method: 'POST', body: JSON.stringify(payload) }),
  getQuizzes: (courseId, topic) => {
    const params = new URLSearchParams()
    if (courseId) params.set('course_id', courseId)
    if (topic) params.set('topic', topic)
    return request(`/quizzes${params.toString() ? `?${params.toString()}` : ''}`)
  },
  submitQuiz: (quizId, payload) => request(`/quizzes/${quizId}/submit`, { method: 'POST', body: JSON.stringify(payload) }),
  getExercises: (courseId, topic) => {
    const params = new URLSearchParams()
    if (courseId) params.set('course_id', courseId)
    if (topic) params.set('topic', topic)
    return request(`/exercises${params.toString() ? `?${params.toString()}` : ''}`)
  },
  submitExercise: (exerciseId, payload) => request(`/exercises/${exerciseId}/submit`, { method: 'POST', body: JSON.stringify(payload) }),
  getTeamChallenges: () => request('/team-challenges'),
  submitTeamChallenge: (challengeId, payload) => request(`/team-challenges/${challengeId}/submit`, { method: 'POST', body: JSON.stringify(payload) }),
  getTeamLeaderboard: () => request('/team-leaderboard'),
  getShowcase: () => request('/portfolio/showcase'),
  getPublicShowcase: (userId) => request(`/showcase/${userId}`, { headers: {} }),
  listPortfolio: () => request('/portfolio/me'),
  createPortfolio: (payload) => request('/portfolio', { method: 'POST', body: JSON.stringify(payload) }),
  getMyFeedback: () => request('/teacher-feedback/me'),
  teacherOverview: () => request('/teacher/overview'),
  teacherReviewQueue: () => request('/teacher/review-queue'),
  sendTeacherFeedback: (payload) => request('/teacher/feedback', { method: 'POST', body: JSON.stringify(payload) }),
  tutorQuery: (payload) => request('/tutor/query', { method: 'POST', body: JSON.stringify(payload) }),
  leaderboard: () => request('/leaderboard'),
}
