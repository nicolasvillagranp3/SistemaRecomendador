import pandas as pd
import numpy as np
from threading import Thread
import time
import re
import math

'''
Voy a usar una mezcla entre regex (limpiar el dataframe, buscar generos, titulos etc...) y user-based collaborative-filtering
para hacer recomendaciones infiriendo caracteristicas similares entre usuarios mas finas.
'''


def extract():
    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')
    return movies, ratings


def transform(movies, ratings, first_time):
    # Solo hace falta transformar el dataframe la primera vez que se ejecuta con las datasets en bruto
    # de ahi que false este puesto predeterminado.
    '''
    Sacamos los géneros que tienen las peliculas, limpiamos los titulos para
    facilitar su busqueda posterior y hacemos una operacion de conversion de
    los movieId a numeros ordenados segun aparicion (Va a hacer que todo vaya
    mucho mas rapido). Tambien pondremos una columna nueva de puntuacion media
    de peliculas que nos facilitara mucho las
    '''
    clean_genres = []
    for i in movies['genres']:
        aux = i.split('|')
        for j in aux:
            if j not in clean_genres:
                clean_genres.append(j)

    def mean_rating(x):
        encontrado = ratings[ratings.movieId == x]
        lon = len(encontrado)
        if lon != 0:
            return math.ceil(np.sum(encontrado['rating'])/lon)
        else:
            return 0

    def clean(a):
        # quitar cualquier cosas entre parentesis o que tenga comillas dobles
        return re.sub(r'\([^)]*\)|"', '', a).strip()

    def reindex(a):
        return new_index[a]
    if first_time:
        new_index = {}
        for i in range(b):
            new_index[movies.loc[i, 'movieId']] = i
            movies.loc[i, 'movieId'] = i
        movies['title'] = movies['title'].apply(clean)
        ratings = ratings.sort_values('movieId')
        ratings['movieId'] = ratings['movieId'].apply(reindex)
        ratings = ratings.sort_values('userId')
        movies['ratings'] = movies['movieId'].apply(mean_rating)
    return ratings, movies, clean_genres


def create_user_matrix(ratings, a, b):
    user_matrix = [[0 for i in range(b)] for j in range(a)]
    for i in range(len(ratings)):
        row = ratings.loc[i, 'userId']-1
        colunm = ratings.loc[i, 'movieId']
        user_matrix[row][colunm] = ratings.loc[i, 'rating']
    return user_matrix


def get_distance(a, b):
    '''
    Queremos que el hecho de que un usario no haya visto una pelicula que el otro si
    no afecte (ya que esto es justo lo que queremos obtener) y que las puntuaciones
    de las peliculas que han visto sean mas o menos parecidas. Con lo cual vamos a calcular
    la media de las distancias entre puntuaciones comunes de los usuarios.
    '''
    total = 0
    contador = 0
    for i in range(len(a)):
        if a[i] != 0 and b[i] != 0:
            total += abs(a[i]-b[i])
            contador += 1
    if contador == 0:
        # Si no tienen ninguna pelicula en comun no me sirve de nada.
        return np.inf
    else:
        return total/contador


def get_similar(user, user_matrix):
    '''
    New user seria un usuario al que le iremos haciendo preguntas.
    Lo mas importante de esta parte es calcular como de similares son dos usuarios.
    Lo hacemos con la funcion de distancia.
    '''
    min = np.inf
    idx = 0
    for i in range(len(user_matrix)):  # Encontramos la menor distancia.
        b = get_distance(user_matrix[i], user)
        if b < min:
            min = b
            idx = i
    return idx


def get_movie(movies):
    '''
    Obtenemos el id de la pelicula (si esta)
    '''
    titulo = input('Introduce el titulo de la pelicula: ')
    indice = -1
    continuar = True
    for i in range(len(movies)):
        if continuar:
            pelicula = movies.loc[i, 'title']
            if pelicula == titulo:
                indice = i
                continuar = False
            elif re.search(titulo, pelicula, re.IGNORECASE):
                indice = i
                entrada = input(
                    f'Es {pelicula} la pelicula que buscabas? (Y/n):  ')
                if entrada == 'Y':
                    continuar = False
    if continuar:
        return -1
    else:
        return indice


