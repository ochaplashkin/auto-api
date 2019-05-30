# Автоматизированная система тестирования API
#### Содержание
  - [Общее описание](https://github.com/ochaplashkin/auto-api/blob/master/README.md#%D0%BE%D0%B1%D1%89%D0%B5%D0%B5-%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)
  - [Установка и запуск](https://github.com/ochaplashkin/auto-api/blob/master/README.md#%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-%D0%B8-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA)
  - [Решение возможных проблем](https://github.com/ochaplashkin/auto-api#%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2%D0%BE%D0%B7%D0%BC%D0%BE%D0%B6%D0%BD%D1%8B%D1%85-%D0%BF%D1%80%D0%BE%D0%B1%D0%BB%D0%B5%D0%BC)
  - [Подробное описание функций](https://github.com/ochaplashkin/auto-api#%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D0%BE%D0%B5-%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B)
#### Общее описание
Система предназначена для автоматизированого тестирования конечных точек (API) с помощью  генерации тестовых запросов и создания отчетов о результатах проведенного тестирования. Предоставляет удобный для анализа сервиса и работы программы отчет в виде html страницы. 
###### Принцип работы
Система анализирует входной файл, состоящий из запросов к тестируемому сервису, расситывает статистическую модель, генерирует множество запросов, которое будет соответствовать статистическому распределению, посылает новые запросы на сервер и обрабатывает ответы, генерирует статистические отчеты либо в текстовом, либо в графическом формате.
#### Установка и запуск
Убедитесь, что у вас установлен Python, версии 3.7+
```sh
$ git clone https://github.com/ochaplashkin/auto-api.git
$ cd auto-api
$ pip3 install requirements.txt -r
```
Измените конфигурационный файл, используя [подробное описание](https://github.com/ochaplashkin/auto-api#%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D0%BE%D0%B5-%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B)
```sh
$ cd config
$ nano config.yml
```
Подготовьте входной файл в соответствии с требованиями:
- Формат файла: TXT
- Структура строк следующая: GET http:// ... 
- Символ разделения строк: '\n'
- Символ разделения данных в строке: ' ' (пробел)

> (!) Файл не должен содержать пустых строк

> (!) Файл не должен содержать знаков киррилицы

Перейдите в корневую папку проекта и запустите скрипт
```sh
$ cd ..
$ python3 main.py
```
#### Решение возможных проблем
#### Подробное описание системы
##### Модуль model.py
```python
def load_configuration(filename):
	"""
	Load a configuration parameters from *filename*. If there are any troubles 
	the display an error message and return empty dict

	:param filename: filename in YAML format
	:type filename: string
	
	:return: configuration parameters
	:rtype: dictionary
	"""
```
```python
def load_data(filename):
	"""
	Load a requests from *filename* and clear data from \n symbol
	If there are any troubles the display an error message and return empty list


	:param filename: filename in TXT format
	:type filename: string

	:return: list of requests without \n symbol
	:rtype: list of string
	"""
```
```python
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
```
```python
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
```
```python
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
```
##### Модуль generator.py
#####
```python
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
```
```python
def generate(data):
	'''
	Generate the requests with help the cartesian product

	:param data: dictionary that must contain info and stats keys
	:type data: dict

	:return: synthetic requests
	:rtype: dict
	'''
```
##### Модуль client.py
#####
```python
def process(data):
	'''
	Send requests from data['synthetic_req']['reqs'] and proccess the status code

	:param data: dictionary that must contain key 'synthetic_req' and assigned with this key values
	:type data: dict

	:return: responses and statistic by status code
	:rtype: dict

	'''
```
##### Модуль report.py
#####
```python
def txt_tree_visualize(data):
	'''
	Generate text report tree structure of service (ascii style)

	E.g:
			Node('/root')
			|-- Node('/root/sub0')
			|   |-- Node('/root/sub0/sub0B')
			|   +-- Node('/root/sub0/sub0A')
			+-- Node('/root/sub1')
	'''
```
```python
def img_tree_visualize(data):
	'''
	Render tree to filename

	:filename:  data['config']['review_base_filename'] + tree
	:format: png
	'''
```
```python
def txt_methods(data):
	'''
	Generate text report the distribution of methods(ascii style)

	Type: 
	E.g:
		GET: %%
		HEAD: %%
		POST: %%
		PUT: %%
		DELETE: %%
		UPDATE: %%

	'''
```
```python
def img_methods(data):
	'''
	Render pie diagram the distribution of methods to filename

	:filename:  data['config']['review_base_filename'] + pie_methods
	:format: png

	'''
```
```python
def txt_params_histogram(data):
	'''
	Generate text report the distribution of parametres in the requests(ascii style)

	E.g:
		parameter_name : the number of occurrences
		      . . .    :    .  .  . 
		      . . .    :    .  .  .

	'''
```
```python
def img_params_histogram(data):
	'''
	Render the histogram distribution of the parametres in the requests to filename

	:filename:  data['config']['review_base_filename'] + params_hist
	:format: png

	'''
```
```python
def txt_level_stats_histogram(data):
	'''
	Generate text report the distribution of nodes in the level(ascii style)

	E.g:
		node1 : percent(%)
		node2 : percent(%)
		node3 : percent(%)
		node4 : percent(%)
		. . . : . . . 
	'''
```
```python
def img_level_stats_histogram(data):
	'''
	Render the histogram distribution of nodes in the level to filename

	:filename:  data['config']['review_base_filename'] + level_nodes
	:format: png

	'''
```
```python
def html(data):
	'''
	Create html page

	Storage structure for html-page:

		root
		|-- config
		|
		|-- reports
		|	|
		|   |-- html_src ( source for the html page)
		|	|
		|	|-- txt
		|	|
		|	|-- pic
		|	|
		|   +-- index.html (start page of the report)
		|
		|-- script

	'''
```
```python
def txt_table(data):
	'''
	Generate text report the synthetic requests and status codes(ascii style)

	E.g: 
		1 https://host.com/a   200
		2 https://host.com/b   203
		3 https://host.com/c   200
		4 https://host.com/a/b 404
		5 https://host.com/f   500
	'''
```
