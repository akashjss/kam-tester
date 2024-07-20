from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

KAMAILIO_CFG_PATH = '/usr/local/etc/kamailio/kamailio.cfg'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-header', methods=['POST'])
def add_header():
    header_name = request.form['headerName']
    header_value = request.form['headerValue']
    append_to_kamailio_cfg(f'append_hf("{header_name}: {header_value}\\r\\n");')
    return redirect(url_for('index'))

@app.route('/configure-destination', methods=['POST'])
def configure_destination():
    destination = request.form['destination']
    append_to_kamailio_cfg(f'set_destination("{destination}");')
    return redirect(url_for('index'))

@app.route('/topology-hiding', methods=['POST'])
def topology_hiding():
    topos_enabled = 'topos' in request.form
    if topos_enabled:
        append_to_kamailio_cfg('loadmodule "topos.so"\nmodparam("topos", "topos_mode", 1)')
    else:
        # Code to disable topology hiding (if necessary)
        pass
    return redirect(url_for('index'))

def append_to_kamailio_cfg(line):
    with open(KAMAILIO_CFG_PATH, 'a') as cfg_file:
        cfg_file.write(line + '\n')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

