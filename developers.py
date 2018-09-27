from app import app
from config import host, port
app.run(host=host, port=port, debug=True)
