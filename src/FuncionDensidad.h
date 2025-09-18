// FuncionDensidad.h
#include "tinyexpr.h"
#ifndef FUNCIONDENSIDAD_H
#define FUNCIONDENSIDAD_H

void semillaI();

int** binomial(double theta, int num_ensayos, int cantidad_muestras);

int** binomial_puntual(double theta, int cantidad_muestras);

double* exponencial(int cantidad_muestras, double lambda);

double* normal(int cantidad_muestras, double sigma, double mu);

int** multinomial(double * probabilidades, int cantidad_muestras, int n_lanzamientos);

double estimate_M(te_expr* expr, double* vars_x, double* vars_y, double a, double b, int n_prelim);

double sample_condicional(te_expr* expr, double* vars_x, double* vars_y, double a, double b, int n_intentos, double M);

double** gibbs_sample(char* fxy, double* punto_inicial, int numero_muestras,double* intervalos, int n_prelim, int n_intentos);

void free_vector_int(int* ptr);

void free_vector_double(double* ptr);

void free_matriz_int(int** matriz, int cantidad_muestras);

void free_matriz_double(double** matriz, int cantidad_muestras);

#endif
