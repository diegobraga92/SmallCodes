#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <ctime>
#define MAX_ATRIBUICOES 10000000

int atribuicoes;
bool fc, mvr, grau;

// Função para checar se o valor é valido (ainda não existe na linha/coluna e não está em nenhuma restrição). Usado somente quando o FC está desativado
bool eh_valido(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, int posicao_atual, int dimensao, int numero_de_restricoes, int valor_proposto)
{
	// Checa se o valor já existe na mesma linha ou coluna e retorna false caso sim

	// Itera todas as posições da coluna atual, pegando a posição da coluna na linha 0 e incrementando o valor da dimensão (Ex: Para D = 4, na posição (1,4), faz: 3 -> 7 -> 11 -> 15)
	for (int linha = posicao_atual % dimensao; linha < (int)vetor_do_tabuleiro.size(); linha += dimensao)
	{
		if (linha != posicao_atual && vetor_do_tabuleiro[linha] == valor_proposto)
			return false;
	}

	// Itera todas as posições da linha atual, pegando a posição da linha na coluna 0 e incrementando 1 (Ex: Para D = 4, na posição (1,4), faz: 0 -> 1 -> 2 -> 3)
	int inicio_coluna = posicao_atual / dimensao;
	inicio_coluna *= dimensao;
	for (int coluna = inicio_coluna; coluna < inicio_coluna + dimensao; coluna++)
	{
		if (coluna != posicao_atual && vetor_do_tabuleiro[coluna] == valor_proposto)
			return false;
	}

	// Checa se a posição_atual está em alguma restrição, e retorna false se a restrição não estiver sendo atendida
	for (int restricao = 0; restricao < numero_de_restricoes; restricao++)
	{
		if (posicao_atual == vetor_de_restricoes[restricao])
		{
			// As restrições foram convertidas para posições e armazenadas na sequência, assim, todo indíce par armazena uma posição que deve ser menor que a posição armazenada no índice impar seguinte
			// Ex: [2] < [3], [5] > [4]
			if (restricao % 2 == 0)
			{
				if (vetor_do_tabuleiro[vetor_de_restricoes[restricao + 1]] != 0 && valor_proposto >= vetor_do_tabuleiro[vetor_de_restricoes[restricao + 1]])
					return false;
			}
			else
			{
				if (vetor_do_tabuleiro[vetor_de_restricoes[restricao - 1]] != 0 && valor_proposto <= vetor_do_tabuleiro[vetor_de_restricoes[restricao - 1]])
					return false;
			}
		}
	}

	return true;
}

// Atualiza o vetor_de_dominios, removendo todos os valores invalidos das celulas afetadas, e retorna false se algum dominio estiver vazio
bool atualiza_dominios(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, std::vector<std::vector<int> >& vetor_de_dominios, int posicao_atual, int dimensao, int numero_de_restricoes, int valor_proposto)
{
	// O vetor de domínio guarda 0 para cada um dos valores possíveis, e quando alguma restrição é encontrada, esse valor 0 é incrementado, se forma que seja possível realizar a operação reversa posteriormente
	// Os valores_propostos são mantidos com seus valores originais (1..D), por isso, para acessar a posição respectiva no domínio, é necessário usar [valor_proposto-1]
	bool sem_dominio_vazio = true;
	for (int linha = posicao_atual % dimensao; linha < (int)vetor_do_tabuleiro.size(); linha += dimensao)
	{
		if (vetor_do_tabuleiro[linha] == 0)
		{
			vetor_de_dominios[linha][valor_proposto-1]++;
			
			// Retorna false caso algum domínio fique com todos os valores acima de 0
			if (!std::any_of(vetor_de_dominios[linha].begin(), vetor_de_dominios[linha].end(), [](int i) {return i == 0; }))
				sem_dominio_vazio = false;
		}
	}

	int inicio_coluna = posicao_atual / dimensao;
	inicio_coluna *= dimensao;
	for (int coluna = inicio_coluna; coluna < inicio_coluna + dimensao; coluna++)
	{
		if (vetor_do_tabuleiro[coluna] == 0)
		{
			vetor_de_dominios[coluna][valor_proposto - 1]++;

			if (!std::any_of(vetor_de_dominios[coluna].begin(), vetor_de_dominios[coluna].end(), [](int i) {return i == 0; }))
				sem_dominio_vazio = false;
		}
	}
	
	// Caso a posição seja usada em alguma restrição, todos os valores inválidos são removidos do dominio da posição par
	for (int restricao = 0; restricao < numero_de_restricoes; restricao++)
	{
		if (posicao_atual == vetor_de_restricoes[restricao])
		{
			if (restricao % 2 == 0)
			{
				for (int valor_para_remover = 0; valor_para_remover < valor_proposto-1; valor_para_remover++)
				{
					vetor_de_dominios[vetor_de_restricoes[restricao + 1]][valor_para_remover]++;
				}
				
				if (!std::any_of(vetor_de_dominios[vetor_de_restricoes[restricao + 1]].begin(), vetor_de_dominios[vetor_de_restricoes[restricao + 1]].end(), [](int i) {return i == 0; }))
					sem_dominio_vazio = false;
			}
			else
			{
				for (int valor_para_remover = dimensao-1; valor_para_remover >= valor_proposto; valor_para_remover--)
				{
					vetor_de_dominios[vetor_de_restricoes[restricao - 1]][valor_para_remover]++;
				}

				if (!std::any_of(vetor_de_dominios[vetor_de_restricoes[restricao - 1]].begin(), vetor_de_dominios[vetor_de_restricoes[restricao - 1]].end(), [](int i) {return i == 0; }))
					sem_dominio_vazio = false;
			}
		}
	}

	return sem_dominio_vazio;
}

