#include "FuncionDensidad.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define PI 3.14159265358979323846

static int semilla = 0;

void semillaInicial(){
	if(!semilla){
		srand(time(NULL));
		semilla = 1;
	}
}

int** binomial(double theta, int num_ensayos, int cantidad_muestras){
    int** resultado = calloc(2, sizeof(int*)); // inicializa a 0
	int* valores = calloc(cantidad_muestras*num_ensayos, sizeof(int));
	int* frecuencia = calloc(num_ensayos+1, sizeof(int));

    int exitos;
    double aleatorio;

    for(int i = 0; i < cantidad_muestras; i++) {
        exitos = 0;
        for(int j = 0; j < num_ensayos; j++) {
            aleatorio = (double)rand() / RAND_MAX; // número entre 0 y 1
            if(aleatorio < theta) {
                exitos++;
				valores[i*num_ensayos+j] = 1;
            }
        }
        frecuencia[exitos]++; // contar cuántos éxitos 
    }

	resultado[0] = valores;
	resultado[1] = frecuencia;
    return resultado;
}

int** binomial_puntual(double theta, int cantidad_muestras){
	int** resultado = binomial(theta, 1, cantidad_muestras);
	return resultado; 
}

double* exponencial(int cantidad_muestras, double lambda){
	double* resultado = calloc(cantidad_muestras, sizeof(double));
	double x, u;
	
	for(int i = 0; i < cantidad_muestras; i++) {
	        u = (double)rand() / RAND_MAX;    // número uniforme 0-1
	        x = -log(u) / lambda;             // fórmula de exponencial
	        resultado[i] = round(x * 1e6) / 1e6;
	    }
	return resultado;
}

double* normal(int cantidad_muestras, double sigma, double mu){
	double* resultado = calloc(cantidad_muestras, sizeof(double));
	double u1, u2, z, x;

	for(int i = 0; i < cantidad_muestras; i++){
		u1 = (double)rand()/RAND_MAX;
		u2 = (double)rand()/RAND_MAX;

		z = sqrt(-2 * log(u1)) * cos(2* PI * u2);
		x = mu + sigma * z;
		resultado[i] = round(x*1e6)/1e6;
		
	}
	return resultado; 
	
}

int** multinomial(double * probabilidades, int cantidad_muestras, int n_lanzamientos){
	double total = 0.0;
	int i = 0;
	double acum ,r = 0.0;
	
	while(probabilidades[i] != -1.0){
		total += probabilidades[i];
		i++;
	}

	if(fabs(total - 1.0) > 1e-6){
		return NULL;
	}

	int** resultado = calloc(cantidad_muestras, sizeof(int*));
	

	for(int j = 0; j < cantidad_muestras; j++){
		int* vector = calloc(i, sizeof(int));
		for(int k = 0; k < n_lanzamientos; k++){
			r = (double)rand()/RAND_MAX;
			acum = 0.0;
			for(int l = 0; l < i; l++){
				acum += probabilidades[l];
				if(r < acum || l == i-1){
					vector[l] += 1;
					break;
				}

					
			}
		}
		resultado[j] = vector;
	}
	return resultado;
}

void free_vector_int(int* ptr){
    free(ptr);
}

void free_vector_double(double* ptr){
    free(ptr);
}

void free_matriz_int(int** matriz, int cantidad_muestras){
    if(matriz == NULL) return;
    for(int j = 0; j < cantidad_muestras; j++){
        free(matriz[j]);
    }
    free(matriz);
}