def get_rating(movies):
    '''
    A partir de un id obtenemos el rating medio
    '''
    indice = get_movie(movies)
    if indice != -1:
        c = movies.loc[indice, 'ratings']
        print(f'La puntuacion media de los usuarios es: {c}')
    else:
        print('Pelicula no encontrada en la base de datos.')


def get_by_genre(movies, genres):
    '''
    Podra elegir el género de la pelicula
    y si la prefiere reciente o antigua
    '''
    for i in range(1, len(genres)+1):
        print(f'{i}.{genres[i-1]}')
    try:
        elegido = int(input('Introduce el numero del género que deseas: '))
        entrada = int(
            input('Que prefieres peliculas antiguas (0) o nuevas (1) 0/1:'))
    except:
        print('El valor que has introducido no es de tipo numérico.')
        entrada = -1
    continuar = True
    genero = genres[elegido-1]
    if entrada == 0:  # De arriba a abajo
        # Le preguntamos si ya ha visto la pelicula.
        for i in range(len(movies)):
            if continuar:
                if movies.loc[i, 'ratings'] > 4 and re.search(genero, movies.loc[i, 'genres']):
                    c = movies.loc[i, 'title']
                    print(f'La pelicula es: {c} ')
                    entrada = input(
                        '¿Quieres obtener una pelicula distinta? Y/n: ')
                    if entrada == 'n':
                        # El bucle for seguira pero no hara nada, pondria un break pero nos han enseñado
                        continuar = False
                        # que es mala praxis de programacion.

    elif entrada == 1:
        for i in range(len(movies)):
            if continuar:
                if movies.loc[i, 'ratings'] > 4 and re.search(genero, movies.loc[i, 'genres']):
                    c = movies.loc[i, 'title']
                    print(f'La pelicula es: {c} ')
                    entrada = input(
                        '¿Quieres obtener una pelicula distinta? Y/n: ')
                    if entrada == 'n':
                        continuar = False


def hilo():
    global movies, ratings, a, b, user_matrix, clean_genres, first_time
    movies, ratings = extract()
    a = len(pd.unique(ratings['userId']))
    b = len(movies)
    ratings, movies, clean_genres = transform(movies, ratings, first_time)
    user_matrix = create_user_matrix(ratings, a, b)


def escribir(texto):
    for i in texto:
        print(i, end='', flush=True)
        time.sleep(0.06)
    print('')


def update_ratings(id_nuevo, indice, ratings):
    try:
        reseña = int(input('Valora la pelicula (1-5):'))
    except:
        print('Entrada invalida')
        reseña = -1
    if reseña > 0:
        ratings = pd.concat([ratings, pd.DataFrame({'userId': id_nuevo, 'movieId': indice,
                                                    'rating': reseña, 'timestamp': time.time()}, index=[len(ratings)])]).copy()
    return ratings


def create_new_user(ratings, movies):
    '''
    Objetivo: Crear un nuevo usuario y meterlo en el dataframe. Le daremos la opcion de meter peliculas
    que haya visto o de ser preguntado por peliculas que haya podido ver para poder hacerle mejores
    recomendaciones.
    '''
    id_nuevo = len(pd.unique(ratings['userId']))+1
    print(f'Tu id de usuario sera: {id_nuevo}')
    entrada = ''
    print('La informacion que nos aportes sera crucial para recomendarte peliculas buenas')
    pos = '1. Introducir reseña de pelicula\n2. Ser preguntado por peliculas aleatorias\n3. Salir\nIntroduce una opcion: (1/2/3): '
    while entrada != 3:
        try:
            entrada = int(input(pos))
        except:
            print('Entrada invalida')
            entrada = -1
        if entrada == 1:
            ratings = update_ratings(id_nuevo, get_movie(movies), ratings)
        elif entrada == 2:
            # Cogemos peliculas que sean mas probables
            a = movies[movies.ratings > 3]
            preguntas = a.sample(15)
            indices = list(preguntas['movieId'])
            titulos = list(preguntas['title'])
            for i in range(len(indices)):
                ver = input(f'Has visto la pelicula {titulos[i]}: Y/n')
                if ver == 'Y':
                    ratings = update_ratings(id_nuevo, indices[i], ratings)
    return ratings.astype('int64'), movies, id_nuevo


