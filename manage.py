from main import create_app
from decouple import config

app = create_app(config('APP_ENV'))

if __name__ == '__main__':
    app.run()