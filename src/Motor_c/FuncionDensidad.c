#include "FuncionDensidad.h"
#include "tinyexpr.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdio.h>

#define PI 3.14159265358979323846

static int semilla = 0;

void semillaInicial(){
	if(!semilla){
		srand(time(NULL));
		semilla = 1;
	}
}

int* binomial(double theta, int num_ensayos, int cantidad_muestras){
	int* frecuencia = calloc(num_ensayos+1, sizeof(int));

    int exitos;
    double aleatorio;

    for(int i = 0; i < cantidad_muestras; i++) {
        exitos = 0;
        for(int j = 0; j < num_ensayos; j++) {
            aleatorio = (double)rand() / RAND_MAX; // número entre 0 y 1
            if(aleatorio < theta) {
                exitos++;
            }
        }
        frecuencia[exitos]++; // contar cuántos éxitos 
    }

    return frecuencia;
}

int** binomial_puntual(double theta, int cantidad_muestras){
    int** resultado = calloc(2, sizeof(int*)); // inicializa a 0
	int* valores = calloc(cantidad_muestras*1, sizeof(int));
	int* frecuencia = calloc(2, sizeof(int));

    int exitos;
    double aleatorio;

    for(int i = 0; i < cantidad_muestras; i++){
        exitos = 0;
        aleatorio = (double)rand()/RAND_MAX;
        if(aleatorio < theta) {
            exitos++;
			valores[i] = 1;
        }else{
            valores[i] = 0;
        }
        frecuencia[exitos]++;
    }

	resultado[0] = valores;
	resultado[1] = frecuencia;
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

int metropolis_paso(int k_actual, int n_max, te_expr* expr, double* k_var_double) {

    // --- 1. PROPUESTA (Lógica sin cambios) ---
    int k_prop;
    double q_ki, q_ik; 

    if (k_actual == 0) {
        k_prop = 1;
        q_ki = 1.0; 
        q_ik = (n_max == 1) ? 1.0 : 0.5;
    } else if (n_max != -1 && k_actual == n_max) {
        k_prop = n_max - 1;
        q_ki = 1.0; 
        q_ik = (n_max - 1 == 0) ? 1.0 : 0.5;
    } else {
        k_prop = k_actual + ((double)rand() / RAND_MAX < 0.5 ? -1 : 1);
        q_ki = 0.5; 
        if (k_prop == 0 || (n_max != -1 && k_prop == n_max)) {
            q_ik = 1.0; 
        } else {
            q_ik = 0.5; 
        }
    }

    // --- 2. EVALUACIÓN (Asume LOG-PROB) ---
    *k_var_double = (double)k_actual; 
    double log_f_actual = te_eval(expr); // Asume que esto es log(P)

    *k_var_double = (double)k_prop; 
    double log_f_propuesta = te_eval(expr); // Asume que esto es log(P)

    // --- 3. ACEPTACIÓN (Manejo de -inf) ---
    
    // Si log(P_actual) = -inf (P=0)
    if (isinf(log_f_actual) && log_f_actual < 0) {
        if (log_f_propuesta > -INFINITY) {
            return k_prop; // Aceptar (movimiento 0 -> >0)
        }
        return k_actual; // Rechazar (movimiento 0 -> 0)
    }
    // Si log(P_propuesta) = -inf (P=0)
    if (isinf(log_f_propuesta) && log_f_propuesta < 0) {
        return k_actual; // Rechazar (movimiento >0 -> 0)
    }

    // Ambas P son > 0
    double log_A = (log_f_propuesta + log(q_ik)) - (log_f_actual + log(q_ki));

    // Aceptación segura
    double u = (double)rand() / RAND_MAX;
    if (u == 0.0) return k_prop; // Evitar log(0)

    if (log(u) < log_A) {
        return k_prop; // Aceptar
    }
    
    return k_actual; // Rechazar
}

int* Metropolis1DDiscreta(char* fx, int punto_inicial, int limite, int numero_muestras, int burstime) {
    
    double k_var_para_tinyexpr = (double)punto_inicial; 
    
    te_variable vars[] = { {"x", &k_var_para_tinyexpr} };

    te_expr* expr = te_compile(fx, vars, 1, NULL);
    if (!expr) return NULL; 

    int* resultado = calloc(numero_muestras - burstime, sizeof(int));
    if (resultado == NULL) exit(1); 
    
    int k_actual = punto_inicial;
    int i_resultado = 0; 
    
    for (int i = 0; i < numero_muestras; i++) {
        
        k_actual = metropolis_paso(k_actual, limite, expr, &k_var_para_tinyexpr);
        if (i >= burstime) {
            resultado[i_resultado] = k_actual;
            i_resultado++;
        }
    }

    te_free(expr);
    return resultado;
}

static double metropolis_paso_continuo(double k_actual, double sigma, te_expr* expr, double* k_var_double) {
    
    // --- 1. PROPUESTA (Lógica sin cambios) ---
    double u1 = (rand() + 1.0) / (RAND_MAX + 2.0);
    double u2 = (rand() + 1.0) / (RAND_MAX + 2.0);
    double z = sqrt(-2.0 * log(u1)) * cos(2 * PI * u2);
    double k_prop = k_actual + z * sigma;

    // --- 2. EVALUACIÓN (Asume LOG-PROB) ---
    *k_var_double = k_actual;
    double log_f_actual = te_eval(expr);

    *k_var_double = k_prop;
    double log_f_propuesta = te_eval(expr);

    // --- 3. ACEPTACIÓN (Manejo de -inf) ---
    if (isinf(log_f_actual) && log_f_actual < 0) {
        if (log_f_propuesta > -INFINITY) return k_prop; // Aceptar 0 -> >0
        return k_actual; // Rechazar 0 -> 0
    }
    if (isinf(log_f_propuesta) && log_f_propuesta < 0) {
        return k_actual; // Rechazar >0 -> 0
    }
    
    double log_A = log_f_propuesta - log_f_actual; 
    
    // Aceptación segura (tu método ya era seguro)
    double log_u = log((rand() + 1.0) / (RAND_MAX + 2.0));
    
    if (log_u < log_A) {
        return k_prop; // Aceptar
    }
    
    return k_actual; // Rechazar
}


double* Metropolis1DContinua(char* fx, double punto_inicial, double sigma, int numero_muestras, int burstime) {
    
    // tinyexpr DEBE usar un puntero a double
    double k_var_para_tinyexpr = punto_inicial; 
    
    // (Te recomiendo usar 'x' como variable, es más estándar para continuo)
    te_variable vars[] = { {"x", &k_var_para_tinyexpr} };

    te_expr* expr = te_compile(fx, vars, 1, NULL);
    if (!expr) return NULL; 

    // --- CORREGIDO: double* y sizeof(double) ---
    double* resultado = calloc(numero_muestras - burstime, sizeof(double));
    if (resultado == NULL) exit(1); 
    
    double k_actual = punto_inicial;
    int i_resultado = 0; 
    
    // Bucle único de simulación
    for (int i = 0; i < numero_muestras; i++) {
        
        // --- CORREGIDO: Llama al 'paso' correcto y pasa 'sigma' ---
        k_actual = metropolis_paso_continuo(k_actual, sigma, expr, &k_var_para_tinyexpr);
        
        // Guardar si ya pasó el burn-in
        if (i >= burstime) {
            resultado[i_resultado] = k_actual;
            i_resultado++;
        }
    }

    te_free(expr);
    return resultado; // Devuelve un puntero a double
}


static void metropolis_paso_continuo_2d(double* k_actual, double sigma, te_expr* expr, double* x_var, double* y_var) {
    
    // --- 1. PROPUESTA (Lógica sin cambios) ---
    double k_prop[2];
    k_prop[0] = k_actual[0] + rand_normal() * sigma;
    k_prop[1] = k_actual[1] + rand_normal() * sigma; 

    // --- 2. EVALUACIÓN (Asume LOG-PROB) ---
    *x_var = k_actual[0];
    *y_var = k_actual[1];
    double log_f_actual = te_eval(expr);

    *x_var = k_prop[0];
    *y_var = k_prop[1];
    double log_f_propuesta = te_eval(expr);

    // --- 3. ACEPTACIÓN (Manejo de -inf) ---
    if (isinf(log_f_actual) && log_f_actual < 0) {
        if (log_f_propuesta > -INFINITY) { // Aceptar 0 -> >0
             k_actual[0] = k_prop[0]; 
             k_actual[1] = k_prop[1];
        }
        return; // Rechazar 0 -> 0
    }
    if (isinf(log_f_propuesta) && log_f_propuesta < 0) {
        return; // Rechazar >0 -> 0
    }

    double log_A = log_f_propuesta - log_f_actual;

    // Aceptación segura
    double u = (double)rand() / RAND_MAX;
    if (u == 0.0) {
        k_actual[0] = k_prop[0]; 
        k_actual[1] = k_prop[1];
        return;
    }

    if (log(u) < log_A) {
        k_actual[0] = k_prop[0]; 
        k_actual[1] = k_prop[1];
    }
    // else: Rechazar
}

double** Metropolis2DContinua(char* fxy, double* punto_inicial, double sigma, int numero_muestras, int burstime) {
    
    // --- 1. PREPARACIÓN DE TINYEXPR ---
    double x_var_tinyexpr = punto_inicial[0]; 
    double y_var_tinyexpr = punto_inicial[1];
    
    te_variable vars[] = { 
        {"x", &x_var_tinyexpr},
        {"y", &y_var_tinyexpr}
    };

    te_expr* expr = te_compile(fxy, vars, 2, NULL);
    if (!expr) return NULL; 

    // --- 2. PREPARACIÓN DE RESULTADOS ---
    double** resultado = calloc(numero_muestras - burstime, sizeof(double*));
    if (resultado == NULL) exit(1); 
    
    double k_actual[2]; // El estado actual [x, y]
    k_actual[0] = punto_inicial[0];
    k_actual[1] = punto_inicial[1];
    
    int i_resultado = 0; 
    
    // --- 3. BUCLE ÚNICO ---
    for (int i = 0; i < numero_muestras; i++) {
        
        // Llama al "paso" (pasa k_actual por referencia)
        metropolis_paso_continuo_2d(k_actual, sigma, expr, &x_var_tinyexpr, &y_var_tinyexpr);
        
        // Guardar si ya pasó el burn-in
        if (i >= burstime) {
            resultado[i_resultado] = calloc(2, sizeof(double)); // Reservar fila
            resultado[i_resultado][0] = k_actual[0];
            resultado[i_resultado][1] = k_actual[1];
            i_resultado++;
        }
    }

    te_free(expr);
    return resultado; // Devuelve un puntero a (puntero a double)
}

static void metropolis_paso_discreto_2d(int* k_actual, int* n_max, te_expr* expr, double* kx_var, double* ky_var) {
    
    // --- 1. PROPUESTA (Lógica sin cambios) ---
    int i_x = k_actual[0], i_y = k_actual[1];
    int n_max_x = n_max[0], n_max_y = n_max[1];
    int k_prop[2] = {i_x, i_y};
    double q_ki = 0.5, q_ik = 0.5;

    if ((double)rand() / RAND_MAX < 0.5) {
        // Mover en X ... (lógica idéntica)
        if (i_x == 0) { k_prop[0] = 1; q_ki = 1.0; q_ik = (n_max_x == 1) ? 1.0 : 0.5; }
        else if (n_max_x != -1 && i_x == n_max_x) { k_prop[0] = n_max_x - 1; q_ki = 1.0; q_ik = (n_max_x - 1 == 0) ? 1.0 : 0.5; }
        else { k_prop[0] = i_x + ((double)rand() / RAND_MAX < 0.5 ? -1 : 1); q_ki = 0.5;
            if (k_prop[0] == 0 || (n_max_x != -1 && k_prop[0] == n_max_x)) q_ik = 1.0;
            else q_ik = 0.5;
        }
    } else {
        // Mover en Y ... (lógica idéntica)
        if (i_y == 0) { k_prop[1] = 1; q_ki = 1.0; q_ik = (n_max_y == 1) ? 1.0 : 0.5; }
        else if (n_max_y != -1 && i_y == n_max_y) { k_prop[1] = n_max_y - 1; q_ki = 1.0; q_ik = (n_max_y - 1 == 0) ? 1.0 : 0.5; }
        else { k_prop[1] = i_y + ((double)rand() / RAND_MAX < 0.5 ? -1 : 1); q_ki = 0.5;
            if (k_prop[1] == 0 || (n_max_y != -1 && k_prop[1] == n_max_y)) q_ik = 1.0;
            else q_ik = 0.5;
        }
    }
    
    // --- 2. EVALUACIÓN (Asume LOG-PROB) ---
    *kx_var = (double)i_x;
    *ky_var = (double)i_y;
    double log_f_actual = te_eval(expr); // CAMBIADO

    *kx_var = (double)k_prop[0];
    *ky_var = (double)k_prop[1];
    double log_f_propuesta = te_eval(expr); // CAMBIADO

    // --- 3. ACEPTACIÓN (Manejo de -inf) ---
    // Original: if (f_actual == 0) ...
    if (isinf(log_f_actual) && log_f_actual < 0) { // log(0) = -inf
        if (log_f_propuesta > -INFINITY) {
            k_actual[0] = k_prop[0];
            k_actual[1] = k_prop[1];
        }
        return; // 0 -> 0 ó 0 -> >0
    }
    // Original: if (f_propuesta == 0) ...
    if (isinf(log_f_propuesta) && log_f_propuesta < 0) {
        return; // Rechazar >0 -> 0
    }

    // Original: log_R = log(f_propuesta) + log(q_ik) - log(f_actual) - log(q_ki);
    // --- CÁLCULO LOG_R (CORREGIDO) ---
    double log_R = (log_f_propuesta + log(q_ik)) - (log_f_actual + log(q_ki));

    // Aceptación segura (tu método ya era seguro)
    double u = (double)rand() / RAND_MAX;
    if (u == 0.0) {
        k_actual[0] = k_prop[0];
        k_actual[1] = k_prop[1];
        return;
    }
    double log_u = log(u);
    if (log_u < log_R) {
        k_actual[0] = k_prop[0]; 
        k_actual[1] = k_prop[1];
    }
}

double** Metropolis2DDiscreta(char* fxy, int* punto_inicial, int* n_max, int numero_muestras, int burstime) {
    
    // --- 1. PREPARACIÓN DE TINYEXPR (con 'fac') ---
    double kx_var_tinyexpr = (double)punto_inicial[0]; 
    double ky_var_tinyexpr = (double)punto_inicial[1];
    
    te_variable vars[] = { 
        {"x", &kx_var_tinyexpr}, 
        {"y", &ky_var_tinyexpr}
    };

    te_expr* expr = te_compile(fxy, vars, 2, NULL);
    if (!expr) return NULL; 

    
    // --- 2. PREPARACIÓN DE RESULTADOS ---
    double** resultado = calloc(numero_muestras - burstime, sizeof(double*));
    if (resultado == NULL) exit(1); 
    
    int k_actual[2]; // El estado actual [k, l]
    k_actual[0] = punto_inicial[0];
    k_actual[1] = punto_inicial[1];
    
    int i_resultado = 0; 
    
    // --- 3. BUCLE ÚNICO ---
    for (int i = 0; i < numero_muestras; i++) {
        
        metropolis_paso_discreto_2d(k_actual, n_max, expr, &kx_var_tinyexpr, &ky_var_tinyexpr);
        
        if (i >= burstime) {
            resultado[i_resultado] = calloc(2, sizeof(double));
            resultado[i_resultado][0] = (double)k_actual[0]; // Guardar como double
            resultado[i_resultado][1] = (double)k_actual[1];
            i_resultado++;
        }
    }

    te_free(expr);
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