def update_user(id, ratings, movies):
    entrada = ''
    print('La informacion que nos aportes sera crucial para recomendarte peliculas buenas')
    pos = '1. Introducir reseña de pelicula\n2.Ser preguntado por peliculas aleatorias\n3. Salir\nIntroduce una opcion: (1/2/3): '
    while entrada != 3:
        try:
            entrada = int(input(pos))
        except:
            print('Entrada invalida')
            entrada = -1
        if entrada == 1:
            ratings = update_ratings(id, get_movie(movies), ratings)
        elif entrada == 2:
            # Cogemos peliculas que sean mas probables
            a = movies[movies.ratings > 3]
            preguntas = a.sample(15)
            indices = list(preguntas['movieId'])
            titulos = list(preguntas['title'])
            for i in range(len(indices)):
                ver = input(f'Has visto la pelicula {titulos[i]}: Y/n')
                if ver == 'Y':
                    ratings = update_ratings(id, indices[i], ratings)
    return ratings.astype('int64'), movies


def load(ratings, movies):
    ratings.to_csv('ratings.csv', header=True, index=None)
    movies.to_csv('movies.csv', header=True, index=None)


def recomendacion(userId, user_matrix, movies, ratings):
    # Aqui peta. Solo esta preparado para obtener una recomendacion
    if userId > len(user_matrix):
        print('EL usuario no existe. Pruebe a cerrar y abrir el programa')
    else:
        a = user_matrix.pop(userId-1)
        # cuando la matriz ya esta creada.
        idx = get_similar(a, user_matrix)+1
        id = ratings[(ratings.userId == idx) & (
            ratings.rating > 3)]['movieId'].sample(1)
        pelicula = list(movies.loc[id]['title'])[0]
        print(
            f'La pelicula elegida segun la valoracion de usuarios similares es: {pelicula}')


if __name__ == '__main__':
    '''
    El valor de first time es importante para no tener que procesar los dataframe cada vez que se ejecuta.
    Al sobreescribir la informacion de los ficheros no sera necesario y ganara en eficiencia.
    '''
    first_time = True  # Primera vez que se ejecuta True resto False
    # Para que vayan cargandose las cosas mientras hago las primeras operaciones de entrada y salida.
    hilo1 = Thread(target=hilo)
    hilo1.start()
    intro = 'Bienvenido al recomendador de peliculas\nA contiuacion podra iniciar sesion con su id de usuario o crear un nuevo usuario'
    menu = '1. Obtener puntuación de pelicula\n2. Obtener mejores peliculas por genero\n3. Recomendados para ti\n4. Actualizar usuario\n5. Salir del programa'
    escribir(intro)
    print('1. Iniciar Sesion con Id\n2. Crear usuario')
    hilo1.join()  # Esperamos a que se carguen todos los datos.
    try:
        entrada = int(input('Introduce la opcion deseada (1/2): '))
    except:
        print('Entrada invalida')
        entrada = 5
    if entrada == 1:
        try:
            id = int(input('Introduce tu Id de usuario: '))
        except:
            print('Entrada invalida')
            entrada = 5
    elif entrada == 2:
        ratings, movies, id = create_new_user(ratings, movies)
    while entrada != 5:
        print(menu)
        try:
            entrada = int(input('¿Que opcion deseas?: '))
        except:
            print('El valor introducido no es numerico.')
        if entrada == 1:
            get_rating(movies)
        elif entrada == 2:
            get_by_genre(movies, clean_genres)
        elif entrada == 3:
            recomendacion(id, user_matrix, movies, ratings)
        elif entrada == 4:
            ratings, movies = update_user(id, ratings, movies)
        print('\n')
    load(ratings, movies)  # Actualizamos los csv
    print('Gracias por usar el recomendador')
