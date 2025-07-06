cd backend-python-llm
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt

run
uvicorn api:app --reload --port 8000

test 
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Will ECB hike rates?", "session_id": "test1"}'

