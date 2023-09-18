from graphviz import Digraph

dot = Digraph(format='png', engine='dot')
dot.attr(rankdir='LR')

dot.node('0', shape='circle', label='x0')
dot.node('1', shape='circle', label='x1')
dot.node('2', shape='circle', label='x2')
dot.node('3', shape='doublecircle', label='x3') # Aceptación

dot.edge('0', '1', 'a')
dot.edge('1', '2', 'a')
dot.edge('2', '3', 'a')
dot.edge('2', '3', 'b')
dot.edge('3', '3', 'a')
dot.edge('3', '3', 'b')

dot.render('automata', format='png')
