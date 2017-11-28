Requiere de Docker, la interfaz de linea de comando de google en su computadora y kubernetes (se instala con gcloud)

Para desarrollar este proyecto requiere de una cuenta en google cloud plataform. Luego cree un proyecto en la consola de google.
Ademas cree (si en caso no tenga) su cuenta en docker hub.
#En su maquina local:
1. clonar el proyecto en su maquina local:
git clone https://github.com/vitohuanqui/cloudfinal.git
1.1 Realizaremos la configuracion de los dockers para luego ser usadas en la plataforma de google.
1.2 en containers/database se encontrara el docker file necesario para crear la imagen de la base de datos (postgres)
1.3 docker build -t {docker_hub_account}/postgresql:9.5
1.4 creamos la cuenta :
docker run --name database -e POSTGRES_DB=app_db -e POSTGRES_PASSWORD=app_db_pw -e POSTGRES_USER=app_db_user -d {identifier}/postgresql:9.5
1.5 Pushiamos la imagen a nuestro docker hub
docker push {docker_hub_account}/postgresql:9.5
1.6 lo mismo realizamos con la aplicacion de Django:
docker build -t {docker_hub_account}/djangoapp .
1.7 y pusheamos el docker image
docker push {docker_hub_account}/djangoapp

2. Setear el proyecto creado en GCP(google cloud plataform) con el siguiente comando:
gcloud config set project {project_id}
3. crear cluster en tu nube google (grupo):
gcloud container clusters create {cluster_identifier}
4. para poder manejar el cluster de forma local configuramos kubernetes (kubectl):
gcloud container clusters get-credentials {cluster_identifier}

conecctamos docker con kubectl osea con nuestra cluster---- DEPLOYAR  cluster
kubectl create -f instance_template_database.yaml
y creamos el servicio
kubectl create -f service.yaml

ahora la app
kubectl create -f instance_template.yaml
kubectl create -f service.yaml
kubectl get pods -> sacamos ip del cluster

kubectl exec ip-cluster -- python /app/manage.py migrate

para scalar mecanicamente usamos: 	
kubectl scale rc APP --replicas=NUM

IMPORANTE:
para testear el autoescalamiento usar:
while true; do (curl http://{ip externa}/ &); sleep 0.01; done