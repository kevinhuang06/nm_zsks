import os

from app import create_app

config_name = os.getenv('ALGO_CONFIG')
app = create_app('test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6566)