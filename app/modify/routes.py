from flask import Flask, Blueprint, request, abort, jsonify
from flask_cors import CORS
from ..main.models import db, Locations, Prefixes
from sqlalchemy import asc, desc, func, exc
from sqlalchemy.orm import load_only
from ..auth.auth import requires_auth

modify = Blueprint('modify', __name__)

CORS(modify, resources={r"/*": {"origins": "*"}})

@modify.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
  return response


@modify.route('/locations', methods=['POST'])
@requires_auth('add:location')
def add_location(payload):
    userinput = request.get_json()
    if 'name' not in userinput:
        abort(400)    
    try:
        new_location = Locations(name=userinput['name'])
        new_location.insert()
        query = Locations.query.all()
        locations = [loc.format() for loc in query]  
        success = True      
    except exc.IntegrityError as e:
        success = False
        locations = str(e.__cause__)
        db.session.rollback()
        abort(500)
    finally:
        return jsonify({
            'success': success,
            'locations': locations
        })


@modify.route('/prefixes', methods=['POST'])
@requires_auth('add:dsn')
def add_prefix(payload):
    userinput = request.get_json()
    if 'dsn_prefix' not in userinput:
        abort(400)
    dsn = userinput['dsn_prefix']
    if 'comm_prefix' not in userinput:
        abort(400)
    comm = userinput['comm_prefix']
    if 'location_id' not in userinput:
        abort(400)
    location = userinput['location_id']
    description = userinput['description']
    try:
        new_prefix = Prefixes(dsn_prefix=dsn)
        new_prefix.comm_prefix = comm
        new_prefix.description = description
        new_prefix.location_id = location
        new_prefix.insert()
        query = Prefixes.query.all()
        dsns = [dsn.format() for dsn in query]
        success = True
    except exc.IntegrityError as e:
        success = False
        dsns = str(e.__cause__)
        db.session.rollback()
        abort(500)
    finally:
        return jsonify({
            'success': success,
            'prefix_list': dsns
        })

@modify.route('/locations/<int:location_id>', methods=['PATCH'])
@requires_auth('update:location')
def update_location(payload, location_id):
    userinput = request.get_json()
    if 'name' not in userinput:
        abort(400)    
    try:
        query = Locations.query.filter(Locations.id == location_id).one_or_none()
        if query is not None:
            query.name = userinput['name']
            new_location = query.format()
            query.update()  
            success = True 
        else:
            new_location = "location not found"
            success = False
    except:
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'locations': new_location
        })

@modify.route('/prefixes/<int:prefix_id>', methods=['PATCH'])
@requires_auth('update:dsn')
def update_prefix(payload, prefix_id):
    userinput = request.get_json()
    print(userinput)
    if 'dsn_prefix' not in userinput:
        abort(400)
    dsn = userinput['dsn_prefix']
    if 'comm_prefix' not in userinput:
        abort(400)
    comm = userinput['comm_prefix']
    if 'location_id' not in userinput:
        abort(400)
    location = userinput['location_id']
    description = userinput['description']
    try:
        query = Prefixes.query.filter(Prefixes.id == prefix_id).one_or_none()
        if query is not None:
            query.dsn_prefix = dsn
            query.comm_prefix = comm
            query.description = description
            query.location_id = location
            new_prefix = query.format()
            query.update()
            success = True
        else:
            new_prefix = "prefix not found"
            success = False
    except:
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'prefix_list': new_prefix
        })

@modify.route('/locations/<int:location_id>', methods=['DELETE'])
@requires_auth('delete:location')
def delete_locations(payload, location_id):
    try:
        query = Locations.query.filter(Locations.id == location_id).one_or_none()
        if query is not None:
            removed = query.format()
            query.delete()
            success = True
        else:
            removed = "not found"
            success = False
    except:
        db.session.rollback()
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'location': removed
        })

@modify.route('/prefixes/<int:prefix_id>', methods=['DELETE'])
@requires_auth('delete:dsn')
def delete_prefixes(payload, prefix_id):
    try:
        query = Prefixes.query.filter(Prefixes.id == prefix_id).one_or_none()
        if query is not None:
            removed = query.format()
            query.delete()
            success = True
        else:
            removed = "not found"
            success = False
    except:
        db.session.rollback()
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'prefix': removed
        })

@modify.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()
