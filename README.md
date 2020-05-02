# ImageNet on Kubernetes

## Starting services and setting up

* Create a terminal at this location (the root of the git folder)

* If you use Windows 10 Home or earlier, start up your Docker-Toolbox first. You can skip this step for Windows 10 Pro/Linux/MacOS

* Start up minikube

```
minikube start
```

* Once minikube is up, connect your minikube docker daemon to the terminal. On Linux/MacOS -

```
eval $(minikube docker-env)
```

* On Windows PowerShell -

```
minikube docker-env | Invoke-Expression
```

## Building and running docker image and Kubernetes deployment

* Now that the minikube docker daemon is connected to the terminal, build the docker image to be used by kubernetes -

```
docker build -t imagenet-inference .
```

* Deploy the kubernetes deployment with the imagenet-deployment.yaml file -

```
kubectl create -f imagenet-deployment.yaml
```

* Setup the service to expose the app

```
kubectl expose deployment imagenet-deployment --type=LoadBalancer --port=8080
```

* Get the IP of the deployment from minikube

```
minikube service imagenet-deployment --url
```

* You will see an IP similar to `http://192.168.99.101:30419`. For the rest of these instructions, I will use this same IP, please substitute it with the IP and port you get.

## Endpoint and prediction

* Paste the IP you get into the browser to see the welcome message `ImageNet Inference with AlexNet`

* To predict with an image - put in `/predict?url=` at the end of the IP and port and then the link to the image. For this test dog image I used, here is the example for a full link (don't forget to replace the IP and port with yours) -

```
http://192.168.99.101:30419/predict?url=https://www.petmd.com/sites/default/files/senior-golden-retriever-with-ball-picture-id488657289.jpg
```

* Depending on the pod you end up in, the model and the image you passed will download first, and this might take time. Please wait until the downloads are complete and the prediction is made. You will see a result on the screen like this -

```
Label: golden retriever | Confidence: 36.70255243778229%
```

* You can also curl for the command-line results if necessary.

## Stopping the service, deployment and minikube

* Stop the service -

```
kubectl delete service imagenet-deployment
```

* Stop the deployment -

```
kubectl delete deployment imagenet-deployment
```

* Stop Minikube -

```
minikube stop
```

* If you started the docker-toolbox, stop the docker VM from its terminal -

```
docker-machine stop
```

* Clean up the images too if necessary before stopping the minikube instance
