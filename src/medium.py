from flask import Flask

transient = Flask('down')

@transient.route('/set_routes/<string:gym>/<string:floorman>',methods=['GET','POST'])
def set_routes(gym, floorman):
	setting = request.get_data(as_text=True, cache=False)
	setting = RecObj(json.loads(setting))
	res = db.apply_setting(setting)
	return json.dumps({'success':res})

@transient.route('/follow/<string:route_id>/<string:user_id>',methods=['GET','POST'])
def follow(route_id, user_id):
	res = db.route[route_id].bind.follower(user_id)
	return json.dumps({'success':res})

@transient.route('/holla/<string:user_id>/<string:route_id>', methods=['GET','POST'])
def holla(user_id, route_id):
	res = db.holla[route_id](user_id)
	return json.dumps({'success':res})

