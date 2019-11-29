# -*- coding: utf-8 -*-
#Project Imformation: bilateral filter, CUDA accelerate, PyQt GUI.
#Author             : luoshutu.
#CUDA C

from pycuda.compiler import SourceModule

mod = SourceModule('''
__global__ void creatGaussModel(float *tGaussian, float *s_sigma, int *filModelLen)
{
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    float delta = s_sigma[0];
    int radius = filModelLen[0] / 2;
    tGaussian[x * 15 + y] = expf(-( (x - (radius)) * (x - (radius)) + 
                                     (y - (radius)) * (y - (radius)) ) / (2.0 * delta * delta));
}

//Euclidean Distance (x, y, d) = exp((|x - y| / d)^2 / 2)
__device__ float RangeGaussian(int center_value, int current_value, float delta)
{

    float xx = 1.f * (current_value - center_value)*(current_value - center_value);

    return expf(-xx / (2.f * delta * delta));
}

__global__ void bilateral_filter_kernel(unsigned int *d_dst, unsigned int *d_src, float *sGaussian, int *imgWidth, int *imgHeight, float *r_sigma, int *filModelLen)
{
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    int width = imgWidth[0];
    int height = imgHeight[0];
    float delta = r_sigma[0];
    int radius = filModelLen[0] / 2;

    if (x >= width || y >= height)
    {
        return;
    }

    float sum = 0.0f;
    float t = 0.0f;
    float factor;

    for (int m = -radius; m <= radius; m++)
    {
        for (int n = -radius; n <= radius; n++)
        {
            int y_index = y + m;
            int x_index = x + n;

            if (y_index < 0)        y_index = 0;
            if (x_index < 0)        x_index = 0;

            if (y_index >= height)  y_index = height - 1;
            if (x_index >= width)   x_index = width - 1;

            float center_value  = d_src[x       * height + y];
            float current_value = d_src[x_index * height + y_index];

            //factor = sGaussian[m + radius] * sGaussian[n + radius];
            factor = sGaussian[(m + radius) * filModelLen[0] + n + radius] * RangeGaussian(center_value, current_value, delta);
            t   += factor * current_value;
            sum += factor;
        }
    }

    d_dst[y + x * height] = 128;//floor(t / sum);
}
''')

bilateral_filter_kernel = mod.get_function('bilateral_filter_kernel')
creatGaussModel = mod.get_function('creatGaussModel')
