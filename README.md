# EduQuest AI (React + FastAPI)

EduQuest AI is an learning platform implemented in the research paper **“Educational gamification and artificial intelligence for promoting digital literacy.”**

It includes:
- role-based login for learners and teachers
- quest board, quiz hub, exercise lab, and course pathways
- team challenges for collaborative learning
- teacher review queue with direct educator feedback and endorsements
- automatic timing and hint tracking
- coins that unlock bonus labs and case studies
- individual and team leaderboards
- shareable badge, endorsement, and certificate showcase pages
- grounded tutor with local RAG support

## Demo accounts
- `maya@student.demo` / `maya123`
- `leo@student.demo` / `leo123`
- `rivera@teacher.demo` / `teacher123`


## Backend
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

## models
For grounded tutoring and concise model explanations:
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

## Public showcase
Every learner has a public showcase page at:
```text
/showcase/<user_id>
```
