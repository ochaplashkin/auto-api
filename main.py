import model
import generator
import client
import report

def main():
	'''
	The base architecture of script : pipe and filter
	+------------------+
	|      Model       |
	|                  |
	|  Read the config | (model.py) <<- /config/config.yml
	|  and input files |          
	| calc stats model |
	+------------------+
		   V
	+-----------------+
	|    Generator    |
	|                 |
	|create synthetic | (generator.py)
	|    requests     |
	|                 |
	+-----------------+
		   V
	+-----------------+
	|     Client      |
	|                 |
	|  send requests  | (client.py)
	|  	and process   |
	|   responses     |
	+-----------------+
		   V
	+-----------------+
	|     Report      |
	|                 |
	| create reports  | (report.py) ->> /reports/txt
	|    and html     |				   /reports/pic
	|   structure     |                /reports/index.html
	+-----------------+

	'''

	report.do(client.do(generator.do(model.do())))

if __name__ == '__main__':
	main()