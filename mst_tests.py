import random
from copy import copy
import os, sys

# nodes
class vertex:
	def __init__(self, name):
		self.name = name
		self.adj = dict()
		self.visited = False

# graph
class graph:
	def __init__(self, node_list):
		self.node_list = node_list
		self.nodes_order = list(self.node_list)
	
	def unvisit_all(self):
		for node in self.node_list:
			self.node_list[node].visited = False
	
	def get_connections(self):
		return {node: self.node_list[node].adj for node in self.node_list}

	# mst using prim's algorithm
	def prim_mst(self, start_node=None):
		if not start_node:
			curr_node = self.node_list[random.choice(list(self.node_list))]
		else:
			curr_node = self.node_list[self.nodes_order[start_node]]

		path = [curr_node.name]
		total = 0
		while set(path) != set(self.node_list):
			orphans = set(self.node_list) - set(path) # gets vertices not in graph
			edges_list = dict()
			for vert in path: # for verts already in path
				for conn_v in self.node_list[vert].adj:
					if conn_v in orphans: # if is connected to an orphan
						edges_list.update({(vert, conn_v): self.node_list[vert].adj[conn_v]}) # adds edge to edges list

			keys = list(edges_list)

			# finds smallest edge
			min_, edge = edges_list[keys[0]], keys[0]
			for key in keys:
				if edges_list[key] < min_:
					min_, edge = edges_list[key], key

			total += min_ # adds to total path
			path.append(edge[1])
			
		return path, total

# random graph generation functions
def pick_exclusive(seq, ks, n=1): # picks from set excluding certain elements
	assert n > 0
	for k in ks:
		seq.remove(k)
	return random.sample(seq, n)

# 65 - A to 90 - Z
def generate_random_graph(cnt=6): # generates a random graph
	if not 5 <= cnt <= 26:
		raise AssertionError("Only generates betweeen 5 and 26 vertices (inclusive)")
	vert_list = [chr(x) for x in range(65, 65+cnt)]
	nodes_dict = {v: vertex(v) for v in vert_list}

	# generating initial path

	nodes = list(nodes_dict)
	for i in range(len(nodes) - 1):
		rand_weight = random.randint(6, 10)
		nodes_dict[nodes[i]].adj.update({nodes[i+1]: rand_weight})
		nodes_dict[nodes[i+1]].adj.update({nodes[i]: rand_weight})

	for node in nodes_dict:
		if len(nodes_dict[node].adj) < 3:
			edge_cnt = 1 if len(nodes_dict[node].adj) == 1 else random.randint(1, 3)
			edges = pick_exclusive(copy(vert_list), [node] + list(nodes_dict[node].adj), edge_cnt) # picks edges not already in list and is not itself
			edges_weighted = {edge: random.randint(1, 7) for edge in edges} # assigns random weights to new edges
			nodes_dict[node].adj.update(edges_weighted) # appends said edges to adjacency list
			for vert in edges_weighted:
				nodes_dict[vert].adj.update({node: edges_weighted[vert]})

	return graph(nodes_dict)

# tests: this is from the example, generated path matches example
'''
gra = {'A': {'D': 3, 'B': 4, 'C': 1}, 'B': {'D': 3, 'C': 5, 'A': 4}, 'C': {'B': 5, 'D': 4, 'E': 2, 'A': 1}, 'D': {'C': 4, 'E': 1, 'B': 3, 'A': 3}, 'E': {'D': 1, 'C': 2}}

test1 = dict()
for n in gra:
	test1[n] = vertex(n)
	test1[n].adj = gra[n]

gr = graph(test1)
grc = gr.get_connections()
for c in grc:
	print(c, grc[c])

for i in range(len(gra)):
	print(gr.prim_mst(i))
'''

print_out = False
output_ans = True
findall = False
vertex_cnt = 6
sampsize = 1
output_dir = '.'
for arg in sys.argv:
	if arg == 'h' or arg == 'help':
		print('''
Automatically generates graphs and their MSTs (MST algo. is prim's algorithm, not the one asked)

python mst_tests.py [options]

options:
	printout - prints to terminal the output in addition to writing to file
	noanswer - do not output the answer to file
	findall - produce every single possible MST
	vertices=n - create tests with n vertices (n must be an integer)
	sampsize=n - create n samples (n must be integer)
	output_dir=dir - outputs files to dir directory (path is relative to mst_tests.py)

Example:
	python mst_tests.py printout output_dir=test_cases vertices=10
		''')
	if arg == 'printout':
		print_out = True
	elif arg == 'noanswer':
		output_ans = False
	elif arg == 'findall':
		findall = True
	else:
		arg_sep = arg.split('=')
		if arg_sep[0] == 'vertices':
			try:
				vertex_cnt = int(arg_sep[1])
			except ValueError:
				raise ValueError('Vertex count must be an integer')
		elif arg_sep[0] == 'sampsize':
			try:
				sampsize = int(arg_sep[1])
			except ValueError:
				raise ValueError('Sample size must be an integer')
		elif arg_sep[0] == 'output_dir':
			output_dir = arg_sep[1]
			print(output_dir)

for s in range(sampsize):
	with open(os.path.join(output_dir, 'graph{}.txt'.format(s+1)), 'w') as f:
		f.write('{}\n'.format(vertex_cnt))
		gr = generate_random_graph(vertex_cnt)
		connections = gr.get_connections()
		for c in connections:
			f.write('{}\n'.format(c))
		for c in connections:
			for c_n in connections[c]:
				f.write('{} {} {}\n'.format(c, c_n, connections[c][c_n]))
		
		if output_ans:
			if findall:
				for i in range(vertex_cnt):
					res, total = gr.prim_mst(i)
					f.write('{} - {}\n'.format(res, total))
			else:
				res, total = gr.prim_mst()
				f.write('{} - {}\n'.format(res, total))

		if print_out:
			print(connections)
			print(res)
