# System Architecture Diagram

This diagram shows the complete system architecture for deploying the application to a public cloud vendor like AWS using modern cloud-native services.

The diagram is written using [Mermaid](https://mermaid.js.org/) which can be [rendered by GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams):

```mermaid
graph TB

graph TB
    User[👤 End Users] --> Internet[🌐 Internet]

    subgraph Cloud["Cloud Platform"]
        Internet --> ALB[Load Balancer<br/>HTTPS & Routing]

        subgraph K8s["Kubernetes Cluster"]
            subgraph Namespace["sample-app Namespace"]
                subgraph App["FastAPI Application"]
                    Pod1[📦 App Pod 1]
                    Pod2[📦 App Pod 2]
                end

               AppSvc[🔗 App Service<br/>Port 8000]

                Ingress[Ingress Controller]

                Pod1 --> AppSvc
                Pod2 --> AppSvc
                AppSvc --> Ingress
            end
        end

        subgraph Database["Database"]
            DB[🗄️ PostgreSQL<br/>RDS or In-Cluster]
        end

        subgraph Registry["Container Registry"]
            Image[🐳 App Image]
        end
    end

    ALB --> Ingress
    Ingress --> AppSvc

    Pod1 --> DB
    Pod2 --> DB

    K8s -.->|Pull Image| Registry

```

## Architecture Components

The following architecture components can be used for a production-ready deployment of the application:

### **Compute & Orchestration**

- **Amazon EKS**: Managed Kubernetes cluster for container orchestration
- **FastAPI Pods**: Multiple replicas for high availability and load distribution
- **Helm Charts**: Package and deploy the application using stakater/application chart
- **Container Registry**: Store and manage Docker images (ECR, GCR, ACR, GHCR)

### **Networking**

- **VPC**: Isolated network with public/private subnets across multiple AZs
- **Route 53**: DNS management and domain routing
- **Application Load Balancer**: HTTPS termination, SSL/TLS, and traffic distribution
- **Ingress Controller**: NGINX-based ingress for Kubernetes service routing

### **Database**

- **Amazon RDS**: Managed database service for PostgreSQL deployment
- **In-Cluster PostgreSQL**: Cheaper alternative for development/testing environments

### **Monitoring & Observability**

- **Logging**: Centralized application logs
- **Metrics**: Performance monitoring and alerting
- **Health Checks**: Application and infrastructure health monitoring

### **Deployment Tools**

- **Terraform**: Infrastructure as Code for cloud resources
- **Helm**: Kubernetes package manager for application deployment
- **GitHub Actions**: CI/CD pipeline for automated deployments

## DevOps Flow

1. **Code Changes** → GitHub Actions triggers build
2. **Docker Build** → Image pushed to Container Registry
3. **Terraform** → Provisions cloud infrastructure
4. **Helm Deployment** → Deploys application to Kubernetes cluster
5. **Load Balancer** → Routes traffic to healthy pods
6. **Monitoring** → Monitoring system collects logs and metrics
