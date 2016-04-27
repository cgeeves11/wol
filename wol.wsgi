import os, sys
 
activate_this = '/www/wol/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.append('/www/wol/wol')
 
from app import app as application

home='/www/wol/wol'
