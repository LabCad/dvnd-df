
		#include<stdio.h>
		

struct simplepycuda_grid { int x,y; };

struct simplepycuda_block { int x,y,z; };

__global__ void kernel_doublify( float* a )
		{
			int idx = threadIdx.x + threadIdx.y*4;
			a[idx] *= 2;
		}
	
extern "C" void kernel_loader( float* a , simplepycuda_grid g, simplepycuda_block b, size_t shared, size_t stream) {
//	printf("lets go! grid(%d,%d) block(%d,%d,%d) shared=%lu stream=%lu\n",g.x,g.y,b.x,b.y,b.z,shared,stream);
	dim3 mygrid;  mygrid.x = g.x;  mygrid.y = g.y;
	dim3 myblock; myblock.x = b.x; myblock.y = b.y; myblock.z = b.z;
	kernel_doublify<<<mygrid, myblock, shared, cudaStream_t(stream)>>>( a);
cudaDeviceSynchronize();
//	printf("finished kernel!");
}


//nvcc --shared __simplepycuda_kernel_doublify.cu  -o __simplepycuda_kernel_doublify.so --compiler-options -fPIC 2> __simplepycuda_kernel_doublify.log
