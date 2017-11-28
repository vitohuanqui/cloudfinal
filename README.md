Para desarrollar este proyecto requiere de una cuenta en google cloud plataform. Luego cree un proyecto en la consola de google.

#En su maquina local:
1. clonar el proyecto en su maquina local:
git clone 
1. Setear el proyecto proyecto con el siguiente comando 
crear cluster en tu nube google:
gcloud container clusters create demo
la sacas con list
gcloud container clusters list
configuramos kubectl para que se comunique ocn el cluister
gcloud container clusters get-credentials demo


SUBIR A DOCKER HUB los containers

kubectl get rc

conecctamos docker con kubectl osea con nuestra cluster---- DEPLLYAR  cluster
kubectl create -f replication-controller.yaml
y creamos el servicio
kubectl create -f service.yaml

ahora la apṕ
kubectl create -f replication-controller-orange.yaml
kubectl create -f service.yaml
kubectl get pods -> sacamos ip del cluster

kubectl exec ip-cluster -- python /app/manage.py migrate


kubectl scale rc APP --replicas=NUM