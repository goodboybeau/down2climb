from rec_obj import RecObj

class Setting(RecObj):
	def __call__(self, route):
		print 'setting',route
		if type(route) == list:
			self.routes = (route)
		else:
			self.routes.append(route)
		return self


	@property
	def gonners(self):
		gonners = filter((lambda r: r.state == Route.gonner), self.routes)
		print 'gonners:',gonners
		return gonners

	@property
	def newbies(self):
		newbies = filter((lambda r: r.state == Route.newbie), self.routes)
		print 'newbies:',newbies
		return newbies

	def at(self, gym):
		return gym(self)

class Gym(RecObj):
	
	def __call__(self, setting):
		self.take_down(setting.gonners)
		self.put_up(setting.newbies)
		return True

	@property
	def walls(self):
		self._walls = RecObj() if self._walls == None else self._walls
		return self._walls

	def take_down(self, routes):
		for route in routes:
			print 'taking down %s from %s' % (route, route.wall)
			self.walls[route.wall].remove(route)

	def put_up(self, routes):
		for route in routes:
			print 'putting %s up on %s' % (route, route.wall)
			self.walls[route.wall].add(route)

	def add_wall(self, wall):
		self.walls[wall] = wall

class Wall(RecObj):
	
	def __init__(self, name):
		self.name = name

	def __hash__(self):
		res = 0
		for n in str(self.name):
			res ^= int(hex(ord(n)),0)
		return res	

	def add(self, route):
		self.routes[route] = route

	def remove(self, route):
		self.routes.pop(route)

class Route(RecObj):
	newbie = 'newbie'
	gonner = 'gonner'
	
	def __str__(self):
		return '%s, %s' % (str(self.name), str(self.grade))

	@property
	def state(self):
		self._state = Route.newbie if self._state == None else self._state
		return self._state
	
	@property
	def wall(self):
		if self._wall == None:
			raise AssertionError('Routes are on walls')
		else:
			return self._wall

	@wall.setter
	def wall(self, wall):
		self._wall = wall

class Setter(RecObj):
	def set(self, routes):
		return Setting()(routes)	

class Grade(RecObj):
	BoulderGrade = 'boulder'
	TopRopeGrade = 'top rope'
	LeadGrade = 'lead'


if __name__ == '__main__':
	studio=Gym(name='The Studio')
	print studio
	g = Grade()
	g.kind = Grade.BoulderGrade
	g.top_level = 4
	
	r = Route(name='wickedy')
	r.grade = g
	r.wall = Wall('lead wall')
	these_routes = [r]
	eric = Setter()
	print 'Eric is about to set', these_routes, type(these_routes)
	try:
		print 'Eric set:',eric.set(these_routes).at(studio)
	except Exception as e:
		print 'Eric failed %s %s ' % (type(e), str(e))
		raise
	else:
		print 'Eric did it!'
	finally:
		print 'Eric',eric
		print 'routes', these_routes
		print 'studio',studio


	print r
