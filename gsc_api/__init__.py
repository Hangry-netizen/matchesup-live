from app import app
from flask_cors import CORS
import logging

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.getLogger('flask_cors').level = logging.DEBUG

## API Routes ##
from gsc_api.blueprints.admins.views import admins_api_blueprint
from gsc_api.blueprints.gscs.views import gscs_api_blueprint
from gsc_api.blueprints.sessions.views import sessions_api_blueprint
from gsc_api.blueprints.single_communities.views import single_communities_api_blueprint
from gsc_api.blueprints.references.views import references_api_blueprint
from gsc_api.blueprints.hellos.views import hellos_api_blueprint
from gsc_api.blueprints.reports.views import reports_api_blueprint

app.register_blueprint(admins_api_blueprint, url_prefix='/api/v1/admins')
app.register_blueprint(gscs_api_blueprint, url_prefix='/api/v1/gscs')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
app.register_blueprint(single_communities_api_blueprint, url_prefix='/api/v1/single-communities')
app.register_blueprint(references_api_blueprint, url_prefix='/api/v1/references')
app.register_blueprint(hellos_api_blueprint, url_prefix='/api/v1/hellos')
app.register_blueprint(reports_api_blueprint, url_prefix='/api/v1/reports')
