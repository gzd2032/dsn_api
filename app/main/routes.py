from flask import Blueprint, render_template, redirect, jsonify, abort, request, session
from flask_cors import CORS, cross_origin
from .models import db, Locations, Prefixes
from sqlalchemy import asc, desc, func, exc
from sqlalchemy.orm import load_only
from os import environ

main = Blueprint('main', __name__)

CORS(main, resources={r"/*": {"origins": "*"}})

@main.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
  return response

@main.route('/', methods=['GET'])
def index():
    if 'profile' in session:
        return render_template('index.html',
                               userinfo=session['profile'],
                               app_location=environ.get('APP_LOCATION'))
    return render_template('index.html')

@main.route('/locations', methods=['GET'])
def get_locations():
    try:
        query = Locations.query.all()
        locations = [loc.format() for loc in query]
    except:
        abort(500)
    finally:
        return jsonify({
            'locations': locations
        })

@main.route('/locations/<name>', methods=['GET'])
def get_location_details(name):
    try:
        query = Locations.query.filter(Locations.name.ilike(f'%{name}%')).all()
        if query is None:
            location = "error: unknown location"
            prefixes = "none"
        else:
            location = [loc.details() for loc in query]
    except:
        abort (400)
    finally:
        return jsonify({
            'locations': location
        })

@main.route('/prefixes', methods=['GET'])
def get_prefixes():
    try:
        query = Prefixes.query.order_by(Prefixes.dsn_prefix).all()
        dsns = {}
        for dsn in query:
            dsns[dsn.dsn_prefix] = dsn.comm_prefix + ":" + dsn.locations.name
    except:
        abort (500)
    finally:
        return jsonify({
            'prefix_list': dsns
        })

@main.route('/prefixes/dsn', methods=['GET'])
def get_dsn_list():
    try:
        query = Prefixes.query.all()
        dsns = [dsn.format() for dsn in query]
    except:
        abort (500)
    finally:
        return jsonify({
            'dsn': dsns
        })

@main.route('/prefixes/comm', methods=['GET'])
def get_comm_list():
    try:
        query = Prefixes.query.all()
        dsns = [{dsn.comm_prefix: dsn.dsn_prefix} for dsn in query]
    except:
        abort (500)
    finally:
        return jsonify({
            'comm': dsns
        })

@main.route('/prefixes/dsn/<dsn_prefix>', methods=['GET'])
def get_dsn_prefixes(dsn_prefix):
    try:
        query = Prefixes.query.filter(Prefixes.dsn_prefix.ilike(f'%{dsn_prefix}%')).all()
        dsns = [dsn.format() for dsn in query]
    except:
        abort (500)
    finally:
        return jsonify({
            'prefix_list': dsns
        })

@main.route('/prefixes/comm/<comm_prefix>', methods=['GET'])
def get_comm_prefixes(comm_prefix):
    try:
        query = Prefixes.query.filter(Prefixes.comm_prefix.ilike(f'%{comm_prefix}%')).all()
        comms = [comm.format() for comm in query]
    except:
        abort (500)
    finally:
        return jsonify({
            'prefix_list': comms
        })

