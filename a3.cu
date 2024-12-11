#include "a3.hpp"
#include <numeric>

__device__ float K(float x)
{
    return (1/(sqrtf(2*M_PI)))*expf(-(x*x)/2);
}

__global__ void kde_kernel(const float *x, float *y, int n, int h, float k)
{
    int bx = blockIdx.x;
    int idx = blockDim.x * bx + threadIdx.x;

    if (idx < n)
    {
        float xi = x[idx];

        for (int j = 0; j < n; j++)
        {
            int xj = x[j];
            y[idx] += K((xi - xj) / h);
        }
    }
}

void gaussian_kde(int n, float h, const std::vector<float>& x, std::vector<float>& y) {

    cudaDeviceProp device_prop;
    cudaGetDeviceProperties(&device_prop, 0);

    int threadsPerBlock = int(h);

    h = 0.01;

    int xblocks = (n + threadsPerBlock - 1)/ threadsPerBlock;
   
    float *d_x, *d_y;

    cudaMalloc(&d_x, sizeof(float)*n);
    cudaMemcpy(d_x, x.data(), n*sizeof(float), cudaMemcpyHostToDevice);

    cudaMalloc(&d_y, sizeof(float)*n);
    
    float k = 1/(n*h);
    
    cudaDeviceSynchronize();    

    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "CUDA error: " << cudaGetErrorString(err) << std::endl;
    }

    kde_kernel<<<xblocks, threadsPerBlock, threadsPerBlock*sizeof(float)>>>(d_x, d_y, n, h, k);

    cudaDeviceSynchronize();

    err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "CUDA error: " << cudaGetErrorString(err) << std::endl;
    }

    cudaMemcpy(y.data(), d_y, n * sizeof(float), cudaMemcpyDeviceToHost);

    cudaFree(d_x);
    cudaFree(d_y);

} // gaussian_kde