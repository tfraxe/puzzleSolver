
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

	if (pos_dir) % 3 != 0:
		tab_direita = tabuleiro.copy()
		
		tab_direita[pos_dir], tab_direita[pos_vazio] = tab_direita[pos_vazio], tab_direita[pos_dir]
		
		tab_direita = "".join(tab_direita)

	if (pos_esq) % 3 != 2:
		tab_esquerda = tabuleiro.copy()
		
		tab_esquerda[pos_esq], tab_esquerda[pos_vazio] = tab_esquerda[pos_vazio], tab_esquerda[pos_esq]
		
		tab_esquerda = "".join(tab_esquerda)
	if (pos_cima) >= 0:
		tab_cima = tabuleiro.copy()
		print(tab_cima)
		tab_cima[pos_cima], tab_cima[pos_vazio] = tab_cima[pos_vazio], tab_cima[pos_cima]	
		
		tab_cima = "".join(tab_cima)
	if (pos_baixo) <= 8:
		tab_baixo = tabuleiro.copy()
		
		tab_baixo[pos_baixo], tab_baixo[pos_vazio] = tab_baixo[pos_vazio], tab_baixo[pos_baixo]
		
		tab_baixo = "".join(tab_baixo)

	return (tab_esquerda, pos_esq), (tab_direita, pos_dir), (tab_cima, pos_cima), (tab_baixo, pos_baixo)	




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

'''
Este conjunto irá guardar todos os tabuleiro que já foram explorados durante a busca. 
Não faz sentido "visitar" um tabuleiro já explorado, caso contrário entraríamos possivelmente num loop infinito
'''

tabuleiros_explorados = set()