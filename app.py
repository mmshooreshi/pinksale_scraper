from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import os
import subprocess
import threading
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")
basefolder = "INPUTS"

# def activate_venv():
#     activate_script = os.path.join(os.getcwd(), 'venv', 'bin', 'activate_this.py')
#     exec(open(activate_script).read(), dict(__file__=activate_script))

def stream_logs(process):
    for line in iter(process.stdout.readline, b''):
        socketio.emit('log', {'data': line.decode('utf-8').strip()})
    for line in iter(process.stderr.readline, b''):
        socketio.emit('log', {'data': line.decode('utf-8').strip()})
    process.stdout.close()
    process.stderr.close()
    process.wait()

def run_scrape_urls(include_weeks):
    # activate_venv()
    command = f'python scrape_urls.py "{include_weeks}"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stream_logs(process)

def run_scrape_new():
    # activate_venv()
    command = 'python scrape_new.py'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stream_logs(process)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    include_weeks = request.form['include_weeks']
    flash(f'Starting scrape for weeks: {include_weeks}')

    # Start the scrape_urls.py script in a separate thread
    thread = threading.Thread(target=run_scrape_urls, args=(include_weeks,))
    thread.start()
    thread.join()

    # After scrape_urls.py finishes, run scrape_new.py
    run_scrape_new()

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(basefolder):
        os.makedirs(basefolder)
    socketio.run(app, host='0.0.0.0', port=5000)
