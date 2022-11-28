# Sistema de Recomendación de películas usando expresiones regulares y user-based collaborative filtering en python.
## Intro.
El obejtivo de cualquier recomendador de peliculas es tratar de conocer los gustos profundos del usuario para poder recomendarle peliculas que quizá a priori 
no vería. Con esta idea, a partir del dataset obtenido, desarrollamos una recomendación basadada en obtener los usuarios más similares a uno dado, entendiendo la similitud como una distancia entre puntos de un espacio representado por usuarios, en el que los usuarios con calificaciones parecidas estaran mas cercanos.
## Implementación.
El código viene correctamente documentado, pero una explicación breve me parecia necesaria. 
El programa comienza por cargar y calcular los datos de los ficheros y la matriz de los usuarios de manera concurrente a las operaciones de entrada y salida iniciales mediante la implementacion de un hilo, (para que la experiencia sea mas rapida y fluida). Posteriormente se le permitira al usuario realizar distintas operaciones:
- El usuario podra iniciar sesión con un usuario ya existente o crear uno nuevo.
- El usuario podrá buscar la puntuacion de distintas peliculas para orientarse (implementado usando regex).
- El usuario podrá ser recomendado las mejores peliculas por genero (implementado usando regex)
- El usuario podrá actualizar la puntuacion que la ha dado a las peliculas en el pasado, o incluso puntuar una nueva (implementado usando regex). Cabe explicar que estas
operaciones son de vital importancia para nutrir de datos al modelo, de ahí que haya una opción en la que el usuario pueda ser preguntado acerca de distintas peliculas.
- El usuario podrá obtener la recomendación de una pelicula en especial para su caso, basandose en la idea de proximidad con otros usuarios anteriormente explicado.

- Cabe destacar que toda informacion que se le proporcione al programa sera correctamente guardada para poder ser usada mas adelante en otras ejecuciones, es decir,
al crear un usuario y dotarlo de información, este podra ser consultado y usado en cualquier momento.
Las particularidades del codigo, como por ejemplo las operaciones de limpieza, vienen precisamente explicadas en él.
## Requirements.
- Para poder correr el programa hay que instalar los paquetes necesarios con sus correspondientes versiones. Se ejecutara el siguiente codigo en terminal:
> pip install -r requirements.txt
## Docker.
Para lanzar la imagen de docker habrá que seguir los siguientes pasos:

1. Crear la imagen:
El punto indica que se cogen todos los archivos del directorio en el que nos encontramos. Podemos llamar a la imagen como queramos, teniendo en cuenta que al ejecutarla tendremos que usar ese nombre.
> docker build . -t 'Nombre Imagen'

2. Una vez que tengamos la imagen creada tendremos que elegir un nombre de un contenedor para poder ejecutarlo de nuevo invocandolo. Esto se indica a traves
de --name. Tambien sera importante ejecutarlo con el flag -it para que el programa sea interactivo.
> docker run -it --name 'Nombre Contenedor' -it 'Nombre Imagen'
- Este primer comando sera unicamente necesario ejecutarlo una unica vez. Cada vez que queramos correr el contenedor con la informacion guardada tendremos que
que ejecutar:
> docker start -i 'Nombre Contenedor'




