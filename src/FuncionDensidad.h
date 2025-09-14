// FuncionDensidad.h
#ifndef FUNCIONDENSIDAD_H
#define FUNCIONDENSIDAD_H

void semillaI();

int** binomial(double theta, int num_ensayos, int cantidad_muestras);

int** binomial_puntual(double theta, int cantidad_muestras);

double* exponencial(int cantidad_muestras, double lambda);

double* normal(int cantidad_muestras, double sigma, double mu);

int** multinomial(double * probabilidades, int cantidad_muestras, int n_lanzamientos);

void free_vector_int(int* ptr);

void free_vector_double(double* ptr);

void free_matriz_int(int** matriz, int cantidad_muestras);

#endif
