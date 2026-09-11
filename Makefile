CLUSTER_NAME := demo

.PHONY: all cluster deploy 

all: cluster deploy

cluster:
	kind create cluster --name $(CLUSTER_NAME) --config kind-multi-node.yaml

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml


status:
	@echo "Nodes"
	kubectl get nodes
	@echo ""
	@echo "Deployments"
	kubectl get deployments
	@echo ""
	@echo "Pods"
	kubectl get pods -o wide
	@echo ""
	@echo "Services"
	kubectl get services

logs:
	kubectl logs -l app=web --tail=100

clean:
	kind delete cluster --name $(CLUSTER_NAME)
