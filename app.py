from app import create_app

app = create_app()
@app.route('/')
def home():
    return 'Welcome to our checkers game backend!'

if __name__ == '__main__':
   app.run(debug=True,port=9000,host='0.0.0.0')
