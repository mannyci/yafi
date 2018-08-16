from flask import Blueprint
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import logging
import json
import subprocess
import uuid
from threading import Timer
import threading
from time import sleep
import gevent
import os
import datetime

jobs = Blueprint('jobs', __name__)

# # Threading for the job
class myThread (threading.Thread):
    def __init__(self, cmd, job_id):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.job_id = job_id
    @jobs.route('/status', methods=['GET', 'POST'])
    def run(self):
        logfile = os.path.join('jobs', self.job_id + '.txt')
        start = datetime.datetime.now()
        with open(logfile, 'w+') as f:
            process = subprocess.Popen(self.cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
            timer = Timer(20, process.kill)
            # Kill long running process and return stdout
            try:
                timer.start()
                process.wait()
                print process.returncode
                end = datetime.datetime.now()
            finally:
                timer.cancel()
        runtime = unicode(end - start)
        print "Runtime:", runtime.split('.', 1)[0]


@jobs.route('/provision', methods=['GET', 'POST'])
def provision():
    if request.method == 'GET':
        return render_template('provision.html')
    elif request.method == 'POST':
        job_id = uuid.uuid4().hex[0:20]
        command = request.form['command']
        # result = comm.apply_async((command, job_id), )
        # cjob = celery.run(command, job_id)
        # print cjob
        logging.info("Job ID: %s for command: %s", job_id, command)
        th = myThread(command, job_id)
        try:
            th.start()
            result = 0
        except Exception as e:
            result = 1
            logging.error("Job ID: %s for command: %s", job_id, command)
        return json.dumps({'job_id': job_id, 'command': command, 'result': result})

@jobs.route('/stream')
def stream():
    if request.method == 'GET':
        if request.args:
            job_id =  request.args['job_id']
            def generator(job_id):
                print "JobID: ", job_id
                log = os.path.join('jobs', job_id + '.txt')
                f = open(log, 'r')
                for line in f.readlines():
                    yield line
            return Response(generator(job_id), mimetype= 'text/html' )
        else:
            return jsonify({'status': '400', 'response': 'Not valid request', 'error': 'Method not allowed'}), 400