// Restaura o vetor_de_dominios, realizando a operação oposta à feita pela função atualiza_dominios
bool restaura_dominios(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, std::vector<std::vector<int> >& vetor_de_dominios, int posicao_atual, int dimensao, int numero_de_restricoes, int valor_proposto)
{
	for (int linha = posicao_atual % dimensao; linha < (int)vetor_do_tabuleiro.size(); linha += dimensao)
	{
		if (vetor_do_tabuleiro[linha] == 0)
			vetor_de_dominios[linha][valor_proposto - 1]--;
	}

	int inicio_coluna = posicao_atual / dimensao;
	inicio_coluna *= dimensao;
	for (int coluna = inicio_coluna; coluna < inicio_coluna + dimensao; coluna++)
	{
		if (vetor_do_tabuleiro[coluna] == 0)
			vetor_de_dominios[coluna][valor_proposto - 1]--;
	}

	for (int restricao = 0; restricao < numero_de_restricoes; restricao++)
	{
		if (posicao_atual == vetor_de_restricoes[restricao])
		{
			if (restricao % 2 == 0)
			{
				for (int valor_para_remover = 0; valor_para_remover < valor_proposto - 1; valor_para_remover++)
				{
					vetor_de_dominios[vetor_de_restricoes[restricao + 1]][valor_para_remover]--;
				}
			}
			else
			{
				for (int valor_para_remover = dimensao - 1; valor_para_remover >= valor_proposto; valor_para_remover--)
				{
					vetor_de_dominios[vetor_de_restricoes[restricao - 1]][valor_para_remover]--;
				}
			}
		}
	}

	return true;
}

// Itera por todas as posições, atualizando os domínios das posições que começam com valor diferente de 0
void inicializa_dominios(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, std::vector<std::vector<int> >& vetor_de_dominios, int dimensao, int numero_de_restricoes)
{
	for (int posicao = 0; posicao < (int)vetor_do_tabuleiro.size(); posicao++)
	{
		if (vetor_do_tabuleiro[posicao] != 0)
			atualiza_dominios(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, posicao, dimensao, numero_de_restricoes, vetor_do_tabuleiro[posicao]);
	}
}

