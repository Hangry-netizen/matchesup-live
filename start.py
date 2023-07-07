from app import app
import gsc_api

if __name__ == '__main__':
    # AWS connection
    serve(app, host='0.0.0.0', port=80)
    
    app.run()
