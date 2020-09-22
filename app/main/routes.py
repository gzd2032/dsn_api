from flask import Blueprint, render_template, redirect, jsonify, abort, request
from .models import db, Locations, Prefixes
from sqlalchemy import asc, desc, func

from werkzeug.exceptions import BadRequest

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
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

@main.route('/locations', methods=['POST'])
def add_location():
    userinput = request.get_json()
    if 'name' not in userinput:
        abort(400)    
    try:
        new_location = Locations(name=userinput['name'])
        new_location.insert()
        query = Locations.query.all()
        locations = [loc.format() for loc in query]        
    except:
        abort (500)
    finally:
        return jsonify({
            'locations': locations
        })

@main.route('/locations/<int:location_id>', methods=['PATCH'])
def update_location(location_id):
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

@main.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_locations(location_id):
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
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'prefix': removed
        })

@main.route('/prefixes', methods=['GET'])
def get_prefixes():
    try:
        query = Prefixes.query.all()
        dsns = [dsn.format() for dsn in query]
    except:
        abort (500)
    finally:
        return jsonify({
            'prefix_list': dsns
        })

@main.route('/prefixes/<int:prefix_id>', methods=['PATCH'])
def update_prefix(prefix_id):
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
        query = Prefixes.query.filter(Prefixes.id == prefix_id).one_or_none()
        if query is not None:
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

@main.route('/prefixes', methods=['POST'])
def add_prefix():
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
    except:
        abort (500)
    finally:
        return jsonify({
            'prefix_list': dsns
        })

@main.route('/prefixes/<int:prefix_id>', methods=['DELETE'])
def delete_prefixes(prefix_id):
    try:
        print(prefix_id)
        query = Prefixes.query.filter(Prefixes.id == prefix_id).one_or_none()
        if query is not None:
            removed = query.format()
            query.delete()
            success = True
        else:
            removed = "not found"
            success = False
    except:
        abort (500)
    finally:
        return jsonify({
            'success': success,
            'prefix': removed
        })

@main.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()
