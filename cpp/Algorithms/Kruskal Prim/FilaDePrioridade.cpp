#include "FilaDePrioridade.h"

FilaDePrioridade::FilaDePrioridade(const std::vector<std::pair<double, int>> & vect_, const bool & filaMinima_) : vect(vect_), filaMinima(filaMinima_)
{
	criarHeap();
}

FilaDePrioridade::FilaDePrioridade()
{
	filaMinima = true;
}

FilaDePrioridade::~FilaDePrioridade()
{
}

// Insere o valor no final do vetor e faz bubbleUp até ficar valido
void FilaDePrioridade::push(const std::pair<double, int>& novoValor)
{
	vect.push_back(novoValor);
	bubbleUp(vect.size() - 1);
}

// Joga último valor pra raiz, remove o último valor, e faz bubbleDown até ficar valido
void FilaDePrioridade::pop()
{
	int size = vect.size();

	if (size == 0) return; 

	vect[0] = vect[size - 1];
	vect.pop_back();

	bubbleDown(0);
}


void FilaDePrioridade::criarHeap()
{
	int size = vect.size();
	for (auto ind = size - 1; ind >= 0; --ind)
	{
		bubbleDown(ind);
	}
}

// Verifica se o pai é valido, se não faz swap
void FilaDePrioridade::bubbleUp(const int& indice)
{
	if (indice == 0)
		return;

	int indicePai = (indice - 1) / 2;

	// Fila de Prioridade Mínima
	if (filaMinima)
	{
		if (vect[indicePai].first > vect[indice].first)
		{
			swap(indicePai, indice);
			bubbleUp(indicePai);
		}
	}
	// Fila de Prioridade Máxima
	else
	{
		if (vect[indicePai].first < vect[indice].first)
		{
			swap(indicePai, indice);
			bubbleUp(indicePai);
		}
	}
}

// Verifica se os filhos são validos, se não faz swap
void FilaDePrioridade::bubbleDown(const int& indice)
{
	int indiceFilhoEsquerda = 2 * indice + 1;
	int indiceFilhoDireita = 2 * indice + 2;

	int size = vect.size();
	if (indiceFilhoEsquerda >= size)	return; 

	// Fila de Prioridade Mínima
	if (filaMinima)
	{
		int indiceMin = indice;

		if (vect[indiceMin].first > vect[indiceFilhoEsquerda].first)
			indiceMin = indiceFilhoEsquerda;

		if ((indiceFilhoDireita < size) && (vect[indiceMin].first > vect[indiceFilhoDireita].first))
			indiceMin = indiceFilhoDireita;

		if (indiceMin != indice)
		{
			swap(indice, indiceMin);
			bubbleDown(indiceMin);
		}
	}
	// Fila de Prioridade Máxima
	else
	{
		int indiceMax = indice;

		if (vect[indiceMax].first < vect[indiceFilhoEsquerda].first)
			indiceMax = indiceFilhoEsquerda;

		if ((indiceFilhoDireita < size) && (vect[indiceMax].first > vect[indiceFilhoDireita].first))
			indiceMax = indiceFilhoDireita;

		if (indiceMax != indice)
		{
			swap(indice, indiceMax);
			bubbleDown(indiceMax);
		}
	}
}

void FilaDePrioridade::swap(const int & indice, const int & indice_)
{
	std::pair<double, int> temp = vect[indice];
	vect[indice] = vect[indice_];
	vect[indice_] = temp;
}