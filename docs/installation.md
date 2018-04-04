# Instalación
--------------

## Linux

Instalar dependencias previas:

```
sudo apt-get install git
sudo apt-get install apache2
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Instalar Python
```
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar xzf Python-2.7.13.tgz
cd Python-2.7.13
./configure
make
sudo make install
```

Instalar pip y virtualenv
```
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install virtualenvwrapper
```

Añadimos el virtualenv a nuestro perfil de bash (), añadiendo las siguientes líneas al final:
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Creamos nuestro virtualenv
```
mkvirtualenv musiccity
workon musiccity
```

Clonamos el repositorio
```
git clone https://github.com/InsulaCoworking/MusicCity.git
cd MusicCity
```

Instalamos mySQL (nos pedirá introducir la constraseña de root):
```
sudo apt-get install mysql-server
sudo apt-get install python-dev libmysqlclient-dev
sudo systemctl mysql start
```

Entramos en la consola de mySQL(`mysql -u root -p`) y creamos la base de datos:
```
create database musiccity;
grant all privileges on musiccity.* to 'insuler'@'localhost' identified by "insula";
```


Instalamos las dependencias del proyecto:
```
pip install -r requirements.txt
```

Realizamos las migraciones iniciales, copiamos los ficheros estáticos y creamos el usuario admin:
```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```


### Apache

Instalamos el módulo wsgi de Apache:
```
sudo apt-get install libapache2-mod-wsgi
```

Editamos el fichero de configuración de nuestro sitio (en este ejemplo el de por defecto)
```
sudo nano /etc/apache2/sites-available/000-default.conf
```

Dentro de este fichero, tenemos que añadir las reglas para configurar nuestra app de Django:
```
		Alias /static/ /home/username/static/
        Alias /media/ /home/username/media/
        WSGIScriptAlias / /home/username/MusicCity/musiccity/wsgi.py
        WSGIDaemonProcess musiccity python-home=/home/username/.virtualenvs/musiccity python-path=/home/username/MusicCity
        WSGIProcessGroup musiccity

        <Directory /home/username/MusicCity/musiccity>
         <Files wsgi.py>
            Require all granted
         </Files>
         </Directory>

		 <Directory /home/username/static>
           Require all granted
        </Directory>

        <Directory /home/username/media>
           Require all granted
        </Directory>
```

Una vez guardado, actualizamos el servicio de Apache:
```
sudo service apache2 restart
```

## Nginx

Creamos los directorios externos y añadimos al usuario al grupo web:

```
mkdir media
chmod +777 static/
chmod +777 media/
sudo usermod -aG www-data <username>
```

Creamos un directorio `configs` en el que almacenar las distintas configuraciones (que luego tendrán un enlace simbólico).
Para no tener que crearlos de cero, tenemos en el repositorio unos archivos de configuración de ejemplo
para Nginx y uWSGI que funcionan directamente:

```
mkdir congigs
cp MusicCity/docs/uwsgi_params configs/
cp MusicCity/docs/uwsgi.ini configs/
cp MusicCity/docs/nginx.conf configs/
```

Instalamos Nginx y copiamos los ficheros de configuración a los sitios disponibles y activos:

```
sudo apt-get install nginx
sudo /etc/init.d/nginx start
sudo ln -s /home/<username>/configs/nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
```

Instalamos uWSGI (**importante**: fuera del virtualenv) y añadimos los ficheros de configuración:

```
deactivate
sudo apt-get install libpcre3 libpcre3-dev
sudo pip install uwsgi
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/boniato/configs/uwsgi.ini /etc/uwsgi/vassals/
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data &
```

Si todo funciona correctamente, añadimos el emperor de uWSGI para que se ejecute al arranque del sistema, añadiendo
al final (justo antes de la instrucción `exit "0"`) del fichero `/etc/rc.local` la siguiente línea:

```
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
```
