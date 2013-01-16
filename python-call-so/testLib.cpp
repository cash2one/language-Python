#include <stdio.h>
#include "testLib.h"

CTestLib::CTestLib()
{
}

CTestLib::~CTestLib()
{
}
	
int CTestLib::sum(int a, int b)
{
	int result = a + b;
	show(result);
	return result;
}

void CTestLib::show(int value)
{
	printf("[class] result: %d\n", value);
}

extern "C" {
	CTestLib obj;

	int sum(int a, int b)
	{
		return obj.sum(a, b);
	}
}

