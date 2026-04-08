import { useEffect, useMemo, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { api, TOKEN_KEY } from './api'
import NavBar from './components/NavBar'
import LoginPage from './pages/LoginPage'
import StudentDashboard from './pages/StudentDashboard'
import QuestBoard from './pages/QuestBoard'
import QuizHub from './pages/QuizHub'
import ExerciseLab from './pages/ExerciseLab'
import CoursesPage from './pages/CoursesPage'
import CourseDetailPage from './pages/CourseDetailPage'
import Portfolio from './pages/Portfolio'
import Tutor from './pages/Tutor'
import Leaderboard from './pages/Leaderboard'
import TeacherDashboard from './pages/TeacherDashboard'
import PublicShowcase from './pages/PublicShowcase'
import TeamChallenges from './pages/TeamChallenges'
import TeacherReviewPage from './pages/TeacherReviewPage'

export default function App() {
  const [auth, setAuth] = useState({ token: localStorage.getItem(TOKEN_KEY), user: null })
  const [dashboard, setDashboard] = useState(null)
  const [courses, setCourses] = useState([])
  const [quests, setQuests] = useState([])
  const [quizzes, setQuizzes] = useState([])
  const [exercises, setExercises] = useState([])
  const [teamChallenges, setTeamChallenges] = useState([])
  const [showcase, setShowcase] = useState(null)
  const [teacherFeedback, setTeacherFeedback] = useState([])
  const [leaderboard, setLeaderboard] = useState([])
  const [teacherOverview, setTeacherOverview] = useState(null)
  const [loading, setLoading] = useState(true)

  const isTeacher = auth.user?.role === 'teacher'

  const bootstrap = async () => {
    if (!localStorage.getItem(TOKEN_KEY)) {
      setLoading(false)
      return
    }
    try {
      const user = await api.me()
      setAuth({ token: localStorage.getItem(TOKEN_KEY), user })
    } catch {
      localStorage.removeItem(TOKEN_KEY)
      setAuth({ token: null, user: null })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    bootstrap()
  }, [])

  const loadStudentData = async () => {
    const [dash, courseList, questList, quizList, exerciseList, teamList, showcaseData, feedbackData, board] = await Promise.all([
      api.getDashboard(),
      api.getCourses(),
      api.getQuests(),
      api.getQuizzes(),
      api.getExercises(),
      api.getTeamChallenges(),
      api.getShowcase(),
      api.getMyFeedback(),
      api.leaderboard(),
    ])
    setDashboard(dash)
    setCourses(courseList)
    setQuests(questList)
    setQuizzes(quizList)
    setExercises(exerciseList)
    setTeamChallenges(teamList)
    setShowcase(showcaseData)
    setTeacherFeedback(feedbackData)
    setLeaderboard(board)
    const freshUser = await api.me()
    setAuth((prev) => ({ ...prev, user: freshUser }))
  }

  const loadTeacherData = async () => {
    const [courseList, board, overview] = await Promise.all([api.getCourses(), api.leaderboard(), api.teacherOverview()])
    setCourses(courseList)
    setLeaderboard(board)
    setTeacherOverview(overview)
    const freshUser = await api.me()
    setAuth((prev) => ({ ...prev, user: freshUser }))
  }

  useEffect(() => {
    if (!auth.user) return
    setLoading(true)
    const fn = isTeacher ? loadTeacherData : loadStudentData
    fn().finally(() => setLoading(false))
  }, [auth.user?.id])

  const handleLogin = async (payload) => {
    const result = await api.login(payload)
    localStorage.setItem(TOKEN_KEY, result.token)
    setAuth({ token: result.token, user: result.user })
  }

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY)
    setAuth({ token: null, user: null })
    setDashboard(null)
    setTeacherOverview(null)
    setShowcase(null)
    setTeacherFeedback([])
  }

  const refreshAfterSubmit = async () => {
    if (isTeacher) {
      await loadTeacherData()
    } else {
      await loadStudentData()
    }
  }

  const handleQuestSubmit = async (questId, payload) => {
    const result = await api.submitQuest(questId, payload)
    await refreshAfterSubmit()
    return result
  }

  const handleQuizSubmit = async (quizId, payload) => {
    const result = await api.submitQuiz(quizId, payload)
    await refreshAfterSubmit()
    return result
  }

  const handleExerciseSubmit = async (exerciseId, payload) => {
    const result = await api.submitExercise(exerciseId, payload)
    await refreshAfterSubmit()
    return result
  }

  const handleTeamSubmit = async (challengeId, payload) => {
    const result = await api.submitTeamChallenge(challengeId, payload)
    await refreshAfterSubmit()
    return result
  }

  const handleUnlockBonus = async (courseSlug) => {
    const updatedUser = await api.unlockCourseBonus(courseSlug)
    setAuth((prev) => ({ ...prev, user: updatedUser }))
    await refreshAfterSubmit()
  }

  const content = useMemo(() => {
    if (!auth.user) {
      return (
        <Routes>
          <Route path="/showcase/:userId" element={<PublicShowcase />} />
          <Route path="*" element={<LoginPage onLogin={handleLogin} />} />
        </Routes>
      )
    }
    return (
      <div className="app-shell">
        <NavBar user={auth.user} onLogout={handleLogout} />
        <main className="content-wrap">
          <Routes>
            <Route path="/showcase/:userId" element={<PublicShowcase />} />
            {isTeacher ? (
              <>
                <Route path="/" element={<TeacherDashboard overview={teacherOverview} courses={courses} leaderboard={leaderboard} loading={loading} />} />
                <Route path="/feedback" element={<TeacherReviewPage />} />
                <Route path="/leaderboard" element={<Leaderboard entries={leaderboard} loading={loading} />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            ) : (
              <>
                <Route path="/" element={<StudentDashboard dashboard={dashboard} loading={loading} feedback={teacherFeedback} />} />
                <Route path="/quests" element={<QuestBoard quests={quests} onSubmit={handleQuestSubmit} />} />
                <Route path="/quizzes" element={<QuizHub quizzes={quizzes} courses={courses} onSubmit={handleQuizSubmit} />} />
                <Route path="/exercises" element={<ExerciseLab exercises={exercises} courses={courses} onSubmit={handleExerciseSubmit} />} />
                <Route path="/courses" element={<CoursesPage courses={courses} dashboard={dashboard} />} />
                <Route path="/courses/:slug" element={<CourseDetailPage courses={courses} onUnlockBonus={handleUnlockBonus} />} />
                <Route path="/teams" element={<TeamChallenges challenges={teamChallenges} onSubmit={handleTeamSubmit} teamName={auth.user.team_name} />} />
                <Route path="/portfolio" element={<Portfolio showcase={showcase} userId={auth.user.id} feedback={teacherFeedback} />} />
                <Route path="/tutor" element={<Tutor onAsk={api.tutorQuery} courses={courses} />} />
                <Route path="/leaderboard" element={<Leaderboard entries={leaderboard} loading={loading} />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            )}
          </Routes>
        </main>
      </div>
    )
  }, [auth.user, dashboard, courses, quests, quizzes, exercises, teamChallenges, showcase, teacherFeedback, leaderboard, teacherOverview, loading])

  if (loading && !auth.user) return <div className="splash-screen">Loading EduQuest AI...</div>
  return content
}
