---
title: Breve introducción a Docker
subtitle: Material en [GitHub](https://github.com/D3f0/talks/)
author: Nahuel Defossé
lang: es-AR
header-includes:
    - \usepackage[normalem]{ulem}
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyfoot[CO,CE]{}
    - \fancyfoot[LE,RO]{}
---

# Indice

\tableofcontents

# Docker vs Máquinas Virtuales

Los contenedores permiten a las aplicaciones:

| Métrica | Docker | VMs |
|---------+--------+--------------------|
| Aislamiento  | Bajo | Alto |
| Arranque | Segundos | Minutos |
| SO | Linux [^dock_support] | Linux, Windows, OSX |
| Tamaño | 100M+ | 1G+ |
| Construcción de Imágenes | Corto (minutos) | Largo (Horas) |
| Cantidad Máxima | >50 | <10 |
| Hosting | Docker Hub, Gitlab | ISOs, Vagrant Cloud |

[^dock_support]: Se puede utilizar a través de VirtualBox, xhyve (MacOS) o HyperV (Windows)

# Máquinas virtuales...

![Apliaciones en ejecución con VM](images/WhatIsDocker_2_VMs_0.png)

#  ...y contenedores

![Apliaciones en ejecución en Docker](images/WhatIsDocker_3_Containers_1.png)

# Instalación

## Linux
 * Disponible en el sistema de paquetes
 * [Guía de Instalación en Ubuntu]( https://docs.docker.com/engine/installation/linux/ubuntulinux/)
 * Imporntante agregarse al grupo docker
  `sudo gpasswd -a $(whoami) docker` y volver a iniciar sesión.


# Instalación

## Windows

### Docker Toolbox

* `docker-machine` + Virtualbox + Kitematic
* **Windows 10** Utilizando docker nativo

### Docker for Windows

  * **Beta** con emulación nativa HyperV (Windows 10)
  * https://docs.docker.com/docker-for-windows/

# Instalación Windows (2)

![Instalación de Toolbox](images/Docker_Toolbox.png)

# Instalación

## Mac

### Docker Toolbox

 * `docker-machine` + Virtualbox + Kitematic

### Docker for Mac

 * Beta con emulación nativa de OS X


# Windows y Mac

En Linux la ejecución de Docker es nativa, pero en windows,
necesitamos un soporte que nos provee `docker-machine` en formato de máquina
virtual.

## Creación de una máquina virtual con `docker-machine`

 * `docker-machine create --driver virtualbox vm`
 * `eval $(docker-machine env vm)` o `docker-machine`


# Primer ejecución de un contenedor

### Ejecución bash [^*] en una imagen **debian**

```
docker run -ti debian bash
Unable to find image debian:latest locally
latest: Pulling from library/debian

43c265008fae: Pull complete
Digest: sha256:c1af755d300d0c65bb1194d24bc
Status: Downloaded newer image for debian:latest
root@f601df7b7dd9:/# whoami; pwd; ps
root
/
  PID TTY          TIME CMD
    1 ?        00:00:00 bash
    8 ?        00:00:00 ps
```

[^*]: `-ti` en `run` indican uso de una `tty` y modo `interactivo` en vez de background.

# ¿Qué ocurrió?

 * Docker bajó la imagen de [**dockerhub.io**](https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=debian&starCount=0)
 * Como no le dijimos que versión, bajó `latest` (es lo mismo que haberle puesto **`docker run -ti debian:latest bash`** [^versions]).
 * Se creó un  *contenedor* a partir de la imagen de *debian*.
 * Si iniciamos **`docker ps`** en otro terminal, veremos detalles sobre el contenedor.

[^versions]: Otra versión podría ser `jessie`, `stable`, `oldstable`.

# Imágenes

* Las imágenes nos permiten iniciar contenedores. Los tamaños suelen ser mucho más pequeños que la máquina virtual equivalente.

```
$ docker images
REPOSITORY          TAG                 IMAGE ID
CREATED             SIZE
debian              latest              7b0a06c805e8
2 days ago          123 MB
```

[^img_dock]: Estás imagenes nos serán de utlidad cuando aprendamos a usar `Dockerfiles`

# Imagenes (cont).

 * Las imágnees puede descargarse con `docker pull` además de ser automáticamente descargads por `docker run`.
 * Se pueden borrar con **`docker rmi <NOMBRE>`** o **`docker rmi <IMAGE ID>`**.
 * Existen imagenes de diferentes linux como **debian**, **centos**, **ubuntu** pero también de productos específicos como **mysql**, **httpd** (apache), **postgres** entre otros [^img_dock].
 * Las imágenes de productos ya conocen el binario que deben ejecutar

# Contenedores

* A diferencia de las VMs, inciar múltiples contenedores no es mayor problema.

![Dos contenedores basados en la imagen de **debian**](images/2_debian_cont.png)


# Sistema de archivos

* El sistema de archivos de cada contenedor está basado en su imagen, **pero no se comparte**, por lo tanto cada contenedor tiene su sistema de archivos independiente.
* Dos `run` consecutivos a pesar de estar basados en la misma imagen no compartirán archivos.

# Sistema de archivos

```bash
$ docker run -ti debian bash
root@9b6cecd04132:/# echo "Prueba" > prueba
root@9b6cecd04132:/# cat prueba
Prueba
root@9b6cecd04132:/# exit
$ docker run -ti debian bash
root@31d4e1b3638a:/# cat prueba
cat: prueba: No such file or directory
root@31d4e1b3638a:/#
```

# Volúmenes

## Características

* Los **volúmenes** permiten **compartir sistema de archivos**, ésto es útil para:
    - Permiten persistir datos (si estamos corriendo un software de DB)
    - Permiten compartir código fuente u otros archivos con el anfitrión que deban ser gestionados (repositorios).
    - Permiten compartir datos entre contenedores
* El argumento de **`run`** es **`-v rutaHost:rutaContenedor`**, dónde ambas deben ser absolutas, pero podemos ayudarnos con **`$(pwd)`** para no *sepultar* rutas.

# Volúmenes

## Ejemplo

```bash
$ mkdir vol    # Carpeta a compartir
$ docker run -ti -v "$(pwd)/vol:/vol" debian bash
root@962570a041ad:/# echo "prueba" > /vol/prueba
root@962570a041ad:/# exit
$ docker run -ti -v "$(pwd)/vol:/vol" debian bash
root@d32929d3813d:/# cat /vol/prueba
prueba
root@d32929d3813d:/# exit
$ cat vol/prueba
prueba
```

# Puertos

Docker permite exponer puertos que se comparten de manera automática con el host.

* `-P` Publicar todos los puertos definidos en el `Dockerfile` en todas las interfases del host.
* `-p` Publicar un puerto o rango al host:
    - `ip:hostPort:containerPort` Ej: `-p 127.0.0.1:8000:80`
    - `ip::containerPort`
    - `hostPort:containerPort`
    - `containerPort`
* Para probar apache publicandolo en el puerto 8000:
  `docker run -p 8001:80 -ti httpd`[^nobin]

[^nobin]: Cuando veamos `Dockerfile` veremos por que no es necesario especificar el binario a ejecutar.

# Puertos (cont.)

![Apache ejecutandose en modo interactivo](images/itworks.png)

# Gestión de Contenedores

* Los contenedores **no se pierden** cuando **termina su ejecución**, podemos ver una lista de lo que hemos ejecutado con **`docker ps -a`**.
* Si queremos un contenedor transitorio, que limpie sus rastros tras terminar agrgamos a **`run`**  el argumento **`--rm`**.
* Para borrar contenedores viejos, **`docker rm <NOMBRE>`** o **`docker rm <CONTAINER ID>`**.
* Podemos re-lanzar contenedores viejos utilizando **`docker start <NOMBRE>`** o **`docker start <CONTAINER ID>`**.
* Al momento del **`run`** podemos dar un nombre a un contenedor con **`--name`** [^random_name]

[^random_name]: Así evitando la generación uno aleatorio (Ej: **`crazy_einstein`**


# Gestión de Contenedores (cont)

## Interactivo y Desacoplado
* Si reemplazamos `-ti` por `-d` en `run`, el contenedor se ejecuta en segundo plano.
  `docker run -d httpd --name apache`. Solo impimirá el ID.
* Podemos reclamar la temrinal, utilizando `docker attach`.

## Ejecución en contenedores
* `docker exec <NOMBRE> <COMANDO>` nos permite conectarnos a un contenedor en ejecución.
* Si el contenedor no está ej ejecución, podemos inciarlo con `docker start <NOMBRE>`.
* Sirve para explorar el filesystem y realizar pruebas.
* Ej: `docker exec apachecito bash`


# Gestión de Contenedores (cont)

## Politica de inicio

* Al momento de **`run`** o **`start`** podemos dar una política de inicio para nuestro contenedor con **`--restart`**:

    + **`--restart no`**  No reiniciar el contenedor automáticamente cuando termina. Es el default.
    + **`--restart on-failure`** Reinicia solo si el contenedor termina con una estado distinto de 0.
    + **`--restart on-failure:3`** Idem anterior, con máximo de 3 reinicios.
    + **`--restart always`** Siempre reinicia el contenedor independientemente del estado de salida. Se iniciará automáticamente **cuando el servcio docker se arranque**.
    + **`--restart unless-stopped`** Siempre se reinicia hasta que se para (**`stop`**). Al inicio del servicio docker, tomará el estado anterior.

# Ejemplo
## Creando un contenedor con httpd (apache)

1. Creamos el contenedor desacoplado
  **`docker run -d --name apache httpd`**
2. Nos conectamos y buscamos la carpeta `htdocs`:
```
$ docker exec apache bash
root@a31d58f35fea:/# find / -name htdocs
/usr/local/apache2/htdocs
```
3. Vamos a recrear el contenedor, primero lo borramos: **`docker rm apache`**.
4. Creamos una carpeta con contenido: **`mkdir htdocs && echo "Hola mundo" > htdocs/index.html`**
5.
```
docker run --name apache   \
  -v "$(pwd)/htdocs:/usr/local/apache2/htdocs" \
  -p 8001:80 \
  httpd
```

# Creando Imágenes Propias (a.k.a.`Dockerfile`s)

* Un `Dockerfile` es un archivo que define como crear una nueva imagen.
* Dentro de un `Dockerfile` se definen un conunto de líneas de la forma `<COMANDO> <ARGUMENTOS>...`, algunos comandos son:

    - **`FROM`** imagen base, se suele acompañar de `MAINTAINER`
    - **`ADD`** y **`COPY`** descargar y agregar un archivo a la imagen
    - **`RUN`** ejecutar un comando
    - **`EXPOSE`** exponer un puerto
    - **`CMD`** y **`ENTRYPOINT`** comando por defecto
    - **`USER`** y **`WORKDIR`** definen el usuario y directorio de trabajo por defecto.
    - **`VOLUME`** para definir directorios persistentes

[^whydot]: El . define el directorio actual dónde se buscará el `Dockerfile`

# Ejemplo básico

```docker
FROM debian:latest
MAINTAINER <someone@somewhere.net>

RUN apt-get update -qq
RUN apt-get install -qq -y build-essential
RUN adduser user
USER user
WORKDIR /home/user
ADD ./src /home/user/src
RUN gcc src/mi_programa.c -o mi_programa
CMD ["/home/user/mi_programa"]
```

* Una vez conformado el `Dockerfile` se ejecuta `build` dándole un nombre a la imagen producida [^whydot]
```
docker build -t mi_c .
```

# Ejemplo básico (cont)

* Ahora podemos ejecutar nuestra imagen con `docker run -ti mi_c`.
  - Si le damos un nombre, también nos podemos *"attachar"* y lanzar más comandos.



# Ejemplo de extensión de `Dockerfile`

```docker
FROM httpd
MAINTAINER <someone@somewhere.net>
ADD ./htdocs /usr/local/apache2/htdocs
```

* Como no definimos `RUN` lo heredamos de la imagen `httpd`,  simplemente ejecutamos `docker build -t mi_apache .`.


# **Big Picture**\texttrademark de Distribución

![Esquema de Distribución de Contenedores](images/docker_struct.eps)



# Docker - Contenedores vs Imagenes

## Imagen

 * Una *imagen* es la definición del sistema de archivos para un contenedor.
 * Una imagen suele tener un nombre y una etiqueta que identifica su versión.
 * `docker pull busybox` ()
 * `docker images`

## Contenedor

 * Es una instancia de ejecución de una imagen.
 * `docker run -ti busybox sh`
 * `docker run -ti ubuntu /bin/bash`

# `Dockerfile`

## Ejemplo:

```bash
FROM ubuntu:16.04
RUN apt-get install python2
RUN useradd foo
COPY miscript.py /home/foo/miscript.py
RUN chown /home/foo/miscript.py
RUN chmod +x /home/foo/miscript.py
CMD ["python2", "/tmp/miscript.py"]
```

## Creando la imagen

 * `docker build -t miproyecto .`
 * `docker run `

# Filesystem Read Only

## Volumes
 * Los volumenes son la forma de tener persistencia en Docker.

## Commit
 * Permite editar los pasos realizados en una imagen [`doc`]((https://docs.docker.com/engine/reference/commandline/commit/))


# Docker Compose

`docker-compose` permite definir en un archivo JSON, YAML o INI una configuración de uno o mas contenedores.

```yaml
version: '2'
services:
  web:
    build: .
    ports:
    - "5000:5000"
    volumes:
    - .:/code
    links:
    - redis
  redis:
    image: redis
```

#

## Demo

#

## Gracias
