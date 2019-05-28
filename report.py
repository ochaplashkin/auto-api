import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from anytree import *
from anytree.dotexport import RenderTreeGraph


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
	for pre, fill, node in RenderTree(data['tree']):
		print("%s%s" % (pre, node.name))

def img_tree_visualize(data):
	'''
	Render tree to filename

	:filename:  data['config']['review_base_filename'] + tree
	:format: png

	'''
	directory = data['config']['report_directory'] + "/img/"
	filename = directory+"%s_%s.png" % (data['config']['review_base_filename'],"tree")
	RenderTreeGraph(data['tree']).to_picture(filename)

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
	pass

def img_methods(data):
	'''
	Render pie diagram the distribution of methods to filename

	:filename:  data['config']['review_base_filename'] + pie_methods
	:format: png

	'''
	data_methods  = data['stats']['methods'].keys() 
	data_values = data['stats']['methods'].values()

	fig = plt.figure()

	plt.title('Распределение методов запроса к ' + data['config']['service_name'] + ' (%)')

	xs = range(len(data_methods))

	plt.pie( data_values, autopct='%.1f', radius = 1.1,
			    explode = [0.15] + [0 for _ in range(len(data_methods) - 1)] )
	plt.legend(loc = 'best', labels = data_methods )

	directory = data['config']['report_directory'] + "/img/"
	fig.savefig(directory+ "%s_%s.png" % (data['config']['review_base_filename'],"pie_methods"),bbox_inches='tight',dpi=100)
	fig.clf()

def txt_params_histogram(data):
	'''
	Generate text report the distribution of parametres in the requests(ascii style)

	E.g:
		parameter_name : the number of occurrences
		      . . .    :    .  .  . 
		      . . .    :    .  .  .

	'''
	pass

def img_params_histogram(data):
	'''
	Render the histogram distribution of the parametres in the requests to filename

	:filename:  data['config']['review_base_filename'] + params_hist
	:format: png

	'''
	s = set()

	clear_result = {}
	for k in data['stats']['parametres']:
		for i in data['stats']['parametres'][k]:
			if i in clear_result:
				clear_result[i] += 1
			else:
				clear_result[i] = 1

	fig = plt.figure()

	plt.bar(clear_result.keys(), clear_result.values())

	plt.title('Гистограмма параметров, входящие в запросы к %s' % data['config']['service_name'])

	plt.xlabel('Наименование параметра') 
	plt.xticks(rotation=30)
	plt.ylabel('Количество вхождений') 

	directory = data['config']['report_directory'] + "/img/"
	fig.savefig(directory + "%s_%s.png" % (data['config']['review_base_filename'],"params_hist"),bbox_inches='tight',dpi=100)
	fig.clf()

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
	pass

