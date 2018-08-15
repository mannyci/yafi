# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template, flash, jsonify
import psutil
import json
import gevent
import logging
import helpers


ui = Blueprint('ui', __name__)


# UI routes
@ui.route('/home')
def index():
    return render_template("index.html")

@ui.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
    info = helpers.make_info_dict(request)
    return render_template("dashboard.html", **info)

@ui.route('/util')
def sysutil():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            load = psutil.cpu_percent()
            vir_mem = psutil.virtual_memory().percent
            swap_mem = psutil.swap_memory().percent
            json_val = json.dumps({'load': load, 'vir': vir_mem, 'swap': swap_mem})

            try:
                ws.send(json_val)
                gevent.sleep(2)
            except Exception as e:
                # Socket was probably closed by the browser changing pages
                logging.debug(e)
                ws.close()
                break
        return ''
    else:
        return jsonify({'status': '400', 'response': 'Not valid request', 'error': 'Method not allowed'}), 400