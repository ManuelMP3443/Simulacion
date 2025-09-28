#include "FuncionDensidad.h"
#include "tinyexpr.h"
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

// Aceptación-rechazo con M dinámico usando TinyExpr precompilado
static double sample_condicional(te_expr* expr, double* vars_x, double* vars_y, double a, double b, int n_intentos, double M){
    double x, u;

    for(int i = 0; i < n_intentos; i++){
        x = a + (b-a)*(double)rand()/RAND_MAX;
        *vars_x = x;
        u = ((double)rand()/RAND_MAX) * M; // u en [0,M]

        double fx = te_eval(expr);
        if(u <= fx) return x;
    }

    // fallback
    return a + (b-a)*(double)rand()/RAND_MAX;
}

// Estimación de M usando TinyExpr precompilado
static double estimate_M(te_expr* expr, double* vars_x, double* vars_y, double a, double b, int n_prelim){
    double x, max_f = 0.0;
    for(int i = 0; i < n_prelim; i++){
        x = a + (b-a)*(double)rand()/RAND_MAX;
        *vars_x = x;

        double fx = te_eval(expr);
        if(fx > max_f) max_f = fx;
    }
    return max_f * 1.1;
}

// Gibbs sampling con TinyExpr precompilado
double** gibbs_sample(char* fxy, double* punto_inicial, int numero_muestras, double* intervalos, int n_prelim, int n_intentos){
    double x = punto_inicial[0];
    double y = punto_inicial[1];

    // Variables que apuntan a x e y para TinyExpr
    double vars_x = x;
    double vars_y = y;
    te_variable vars[] = { {"x", &vars_x}, {"y", &vars_y} };

    // Compilar la expresión solo una vez
    te_expr* expr = te_compile(fxy, vars, 2, NULL);
    if(!expr) exit(1);

    // Preparar el arreglo de resultados
    double** resultado = calloc(numero_muestras+1, sizeof(double*));
    for(int i = 0; i < numero_muestras+1; i++)
        resultado[i] = calloc(2, sizeof(double));

    resultado[0][0] = x;
    resultado[0][1] = y;

    // Muestreo Gibbs
    for(int i = 1; i < numero_muestras+1; i++){
        // Estimar M para x dado y
        double Mx = estimate_M(expr, &vars_x, &vars_y, intervalos[0], intervalos[1], n_prelim);
        x = sample_condicional(expr, &vars_x, &vars_y, intervalos[0], intervalos[1], n_intentos, Mx);

        // Estimar M para y dado x
        double My = estimate_M(expr, &vars_y, &vars_x, intervalos[0], intervalos[1], n_prelim);
        y = sample_condicional(expr, &vars_y, &vars_x, intervalos[0], intervalos[1], n_intentos, My);

        resultado[i][0] = x;
        resultado[i][1] = y;
    }

    // Liberar expresión
    te_free(expr);

    return resultado;
}

// Función que devuelve una normal aleatoria usando Box-Muller
static double rand_normal() {
    double u1 = (rand() + 1.0) / (RAND_MAX + 2.0);
    double u2 = (rand() + 1.0) / (RAND_MAX + 2.0);
    return sqrt(-2.0 * log(u1)) * cos(2 * PI * u2);
}

// Evalúa condicional y devuelve muestra aleatoria de X|Y=y
static double eva_normalbi(double condicion, double sigma_cond, double sigma_muestreo, double rho, double mu_cond, double mu_muestreo) {
    double mu = mu_muestreo + rho * (sigma_muestreo / sigma_cond) * (condicion - mu_cond);
    double sigma = sigma_muestreo * sqrt(1 - rho*rho);
    return mu + sigma * rand_normal(); // Aquí generamos la muestra
}

// Muestreo Gibbs
double** normal_bivariada(double* punto_inicial, int numero_muestras, 
                          double sigma_x, double sigma_y, double mux, double muy, double rho) {
    
    double x = punto_inicial[0];
    double y = punto_inicial[1];

    double** resultado = calloc(numero_muestras+1, sizeof(double*));
    for(int i = 0; i < numero_muestras+1; i++)
        resultado[i] = calloc(2, sizeof(double));

    resultado[0][0] = x;
    resultado[0][1] = y;

    for(int i = 1; i <= numero_muestras; i++){
        x = eva_normalbi(y, sigma_y, sigma_x, rho, muy, mux);
        y = eva_normalbi(x, sigma_x, sigma_y, rho, mux, muy);

        resultado[i][0] = x;
        resultado[i][1] = y;
    }

    return resultado;
}

double eval_triangulo(double min_val, double max_val) {
    // Devuelve un número uniforme entre min_val y max_val
    double r = (double)rand() / RAND_MAX;
    return min_val + r * (max_val - min_val);
}

double** triangulo(double* punto_inicial, int numero_muestras) {

    double x = punto_inicial[0];
    double y = punto_inicial[1];

    // Preparar el arreglo de resultados
    double** resultado = calloc(numero_muestras + 1, sizeof(double*));
    for(int i = 0; i <= numero_muestras; i++)
        resultado[i] = calloc(2, sizeof(double));

    resultado[0][0] = x;
    resultado[0][1] = y;

    for(int i = 1; i <= numero_muestras; i++) {
        // Para x dado y: 0 <= x <= 1 - y
        x = eval_triangulo(0, 1 - y);

        // Para y dado x: 0 <= y <= 1 - x
        y = eval_triangulo(0, 1 - x);

        resultado[i][0] = x;
        resultado[i][1] = y;
    }

    return resultado;
}

static double rand_uniform(double a, double b) {
    return a + (b - a) * ((double) rand() / RAND_MAX);
}

static double eval_lineal(double a, double b, double y_fixed, int es_x) {
   
    double c = 3.0 * y_fixed + 2.0; 
    
    double cdf_max = (b*b + c*b) - (a*a + c*a); 
    double u = ((double) rand() / RAND_MAX) * cdf_max;
    
    double discr = c*c + 4*(u + a*a + c*a);
    double x = (-c + sqrt(discr)) / 2.0;
    return x;
}

double** lineal(double* punto_inicial, int numero_muestras){
    double x = punto_inicial[0];
    double y = punto_inicial[1];

    double** resultado = calloc(numero_muestras + 1, sizeof(double*));
    for(int i = 0; i <= numero_muestras; i++)
        resultado[i] = calloc(2, sizeof(double));

    resultado[0][0] = x;
    resultado[0][1] = y;

    for(int i = 1; i <= numero_muestras; i++) {
        // Para x dado y
        x = eval_lineal(0, 2, y, 1); // '1' indica que estamos generando x

        // Para y dado x
        y = eval_lineal(0, 2, x, 0); // '0' indica que estamos generando y

        resultado[i][0] = x;
        resultado[i][1] = y;
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

void free_matriz_double(double** matriz, int cantidad_muestras){
    if(matriz == NULL) return;
    for(int j = 0; j < cantidad_muestras; j++){
        free(matriz[j]);
    }
    free(matriz);
}

