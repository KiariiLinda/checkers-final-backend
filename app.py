from app import create_app
from models import db

app = create_app()
@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
   app.run(debug=True,port=9000)