// Função para selecionar qual a proxima posição. Retorna -1 se não encontrar nenhuma posição com 0 (tabuleiro completo)
int seleciona_proxima_posicao(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, std::vector<std::vector<int> >& vetor_de_dominios, int dimensao, int numero_de_restricoes)
{
	// Caso o MVR esteja ativado, seleciona a posição com o menor número de valores possíveis (menor domínio)
	if (mvr)
	{
		// Inicializa o contador de menor dominio com um valor impossível, para posterior verificação se nenhum valor foi encontrado
		int menor_dominio = dimensao + 1;
		int posicao_com_menor_dominio;

		for (int posicao = 0; posicao < (int)vetor_do_tabuleiro.size(); posicao++)
		{
			if (vetor_do_tabuleiro[posicao] == 0)
			{
				int tamanho_do_dominio = 0;

				// Se o FC estiver habilitado, é contada a quantidade de 0 encontrados no domínio de cada posição
				if (fc)
					tamanho_do_dominio = std::count(vetor_de_dominios[posicao].begin(), vetor_de_dominios[posicao].end(), 0);
				// Se o FC não estiver habilitado, ele itera por todas as posições, com todas as possibilidades (1..dimensao) para verificar qual menor dominio
				else
				{
					for (int valor_proposto = 1; valor_proposto <= dimensao; valor_proposto++)
					{
						if (eh_valido(vetor_do_tabuleiro, vetor_de_restricoes, posicao, dimensao, numero_de_restricoes, valor_proposto))
							tamanho_do_dominio++;
					}
				}
				//Se GRAU estiver habilitado, utiliza celulas com mais restrições(> ou < ) para desempatar
				if (grau && tamanho_do_dominio == menor_dominio)
				{
					int restricoes_da_posicao_atual = 0;
					int restricoes_da_posicao_nova = 0;

					for (int restricao = 0; restricao < numero_de_restricoes; restricao++)
					{
						if (posicao == vetor_de_restricoes[restricao])
							restricoes_da_posicao_nova++;

						if (posicao_com_menor_dominio == vetor_de_restricoes[restricao])
							restricoes_da_posicao_atual++;
					}

					if (restricoes_da_posicao_nova > restricoes_da_posicao_atual)
					{
						posicao_com_menor_dominio = posicao;
					}
				}
				else if (tamanho_do_dominio < menor_dominio)
				{
					menor_dominio = tamanho_do_dominio;
					posicao_com_menor_dominio = posicao;
				}
			}
		}

		// Se o valor do menor_dominio não foi alterado, nenhuma posição com valor 0 foi encontrada, sinalizando que o tabuleiro está completo
		if (menor_dominio == (dimensao + 1))
			return -1;

		return posicao_com_menor_dominio;
	}
	// Caso MVR esteja desativado, corre o tabuleiro e retorna a posição de qualquer valor 0 encontrado
	else
	{
		for (int posicao = 0; posicao < (int)vetor_do_tabuleiro.size(); posicao++)
		{
			if (vetor_do_tabuleiro[posicao] == 0)
				return posicao;
		}

		// Se nenhum valor foi encontrado, retorna -1, sinalizando que o tabuleiro está completo
		return -1;
	}
}

// Função recursiva usada para resolver o tabuleiro futoshiki
bool resolver_futoshiki(std::vector<int>& vetor_do_tabuleiro, std::vector<int>& vetor_de_restricoes, std::vector<std::vector<int> >& vetor_de_dominios, int dimensao, int numero_de_restricoes)
{
	int nova_posicao = seleciona_proxima_posicao(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, dimensao, numero_de_restricoes);
	
	if (nova_posicao == -1)
		return true;

	// Itera pelos valores que estão no dominio da nova_posição, caso o FC não esteja ativado, esse dominio sempre terá todas as possibilidades
	for (int valor_proposto = 1; valor_proposto <= (int)vetor_de_dominios[nova_posicao].size(); valor_proposto++)
	{
		// Retorna falso caso o número de atribuições tenha excedido o limite estabelecido
		if (atribuicoes > MAX_ATRIBUICOES) return false;

		// Caso o valor atual do domínio seja maior que 0, ele é considerado inválido e é pulado
		if (vetor_de_dominios[nova_posicao][valor_proposto-1] > 0)
			continue;

		// Se o FC não estiver habilitado, o vetor_de_dominios nunca é atualizado, assim sendo necessário fazer a verificação de validade para cada valor proposto
		if (!fc)
		{
			// Se o valor for inválido, ele é pulado
			if (!eh_valido(vetor_do_tabuleiro, vetor_de_restricoes, nova_posicao, dimensao, numero_de_restricoes, valor_proposto))
				continue;
		}

		// Atribui o valor proposto na posição, e incrementa o contado de atribuições
		vetor_do_tabuleiro[nova_posicao] = valor_proposto;
		atribuicoes++;
		
		// Se o FC estiver ativo, atualiza todos os domínios conforme a atribuição realizada, caso um domínio fique sem valores, restaura o domínio e pula o valor atual
		if (fc)
		{
			if (!atualiza_dominios(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, nova_posicao, dimensao, numero_de_restricoes, valor_proposto))
			{
				restaura_dominios(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, nova_posicao, dimensao, numero_de_restricoes, valor_proposto);
				continue;
			}
		}

		// Chama a função resolver_futoshiki, caso retorne true o tabuleiro foi completado com sucesso, caso retorne false, foi encontrado um dead-end e será necessário tentar outro valor
		if (resolver_futoshiki(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, dimensao, numero_de_restricoes))
			return true;
		else
		{
			if(fc) restaura_dominios(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, nova_posicao, dimensao, numero_de_restricoes, valor_proposto);
			continue;
		}
	}

	// Caso não tenha sido possível utilizar nenhum dos valores propostos, atribui 0 novamente na posição e retorna false
	vetor_do_tabuleiro[nova_posicao] = 0;

	return false;
}

