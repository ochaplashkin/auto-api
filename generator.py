from anytree import *
import numpy as np


def cart_product(lists):
	'''
	Cartesian product function

	:param lists: lists that should be multiplied
	:type lists: list of lists

	:return: list with cartesian product values
	:rtype: list 

	'''
	def lex_gen(bounds):
		'''
		Helper-function for the cartesian product

		:param bounds: 
		:type bounds: list of integer

		:return: 
		:rtype: list

		'''
		elem = [0] * len(bounds)
		while True:
			yield elem
			i = 0
			while elem[i] == bounds[i] - 1:
				elem[i] = 0
				i += 1
				if i == len(bounds):
					return
			elem[i] += 1

	bounds = [len(lst) for lst in lists]
	for elem in lex_gen(bounds):
		yield [lists[i][elem[i]] for i in range(len(lists))]


def generate(data):
	'''
	Generate the requests with help the cartesian product

	:param data: dictionary that must contain info and stats keys
	:type data: dict

	:return: synthetic requests
	:rtype: dict

	'''
	try:
		protocol = data['info']['url']['protocol']
		host = data['info']['url']['host']

		prefix = "%s://%s/" % (protocol,host)

		url_nodes = []
		for lvl in data['stats']['level_stats']:
			lvl_list = []
			for i in data['stats']['level_stats'][lvl].keys():
				if not 'END' in i:
					lvl_list.append(i)
			url_nodes.append(lvl_list)

		new_urls = []
		for i in range(len(url_nodes),0,-1):
			for k in cart_product(url_nodes[:i]):
				new_url = prefix
				
				for j in k:
					new_url += "%s/" % j

				new_urls.append(new_url)
		return {'reqs':new_urls,
				'count':len(new_urls)
				}
	except Exception as exc:
		print("Error in generate(): %s" % exc)
		return None
	
def do(data):
	'''
	The main-function with the small unittest block

	:return: data that contain synthetic requests
	:rtype: dict

	'''
	data['synthetic_req'] = generate(data)
	if data['synthetic_req'] == {}:
		print("Test 1: Generate data FAILED")

	return data


if __name__ == '__main__':
	do()