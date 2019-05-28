from anytree import *
import yaml

def load_configuration(filename):
	"""
	Load a configuration parameters from *filename*. If there are any troubles 
	the display an error message and return empty dict

	:param filename: filename in YAML format
	:type filename: string
	
	:return: configuration parameters
	:rtype: dictionary
	"""
	with open(filename, 'r') as stream:
	    try:
	        return yaml.safe_load(stream)
	    except yaml.YAMLError as exc:
	        print("Error in load_configuration(): %s" % exc)
	        return {}

def load_data(filename):
	"""
	Load a requests from *filename* and clear data from \n symbol
	If there are any troubles the display an error message and return empty list


	:param filename: filename in TXT format
	:type filename: string

	:return: list of requests without \n symbol
	:rtype: list of string
	"""
	with open(filename,'r') as stream:
		try:
			d = []
			for i in stream:
				d.append(i.replace('\n',''))
			return d
		except Exception as exc:
			print("Error in load_data(): %s" % exc)
			return []
	return d

def parse_data(data):
	"""
	Parse data to the: total requests, protocol, type of method( get,post, etc.), 
	paths without hosts
	If there are any troubles the display an error message and return empty dictionary


	:param data: filename in TXT format
	:type data: string

	:return: cleared data
	:rtype: dict of dict
	"""
	def parse_url(url):
		"""
		Helper-function for url parsing

		:param url: raw data about url
		:type url: string

		:return: clear data
		:rtype: list of (dict,p)
		"""
		_buff = url.split('://') 
		protocol = _buff[0]
		host = _buff[1].split('/')[0]
		p =  _buff[1].replace(host+'/','')
		return [{
			'protocol':protocol,
			'host': host,
			},p]

	try:
		res = {}

		paths = []
		for row in data['requests']:
			_t = row.split(' ')
			req_type,body  = _t[0],_t[1]

			clear = parse_url(body)

			res['url'] = clear[0]
			paths.append(clear[1])

		return paths,res
	except Exception as exc:
		print("Error in parse_data(): %s" % exc)
		return {},{}

def build_tree(data):
	"""
	Parse the requests to API and builds a tree. The tree nodes are the nodes of the service API
	Use anytree library - https://anytree.readthedocs.io
	e.g.
		https://test.com/a
		https://test.com/b
		https://test.com/a/c
	tree:
			test.com
			/		\
			a 		 b
		   /
		  c
	If there are any troubles the display an error message and return empty dictionary


	:param paths: list of paths
	:type paths: list

	:return: tree of service
	:rtype: Node() class from AnyTree library
	"""
	try:

		#preprocess paths
		buff = []
		for i in data['paths']:
			buff.append(i.split('/'))

		used = set() #to avoid repetition

		parent = Node(data['config']['service_name']) #convenient structure from the anytree library
		parent_name = parent.name
		host = parent # for reset in the end cicle

		for path in buff:
			for level in path:

				if '?' in level or '=' in level: #cleaning nodes
					level = level.split('?')[0]

				is_exist_node = find_by_attr(parent,parent.name+'/'+level)

				if is_exist_node:
					parent = is_exist_node
				else:
					parent = Node(parent.name+'/'+level,parent=parent)

			#end for level
			parent = host
		#end for path
		return host
	except Exception as exc:
		print("Error in build_tree(): %s" % exc)
		return None

def calc_statistic(data):
	"""
	Calculation and construction of statistical model in the percentage ratio: count of requests,
	methods, parametres for each level  etc.

	:param data: dictionary that must contain key 'paths' and assigned with this key values
	:type data: dict

	:return: statistical model
	:rtype: dict
	"""

	def parse_params(path):
		"""
		Helper-function for parametres parsing

		:param path: raw path data
		:type path: string

		:return: pairs(k,v), k - param name, v - list of values
		:rtype: dict
		"""
		res = {}
		for i in path.split('?')[1:]:
			parsed_params = i.split('=')
			res[parsed_params[0]] = None
			if len(parsed_params) > 0:
				res[parsed_params[0]] = parsed_params[1:]
		return res

	try:

		res = {
			'count_requests' : len(data['requests']),
			'methods' : {
				'GET'    : 0,
				'HEAD'   : 0,
				'POST'   : 0,
				'PUT'    : 0,
				'DELETE' : 0,
				'UPDATE' : 0
			},
			'parametres':{},
			'level_stats':{}
		}

		#preprocess
		buff = []
		for i in data['paths']:
			buff.append(i.split('/'))
		for req in data['requests']:
			res['methods'][req.split(' ')[0]] += 1


		for r in res['methods']:
			try:
				res['methods'][r] = res['methods'][r]/res['count_requests']*100
			except ZeroDivisionError:
				res['methods'][r] = 0.0


		level_num = 0
		for path in buff:
			for level in path:

				level_key = str(level_num)

				if not (level_key in res['level_stats']):
					res['level_stats'][level_key] = {}

				params = {}
				if '?' in level or '=' in level:
					params = parse_params(level)
					level = level.split('?')[0]

					res['parametres'][level] = params

				if level in res['level_stats'][level_key]:
					res['level_stats'][level_key][level] += 1
				else:
					res['level_stats'][level_key][level] = 1
				
				level_num += 1
			#end for level
			level_num = 0
		#end for path

		for i in res['level_stats']:
			summ_ = 0
			for node in res['level_stats'][i]:
				try:
					res['level_stats'][i][node] = res['level_stats'][i][node]/res['count_requests']*100
					summ_ += res['level_stats'][i][node]
				except ZeroDivisionError:
					res['level_stats'][i][node] = 0.0
			if summ_ < 100.0:
				res['level_stats'][i]['END_'+str(int(i)+1)] = 100.0 - summ_
		return res
	except Exception as exc:
		print("Error in calc_statistic(): %s" % exc)
		return {}

def do():
	'''
	The main-function with the small unittest block

	:return: data that contain config,tree,etc.
	:rtype: dict

	'''
	data = {}

	data['config'] = load_configuration("config/config.yml")
	if data['config'] == {}:
		print('Test 0: Loading a configuration FAILED\n')

	data['requests'] = load_data(data['config']['input_file'])
	if data['requests'] == []:
		print("Test 1: Loading a data from ../config/request1.txt FAILED")


	data['paths'],data['info'] = parse_data(data)
	if data['paths'] == {} and data['info'] == {}:
		print("Test 2: Parsing data FAILED")


	data['tree'] = build_tree(data)
	if data['tree'] == None:
		print("Test 3: Building service tree FAILED")


	data['stats'] = calc_statistic(data)
	if data['stats'] == {}:
		print("Test 4: Calculation statistic FAILED")

	return data


if __name__ == '__main__':
	do()