int main(int argc, char* argv[])
{
	mvr = false;
	grau = false;
	fc = false;

	// Lê e habilita as heurísticas conforme as flags passadas
	for (int args = 1; args < argc; args++)
	{
		if (std::string(argv[args]) == "-fc")
			fc = true;
		if (std::string(argv[args]) == "-mvr")
			mvr = true;
		if (std::string(argv[args]) == "-grau")
			grau = true;
	}

	// Lê o número de casos
	int numero_de_casos;
	std::cin >> numero_de_casos;

	for (int n = 0; n < numero_de_casos; n++)
	{
		atribuicoes = 0;

		/*********************** Entrada de Valores ***********************/
		// Para simplificar o algoritmo, cada par linha+coluna é convertido em uma "posição", onde posicao == (linha-1) * dimensão + (coluna-1)

		// Lê a dimensão e o número de restrições desse caso
		int dimensao, numero_de_restricoes;
		std::cin >> dimensao >> numero_de_restricoes;

		// Lê os R casos de restrição e armazena em uma std::list, onde cada 2 posições representam uma restrição (ex: [0],[1] = 1º res)
		std::vector<int> vetor_de_restricoes(numero_de_restricoes * 2);
		for (int restricao = 0; restricao < (int)vetor_de_restricoes.size(); restricao++)
		{
			int linha_restricao, coluna_restricao;
			std::cin >> linha_restricao >> coluna_restricao;
			vetor_de_restricoes[restricao] = (linha_restricao - 1) * dimensao + (coluna_restricao - 1);
		}

		numero_de_restricoes *= 2;

		// Lê as D linhas com os valores iniciais do tabuleiro, e armazena em um vetor
		std::vector<int> vetor_do_tabuleiro(dimensao * dimensao);
		for (int linha = 0; linha < dimensao; linha++)
		{
			for (int coluna = 0; coluna < dimensao; coluna++)
				std::cin >> vetor_do_tabuleiro[linha * dimensao + coluna];
		}

		// Prepara um vetor com uma lista de dominio para cada uma das posições (Usado para FC)
		std::vector<std::vector<int> > vetor_de_dominios(dimensao*dimensao, std::vector<int>(dimensao));

		for (int posicao = 0; posicao < (int)vetor_do_tabuleiro.size(); posicao++)
		{
			for (int valor = 0; valor < dimensao; valor++)
				vetor_de_dominios[posicao][valor] = 0;
		}

		if(fc)
			inicializa_dominios(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, dimensao, numero_de_restricoes);

		/************************** Processamento *************************/

		std::clock_t inicio = clock();

		if (!resolver_futoshiki(vetor_do_tabuleiro, vetor_de_restricoes, vetor_de_dominios, dimensao, numero_de_restricoes))
		{
			if (atribuicoes >= MAX_ATRIBUICOES)
				std::cout << "Numero de atribuicoes excedeu " << MAX_ATRIBUICOES << "\n";
			else
				std::cout << "Nao existe solucao." << "\n";
		}
		std::clock_t fim = clock();
		double tempo_s = double(fim - inicio) / CLOCKS_PER_SEC;

		/*********************** Saída de Valores ***********************/

		// Escreve número do caso a qual essa saída se refere (1º caso = 1, 2º = 2...)
		std::cout << n + 1 << "\n";

		// Escreve os valores do tabuleiro completo
		for (int linha = 0; linha < dimensao; linha++)
		{
			std::cout << vetor_do_tabuleiro[linha * dimensao];
			for (int coluna = 1; coluna < dimensao; coluna++)
				std::cout << " " << vetor_do_tabuleiro[linha * dimensao + coluna];

			std::cout << "\n";
		}
		std::cout << "\n";
		//std::cout << "Atribuicoes: " << atribuicoes << "\n";
		//std::cout << "Tempo: " << tempo_s << "\n";
		
	}

	return 0;
}