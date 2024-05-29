pwd
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
docker compose --version
ls
ls -l
sudo docker compose up -d
ls -l
sudo docker compose up -d
ls -l
cd jobs
ls -l
cd ..
ls -l
sudo docker exec -it azure-spark-worker-1 spark-submit --master-spark://172.18.0.2:7077 jobs/viz.py
sudo docker exec -it azureuser-spark-worker-1 spark-submit --master-spark://172.18.0.2:7077 jobs/viz.py
sudo docker exec -it azureuser-spark-worker-1 spark-submit --master spark://172.18.0.2:7077 jobs/viz.py
sudo docker compose up -d --build
sudo docker exec -it azureuser-spark-worker-1 spark-submit --master spark://172.18.0.2:7077 jobs/viz.py
