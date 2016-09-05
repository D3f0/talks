# Dockerfile
DOKER_IMAGE=kivy
# Instalación de un aptcacher NG
PROXY_HOST=172.16.18.192
PORXY_PORT=3142
PROXY=${PROXY_HOST}:${PORXY_PORT}

.PHONY=cache_check docker shell
all: docker

build: set_proxy_config
	docker build $(DOCKER_BUILD_EXTRA_ARGS) --build-arg LOCAL_USER_ID=`id -u` -t ${DOKER_IMAGE} .

build_no_cache: set_proxy_config
	$(eval DOCKER_BUILD_EXTRA_ARGS="--no-cache")
	docker build $(DOCKER_BUILD_EXTRA_ARGS) --build-arg LOCAL_USER_ID=`id -u` -t ${DOKER_IMAGE} .


shell:
	$(info Lanzando bash...)
	docker run -ti ${DOKER_IMAGE} bash

set_proxy_config:
	@if python -c "from socket import socket; \
	s = socket(); s.settimeout(1); \
	s.connect(('${PROXY_HOST}', ${PORXY_PORT})); \
	s.close()" 2>/dev/null; then \
		PROXY_LINE='Acquire::http { Proxy "http://${PROXY}"; };'; \
		if ! grep 'Acquire::http { Proxy "http://${PROXY}"; };' etc/apt/apt.conf.d/01proxy >/dev/null ; then \
			echo "Estableciendo información de Proxy"; \
			echo 'Acquire::http { Proxy "http://${PROXY}"; };' > etc/apt/apt.conf.d/01proxy; \
		else \
			echo "Infomracion de Proxy OK"; \
		fi ; \
	else \
		if ! cat etc/apt/apt.proxy.conf/01proxy | grep "Acquire::http" ;  then \
			echo "Eliminando proxy" ; \
			echo '' > etc/apt/apt.conf.d/01proxy; \
		fi \
	fi

