/*  Jacob
 *  DeRosa
 *  jderosa3
 */
#include <functional>
#include <algorithm>
#include <iostream>
#include <cuda_runtime.h>
#include <vector>
#include <numeric>
#include <cmath>

#ifndef A3_HPP
#define A3_HPP

float K(float x)
{
    return (1/(std::sqrt(2*M_PI)))*std::exp(-(x*x)/2);
}

void gaussian_kde(int n, float h, const std::vector<float>& x, std::vector<float>& y)
{
    #pragma omp parallel for default(none) shared(x, y, n, h)
    for (int i = 0; i < n; i++)
    {
        float xi = x[i];

        for (int j = 0; j < n; j++)
        {
            int xj = x[j];
            y[i] += K((xi - xj) / h);
        }
    }
}

#endif // A3_HPPd
