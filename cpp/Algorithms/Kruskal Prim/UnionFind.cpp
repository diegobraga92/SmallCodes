#include "UnionFind.h"

UnionFind::UnionFind(const int& n)
{
	vect = std::vector<int>(n);
	size = std::vector<int>(n);

	for (auto i = 0; i < n; i++)
	{
		vect[i] = i;
		size[i] = 1;
	}
}

UnionFind::~UnionFind()
{
}

// Encontra a raiz do indice x. Comprime o caminho enquanto faz a busca
int UnionFind::find(const int& x)
{
	int i = x;

	while (vect[i] != i)
	{
		vect[i] = vect[vect[i]];
		i = vect[i];
	}

	return i;
}

// Une os subconjuntos de x e y, favorecendo o maior
void UnionFind::Union(const int & x, const int & y)
{
	int raizX = find(x);
	int raizY = find(y);

	if (raizX == raizY) return;

	if (size[raizX] < size[raizY])
	{
		vect[raizX] = raizY;
		size[raizY] += size[raizX];
	}
	else
	{
		vect[raizY] = raizX;
		size[raizX] += size[raizY];
	}
}
