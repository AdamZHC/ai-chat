from flaskr import create_app
import sys
sys.path.append('./flaskr')
if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000,threaded=False)
