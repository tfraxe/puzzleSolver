'''
------ TO-DO -------

1) Implementar função solucao(node): constrói a solução (sequência de movimentos necessários para atingir node)
a partir do nó passado como argumento

2) Implementar função que concretiza a busca em largura a partir de generic_search.

3) Implementar função que concretiza A* a partir de generic_search.
	3.1.) Implementar função heurística pecas_fora_lugar(estado)
	3.2.) Implementar função heurística dist_ate_objetivo(estado)   

'''



#Esta função verifica se o tabuleiro entrado é válido e retorna o índice do elemento 0
def tabuleiro_valido(tab):
	if len(tab) != 9:
		print(f"Tamanho inválido. Tabuleiro só pode ter 9 elementos!")
		return False, 0
	else:
		ocorrencias = {str(e) : [0, 0] for e in range(9)}
		for i, elemento in enumerate(tab):	
			try:
				ocorrencias[elemento][0] += 1
				ocorrencias[elemento][1] = i				
			except KeyError:
				print(f"{elemento} não pode ser um elemento do tabuleiro!")
				return False, 0

		for elemento in ocorrencias:
			if ocorrencias[elemento][0] != 1:
				print(f"Ocorrência do elemento {elemento} não pode ser {ocorrencias[elemento][0]}!")
				return False, 0
		return True, ocorrencias["0"][1]

#Esta função checa se a solução foi alcançada
def check_sol(tab):
	'''
	if tab[0] == "0":
		inicio = 1
	elif tab[8] == "0":
		inicio = 0
	else:
		return False
	'''
	indice = 1
	for elem in tab[:8]:  #inicio : (8+inicio)
		if elem != str(indice):
			return False
		indice += 1
	return True


'''
Esta função gera os próximos estados possíveis do tabuleiro a partir do estado dado como argumento.
Consideram-se aqui apenas os estados gerados a partir de um único movimento do elemento vazio.

Se pos(vazio) + 1 % 3 == 0, então não pode ir para direita.
Se pos(vazio) - 1 % 3 == 2, então não pode ir para esquerda. 
Se pos(vazio) - 3 < 0, então não pode ir para cima. 
Se pos(vazio) + 3 > 8, então não pode ir para baixo.

'''

def gerar_proximos(estado):
	tab_esquerda = []
	tab_direita  = []
	tab_cima     = []
	tab_baixo    = []

	pos_vazio = estado[1]
	tabuleiro = list(estado[0])

	pos_esq   = pos_vazio - 1
	pos_dir   = pos_vazio + 1
	pos_cima  = pos_vazio - 3
	pos_baixo = pos_vazio + 3

	retorno = []

	if (pos_dir) % 3 != 0:
		tab_direita = tabuleiro.copy()
		
		tab_direita[pos_dir], tab_direita[pos_vazio] = tab_direita[pos_vazio], tab_direita[pos_dir]
		
		tab_direita = "".join(tab_direita)

		estado_direita = (tab_direita, pos_dir)
		retorno.append( (estado_direita, 'D'))

	if (pos_esq) % 3 != 2:
		tab_esquerda = tabuleiro.copy()
		
		tab_esquerda[pos_esq], tab_esquerda[pos_vazio] = tab_esquerda[pos_vazio], tab_esquerda[pos_esq]
		
		tab_esquerda = "".join(tab_esquerda)
		
		estado_esquerda = (tab_esquerda, pos_esq)
		retorno.append( (estado_esquerda, 'E'))
	
	if (pos_cima) >= 0:
		tab_cima = tabuleiro.copy()

		tab_cima[pos_cima], tab_cima[pos_vazio] = tab_cima[pos_vazio], tab_cima[pos_cima]	
		
		tab_cima = "".join(tab_cima)

		estado_cima = (tab_cima, pos_cima)
		retorno.append( (estado_cima, 'C'))
	
	if (pos_baixo) <= 8:
		tab_baixo = tabuleiro.copy()
		
		tab_baixo[pos_baixo], tab_baixo[pos_vazio] = tab_baixo[pos_vazio], tab_baixo[pos_baixo]
		
		tab_baixo = "".join(tab_baixo)

		estado_baixo = (tab_baixo, pos_baixo)
		retorno.append( (estado_baixo, 'B'))

	return retorno

from collections import namedtuple
N = namedtuple("N", "custo estado pai action")
#Isto servirá apenas para garantir que as comparações na heap ocorram apenas entre os primeiros elementos de Node
class Node(N):
	def __lt__(self, other):
		return self[0] < other[0]

'''
Esta função implementa uma busca genérica.

Para busca em largura: fronteira é um OrderedDict e heur() sempre retorna 0. 
Um OrderedDict mantém a ordem das inclusões e garante um tempo médio O(1) para testes de pertinência.
Além disso, permite que façamos a remoção FIFO de elementos. Para garantir esse comportamento, vamos 
"embrulhar" a classe OrderedDict em uma outra que padroniza a remoção FIFO, sem nos obrigar a usar o argumento
posicional. 

Para A*: fronteira é um PQDict e heur() pode ser o número de peças fora de lugar ou a distância de manhattan
O PQDict permite que possamos atualizar os valores de uma fila de prioridades. As estruturas padrões de PQ do Python
não permitem isso. 

'''

def generic_search(estado_inicial, fronteira, heur):
	
	no_inicial = Node(custo=0, estado=estado_inicial, pai=(), action='')
	fronteira[no_inicial.estado[0]] = no_inicial
	'''
	Este conjunto irá guardar todos os tabuleiros que já foram explorados durante a busca. 
	Não faz sentido "visitar" um tabuleiro já explorado, caso contrário entraríamos possivelmente num loop infinito
	'''
	tabuleiros_explorados = set()

	while(True):
		tab, node = fronteira.popitem()
		if check_sol(tab):
			return solucao(node) #falta definir função solucao
		else:
			tabuleiros_explorados.add(tab)
			for estado, action in gerar_proximos(node.estado):
				novo_no = Node(custo=node.custo + 1 + heur(), estado=estado, pai=node, action=action)
				
				em_exp = estado[0] in tabuleiros_explorados
				em_frt = estado[0] in fronteira
				if ((not em_exp) and (not em_frt)) or (em_frt and (fronteira[estado[0]].custo > novo_no.custo)):
					fronteira[estado[0]] = novo_no #insere ou atualiza nó.

				'''
				if (estado[0] not in tabuleiros_explorados) and (estado[0] not in fronteira):
					fronteira[estado[0]] = novo_no #insere novo nó
				elif (estado[0] in fronteira) and (fronteira[estado[0]].custo > novo_no.custo):
					fronteira[estado[0]] = novo_no #atualiza nó.

				'''
			
			


valido = False
indice0 = 0
tabuleiro = ""

while (not valido):

	tabuleiro = input("Digite o estado inicial: ")
	valido, indice0 = tabuleiro_valido(tabuleiro)	
'''
O estado será representado por uma tupla (string, int) em que string representa o tabuleiro 
e int a posição do elemento 0 (espaço vazio)
'''
estado_inicial = (tabuleiro, indice0)
print(estado_inicial)
print(check_sol(tabuleiro))
print(gerar_proximos(estado_inicial))