def img_level_stats_histogram(data):
	'''
	Render the histogram distribution of nodes in the level to filename

	:filename:  data['config']['review_base_filename'] + level_nodes
	:format: png

	'''
	colors = ['tab:blue','tab:orange','tab:green',
				'tab:red','tab:purple','tab:brown',
				'tab:pink','tab:gray','tab:olive',
				'tab:cyan']
	fig = plt.figure(figsize=(15,5))
	for level in data['stats']['level_stats']:
			level_name = str(int(level)+1) 

			barlist = plt.bar(data['stats']['level_stats'][level].keys(),
							data['stats']['level_stats'][level].values(),
							color=colors[int(level)],label="%s уровень" % level_name)

	plt.title('Гистограмма узлов API %s ' % data['config']['service_name'])

	plt.xlabel('Наименование узла \n\n') 
	plt.xticks(rotation=90)
	plt.legend(loc='best')
	plt.ylabel('Количество вхождений (%) \n\n')

	directory = data['config']['report_directory'] + "/img/"
	fig.savefig(directory+ "%s_%s.png" % (data['config']['review_base_filename'],"level_nodes"),bbox_inches='tight',dpi=100)
	fig.clf()

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
	table_body = '<tbody>'
	number = 1
	for i in data['server']['responses']:
		req = i["request"] 
		code = i["code"]
		class_type = "allow"
		if (code >= 100 and code <= 200) and (code >= 300 and code < 400):
			class_type = "challenged"
		if (code >= 400):
			class_type = "deny"
		table_body += '<tr class="{tclass}"><th scope="row">{n}</th><td>{request}</td><td>{response}</td></tr>'.format(tclass=class_type,n=str(number),request=req,response=str(code))
		number += 1
	table_body += '</tbody>'


	service_name = data['config']['service_name']

	prefix = "img/"

	tree = "%s_%s.png" % (data['config']['review_base_filename'],"tree")
	params = "%s_%s.png" % (data['config']['review_base_filename'],"params_hist")
	methods = "%s_%s.png" % (data['config']['review_base_filename'],"pie_methods")

	template = '''<!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <meta name="viewport" 
					content="width=device-width, initial-scale=1, shrink-to-fit=no"> <meta http-equiv="x-ua-compatible"
					content="ie=edge"> <title>Test report</title> <link rel="stylesheet" 
					href="https://use.fontawesome.com/releases/v5.8.1/css/all.css"> 
					<link href="html_src/css/bootstrap.min.css" rel="stylesheet"> 
					<link href="html_src/css/mdb.min.css" rel="stylesheet"> 
					<link href="html_src/css/style.min.css" rel="stylesheet">
					<link href="html_src/css/switching.css" rel="stylesheet"></head>
					<body class="grey lighten-3"> <header> <div class="sidebar-fixed position-fixed">
					<a class="logo-wrapper waves-effect"> <img class="img-fluid" alt=""> </a>
					<div class="list-group list-group-flush"> <a href="#" onclick="getOverview()"
					id="overview-btn" class="list-group-item waves-effect"> <i class="fas fa-chart-pie mr-3">
					</i>Обзор </a> <a href="#" onclick="getTable()" id="table-btn" class="list-group-item waves-effect">
					<i class="fas fa-table mr-3"></i>Таблица</a> </div></div></header> <main class="mx-lg-5">
					<div class="container-fluid" id="overview"> <div class=" wow fadeIn"> <div class="col-md-12 mb-4">
					<div class="card"> <div class="card-header">Древовидная структура API сервиса {service_name}</div>
					<div class="card-body"> <p><img id="overview-img" src="{tree_path}" width="100%" height="100%"></p>
					</div></div></div></div><div class="row wow fadeIn"> <div class="col-md-6 mb-4"> <div class="card">
					<div class="card-header"> Гистограмма параметров </div><div class="card-body"> <p><img src="{params_hist_path}"
					width="100%" height="100%"></p></div></div></div><div class="col-md-6 mb-4"> <div class="card">
					<div class="card-header"> Диаграмма распределения методов запроса </div><div class="card-body">
					<p><img src="{methods_path}" width="100%" height="100%"></p></div></div></div></div></div>
					<div class="container-fluid" id="table"> <div class="card"> <div class="card-body">
					<table class="table table-hover" > <thead class="blue-grey lighten-4"> <tr> <th>#</th>
					<th>Запрос</th> <th>Ответ</th></tr></thead>{tbody}</table> </div></div></div></main> <script type="text/javascript" src="html_src/js/jquery-3.4.0.min.js"></script> <script type="text/javascript" src="html_src/js/popper.min.js">
					</script> <script type="text/javascript" src="html_src/js/bootstrap.min.js"></script><script type="text/javascript" src="html_src/js/switching.js"></script></body></html>
					'''.format(service_name=service_name,tree_path=prefix+tree,
							params_hist_path=prefix+params,methods_path=prefix+methods,
							tbody=table_body)


	Html_file = open(data['config']['report_directory']+"/index.html","w")
	Html_file.write(template)
	Html_file.close()

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
	pass

		
def do(data):
	if data['config']['report_type'] == 'img':
		img_methods(data)
		img_params_histogram(data)
		img_tree_visualize(data)
		img_level_stats_histogram(data)
		html(data)
	else:
		txt_methods(data)
		txt_params_histogram(data)
		txt_tree_visualize(data)
		txt_level_stats_histogram(data)
		txt_table(data)

if __name__ == '__main__':
	do()