import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

token = str(os.getenv("token"))
admin_id = int(os.getenv("admin_id"))
db_auth = str(os.getenv("db_auth"))

I18N_DOMAIN = 'bottrpp'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

