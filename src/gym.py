import unittest, random
from rec_obj import RecObj

class Setting(RecObj):
	def __call__(self, route):
		#print 'setting',route
		if type(route) == list:
			self.routes = (route)
		else:
			self.routes.append(route)
		return self


	@property
	def gonners(self):
		gonners = filter((lambda r: r.state == Route.gonner), self.routes)
		#print 'gonners:',gonners
		return gonners

	@property
	def newbies(self):
		newbies = filter((lambda r: r.state == Route.newbie), self.routes)
		#print 'newbies:',newbies
		return newbies

	def at(self, gym):
		return gym(self)

class Gym(RecObj):

	class Notification(RecObj):
		def when(self, event_type=None):
			self._reasons = [] if self._reasons == None else self._reasons
			if event_type is not None:
				self._reasons.append(event_type)
			return self._reasons

		def __call__(self, value):
			return value in self._reasons

	def __init__(self, name):
		self.name = name
	
	def __call__(self, setting):
		self.take_down(setting.gonners)
		self.put_up(setting.newbies)
		self.do_notifications(Setting)
		return True

	def take_down(self, routes):
		for route in routes:
			#print 'taking down %s from %s' % (route, route.wall)
			self.walls[route.wall()].pop(route)

	def put_up(self, routes):
		for route in routes:
			self.walls[route.wall()] = route

	def notify(self, climber):
		if climber not in self.__notifications.keys():
			self.__notifications[climber] = Notification()
		return self.__notifications[climber]

	def do_notifications(self, reason):
		def because(climber, reason):
			self.__notifications[climber].


class Wall(RecObj):
	
	def __init__(self, name):
		self.name = name

	def __hash__(self):
		print 'hashing'
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

	def __init__(self, name, grade=None):
		self.name = name
		if grade:
			self.grade = grade

		print 'new Route',self.name
	
	def __str__(self):
		return '%s, %s' % (str(self.name), str(self.grade))

	@property
	def state(self):
		self._state = Route.newbie if self._state == None else self._state
		return self._state
	
	def wall(self, wall=None):
		self._wall = wall or self._wall
		return self._wall

class Setter(RecObj):
	def __init__(self, name):
		self.name = name

	def set(self, routes):
		return Setting()(routes)	

class Grade(RecObj):
	BoulderGrade = 'boulder'
	BoulderRange = range(15)

	TopRopeGrade = 'top rope'
	LeadGrade = 'lead'

	RopeGradeRange = [range(5,15), ['a','b','c','d']]

	def __init__(self, kind, grade, subGrade=None):
		if kind in [Grade.TopRopeGrade, Grade.LeadGrade]:
			assert subGrade in Grade.RopeGradeRange[1]

		self.kind = kind
		self.grade = grade
		self.subGrade = subGrade

	@staticmethod
	def get_boulder_grade(g=None):
		return Grade(Grade.BoulderGrade, Grade.BoulderRange[ g or random.randint(0,len(Grade.BoulderRange))])
	
	@staticmethod
	def get_toprope_grade(g=None,subg=None):
		return Grade(Grade.TopRopeGrade, \
				g or random.choice(Grade.RopeGradeRange), \
				subg or random.choice(Grade.RopeGradeRange[1]))
	
	@staticmethod
	def get_lead_grade(g=None,subg=None):
		return Grade(Grade.LeadGrade, \
				g or random.choice(Grade.RopeGradeRange), \
				subg or random.choice(Grade.RopeGradeRange[1]))


class Climber(RecObj):
	def __init__(self,name):
		self.name = name

	def __hash__(self):
		print 'hashing'
		res = 0
		for n in str(self.name):
			res ^= int(hex(ord(n)),0)
		return res	

	def subscribe_to(self,gym):
		gym.notify(self).when(Setting)

	def hear_about(setting):
		print str(self), '\nheard about this setting:',str(setting)


class TestSettingRoutes(unittest.TestCase):
	def setUp(self):
		self.setter = Setter('Eric')
		self.gym = Gym('The Studio')
		self.subscriber = Climber('Larry')
		r = Route(name='wickedy',grade=Grade.get_boulder_grade())
		r.wall(Wall('lead wall'))
		self.routes = [r]

	def test_set_route(self):
		self.setter.set(self.routes).at(self.gym)

if __name__ == '__main__':
	unittest.main()
