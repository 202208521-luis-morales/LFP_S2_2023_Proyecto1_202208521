from graphviz import Digraph

dot = Digraph(format='png', engine='dot')

dot.node('A', label='4.5')
dot.node('B', label='5.32')
dot.node('C', label='suma\n9.82')

dot.node('D', label='4.5')
dot.node('E', label='10')
dot.node('F', label='3')
dot.node('G', label='potencia\n1000')
dot.node('H', label='resta\n-995.5')

dot.edge('A', 'B')
dot.edge('A', 'C')
dot.edge('H', 'D')
dot.edge('H', 'G')
dot.edge('G', 'E')
dot.edge('G', 'F')

dot.render('automata', format='png')
