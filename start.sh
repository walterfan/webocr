#source venv/bin/activate
cd frontend
mkdir -p static/uploads

PORT=$1
if [ x${PORT} == x"" ]; then
    PORT=8000
fi

flask --app app --debug run -p $PORT