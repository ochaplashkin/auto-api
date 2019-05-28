import requests

def process(data):
	'''
	Send requests from data['synthetic_req']['reqs'] and proccess the status code

	:param data: dictionary that must contain key 'synthetic_req' and assigned with this key values
	:type data: dict

	:return: responses and statistic by status code
	:rtype: dict

	'''
	try:
		info = {}
		info['responses'] = []
		info['total'] = {}
		for i in data['synthetic_req']['reqs']:
			r = requests.get(i) # (!) TODO
			code = r.status_code
			current_response = {
				'request' : i,
				'code'	  : r.status_code
				}
			info['responses'].append(current_response)

			if code in info['total']:
				info['total'][code] += 1
			else:
				info['total'][code] = 1
		return info
	except Exception as exc:
		print("Error in process(): %s" % exc)
		return {}


def do(data):
	'''
	The main-function with the small unittest block

	:return: data that contain server info
	:rtype: dict

	'''

	data['server'] = process(data)
	if data['server'] == {}:
		print("Test 1: Processing requests FAILED")

	return data

if __name__ == '__main__':
    do()