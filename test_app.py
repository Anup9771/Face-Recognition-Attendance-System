from app import app

@app.route('/test')
def test():
    return "App is working!"

if __name__ == '__main__':
    app.run()
