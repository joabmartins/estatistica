# Publicando na VPS com Kubernetes (K3s) e Nginx
Este guia detalha os passos para implantar sua aplicação Spring Boot (backend) e Angular (frontend) em uma Virtual Private Server (VPS) usando K3s (um Kubernetes leve), Nginx Ingress Controller e Cert-Manager para HTTPS, com automação via GitLab CI/CD.

## Pré-requisitos (Na VPS)
Certifique-se de que a VPS esteja acessível via SSH e que você tenha permissões de sudo.

1. Atualizar o Sistema Operacional:


```
sudo apt update && sudo apt upgrade -y
```
2. Instalar o Docker (necessário para o K3s):

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Reinicie a sessão SSH ou faça logout/login para a mudança do grupo ter efeito.
```
3. Instalar o K3s (Kubernetes Leve):

```
curl -sfL https://get.k3s.io | sh -
# Verifique a instalação
sudo kubectl get nodes
```
4. Configurar o kubectl (para interagir com o cluster K3s):

```
echo "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml" >> ~/.bashrc
source ~/.bashrc
# Teste novamente
kubectl get nodes
```
## Configuração da Aplicação
### Spring Boot (Backend)
Você não precisa de configurações específicas no Spring Boot para Kubernetes, mas o CORS é essencial para a comunicação com o frontend Angular.

1. Porta: Verifique se seu Spring Boot escuta na porta 8080 (padrão). Se necessário, configure em application.properties ou application.yml:

Properties
```
server.port=8080
```
2. CORS: Adicione a seguinte configuração CORS no seu projeto Spring Boot (exemplo em uma classe @Configuration):

Java
```
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Aplica CORS a todos os endpoints
                .allowedOrigins("http://seu-dominio.com", "https://seu-dominio.com") // Substitua pelo seu domínio
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }
}
```
Lembre-se de substituir seu-dominio.com pelo seu domínio real.

### Angular (Frontend)
Seu Angular será servido por um container Nginx.

 - angular.json: Verifique se outputPath em architect.build.options aponta para a pasta correta (geralmente dist/nome-do-seu-projeto).
 - Variáveis de Ambiente: Configure as URLs da sua API Spring Boot no environment.prod.ts do Angular para apontar para o domínio público da sua aplicação.

## Manifestos Kubernetes (YAMLs)
Crie os seguintes arquivos .yaml na raiz do seu repositório ou em uma pasta dedicada (k8s/):

1. Namespace (Opcional, mas boa prática)
namespace.yaml

YAML
```
apiVersion: v1
kind: Namespace
metadata:
  name: tcc-app
```
2. Spring Boot Backend
spring-deployment.yaml

YAML
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-backend-deployment
  namespace: tcc-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spring-backend
  template:
    metadata:
      labels:
        app: spring-backend
    spec:
      containers:
      - name: spring-backend
        image: seu-repositorio-docker/spring-backend:latest # IMAGEM DO SEU SPRING BOOT
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "200m"
```
spring-service.yaml

YAML
```
apiVersion: v1
kind: Service
metadata:
  name: spring-backend-service
  namespace: tcc-app
spec:
  selector:
    app: spring-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080 # Porta interna do container Spring Boot
  type: ClusterIP
```
3. Angular Frontend
Crie um Dockerfile e um nginx.conf no diretório raiz do seu projeto Angular:

Dockerfile (no projeto Angular):

Dockerfile
```
# Estágio de build do Angular
FROM node:18-alpine as builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build -- --configuration=production # Gera os arquivos estáticos na pasta dist

# Estágio de produção com Nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf # Copia a configuração do Nginx
COPY --from=builder /app/dist/seu-projeto-angular /usr/share/nginx/html # Copia os arquivos do Angular

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
Importante: Substitua seu-projeto-angular pelo nome da pasta de saída do seu build (verifique em angular.json).

nginx.conf (no projeto Angular, junto ao Dockerfile):

Nginx
```
server {
    listen 80;
    server_name localhost; # Isso será substituído pelo Ingress

    root /usr/share/nginx/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ /index.html; # Necessário para aplicações SPA como Angular
    }
}
```
Manifestos Kubernetes para Angular:

angular-deployment.yaml

YAML
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: angular-frontend-deployment
  namespace: tcc-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: angular-frontend
  template:
    metadata:
      labels:
        app: angular-frontend
    spec:
      containers:
      - name: angular-frontend
        image: seu-repositorio-docker/angular-frontend:latest # IMAGEM DO SEU ANGULAR COM NGINX
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "256Mi"
            cpu: "200m"
          requests:
            memory: "128Mi"
            cpu: "100m"
```
angular-service.yaml

YAML
```
apiVersion: v1
kind: Service
metadata:
  name: angular-frontend-service
  namespace: tcc-app
spec:
  selector:
    app: angular-frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80 # Porta interna do container Nginx do Angular
  type: ClusterIP
```
4. Nginx Ingress Controller e Ingress Resource
O K3s já vem com o Traefik como Ingress Controller padrão. Para simplicidade, usaremos ele.

ingress.yaml

YAML
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tcc-ingress
  namespace: tcc-app
  annotations:
    # Para o Cert-Manager emitir certificados Let's Encrypt
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: traefik # Assumindo Traefik como Ingress Controller padrão do K3s
  rules:
  - host: seu-dominio.com # SUBSTITUA PELO SEU DOMÍNIO
    http:
      paths:
      - path: /api # Para o backend Spring Boot
        pathType: Prefix
        backend:
          service:
            name: spring-backend-service
            port:
              number: 80 # Porta do Service, não do container
      - path: / # Para o frontend Angular
        pathType: Prefix
        backend:
          service:
            name: angular-frontend-service
            port:
              number: 80 # Porta do Service
  tls: # Configuração para HTTPS (Cert-Manager cuidará disso)
  - hosts:
    - seu-dominio.com
    secretName: tcc-tls-secret # Será criado pelo Cert-Manager
```
5. Configurando HTTPS com Cert-Manager
 - Instalar Cert-Manager (na VPS):

Bash
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml # Verifique a versão mais recente
```
Aguarde os pods do Cert-Manager estarem Running.

 - Criar ClusterIssuer (na VPS):

cluster-issuer.yaml

YAML
```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: seu-email@exemplo.com # SEU EMAIL!
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: traefik # Ou nginx, dependendo do seu Ingress Controller
```
Aplique: kubectl apply -f cluster-issuer.yaml

## GitLab CI/CD Pipeline (.gitlab-ci.yml)
Configure seu pipeline para construir as imagens Docker, enviá-las para um registry (ex: Docker Hub) e implantar no seu cluster K3s na VPS.

YAML
```
stages:
  - build
  - deploy

variables:
  DOCKER_HUB_USERNAME: seu-usuario-dockerhub # Substitua pelo seu usuário ou nome do registry
  DOCKER_REGISTRY_IMAGE_SPRING: $DOCKER_HUB_USERNAME/spring-backend:$CI_COMMIT_SHORT_SHA
  DOCKER_REGISTRY_IMAGE_ANGULAR: $DOCKER_HUB_USERNAME/angular-frontend:$CI_COMMIT_SHORT_SHA
  SSH_HOST: seu-ip-da-vps # Substitua pelo IP público ou domínio da VPS
  SSH_USER: seu-usuario-ssh-na-vps # Ex: ubuntu, root, etc.

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD # DOCKER_HUB_PASSWORD deve ser uma variável segura do GitLab
    # Build e push do Spring Boot
    - docker build -t $DOCKER_REGISTRY_IMAGE_SPRING ./spring-backend-project # Caminho para a pasta do seu projeto Spring
    - docker push $DOCKER_REGISTRY_IMAGE_SPRING
    # Build e push do Angular
    - docker build -t $DOCKER_REGISTRY_IMAGE_ANGULAR ./angular-frontend-project # Caminho para a pasta do seu projeto Angular
    - docker push $DOCKER_REGISTRY_IMAGE_ANGULAR
  only:
    - main # Ou a branch que você usa para deploy

deploy:
  stage: deploy
  image: alpine/git # Imagem leve com SSH. Você pode precisar de outras ferramentas.
  before_script:
    # Instala SSH e kubectl no runner
    - apk add --no-cache openssh-client
    - apk add --no-cache curl
    - curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    - chmod +x kubectl
    - mv kubectl /usr/local/bin/
    # Configura SSH para acesso à VPS
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa # SSH_PRIVATE_KEY deve ser uma variável segura do GitLab
    - chmod 600 ~/.ssh/id_rsa
    - echo -e "Host *\n\tStrictHostKeyChecking no\n" > ~/.ssh/config # Desabilita a verificação de host (para TCC, NÃO RECOMENDADO EM PRODUÇÃO)
    # Copiar o kubeconfig da VPS para o runner e configurá-lo
    - scp ~/.ssh/id_rsa $SSH_USER@$SSH_HOST:/etc/rancher/k3s/k3s.yaml ~/.kubeconfig
    - export KUBECONFIG=~/.kubeconfig # Define a variável de ambiente para o kubectl
  script:
    # Atualizar as referências das imagens nos manifestos com o hash do commit atual
    - sed -i "s|seu-repositorio-docker/spring-backend:latest|$DOCKER_REGISTRY_IMAGE_SPRING|" k8s/spring-deployment.yaml # Ajuste o caminho se necessário
    - sed -i "s|seu-repositorio-docker/angular-frontend:latest|$DOCKER_REGISTRY_IMAGE_ANGULAR|" k8s/angular-deployment.yaml # Ajuste o caminho se necessário
    # Aplicar os manifestos Kubernetes
    - kubectl apply -f k8s/namespace.yaml # Ajuste o caminho se necessário
    - kubectl apply -f k8s/spring-deployment.yaml
    - kubectl apply -f k8s/spring-service.yaml
    - kubectl apply -f k8s/angular-deployment.yaml
    - kubectl apply -f k8s/angular-service.yaml
    - kubectl apply -f k8s/ingress.yaml
    - kubectl apply -f k8s/cluster-issuer.yaml
  only:
    - main
```
Variáveis Seguras do GitLab CI/CD:

Nas configurações do seu projeto GitLab, vá em Settings > CI/CD > Variables e adicione:

 - DOCKER_HUB_PASSWORD: A senha do seu Docker Hub ou um Token de Acesso Pessoal.
 - SSH_PRIVATE_KEY: A chave privada SSH correspondente à chave pública que você colocou na VPS do professor (~/.ssh/authorized_keys na VPS). Mantenha essa chave extremamente segura!
### Apontamento de Domínio
1. Obtenha o IP da VPS: Anote o endereço IP público da VPS.
2. Configure o DNS: Acesse o painel de controle do seu provedor de domínio (onde você comprou o domínio) e crie um registro A apontando seu domínio principal (seu-dominio.com) para o IP da VPS.
3. Registro WWW (Opcional): Se quiser que www.seu-dominio.com funcione, crie um registro CNAME de www para seu-dominio.com.

### Testes e Verificação
Após o pipeline do GitLab concluir o deploy e o apontamento do domínio:

1. Verifique os Pods: Acesse a VPS via SSH e execute:

Bash
```
kubectl get pods -n tcc-app
```
Todos os pods (spring-backend-deployment-... e angular-frontend-deployment-...) devem estar no status Running.

2. Verifique os Services:

Bash
```
kubectl get services -n tcc-app
```

3. Verifique o Ingress:

Bash
```
kubectl get ingress -n tcc-app
```
Verifique se o tcc-ingress tem um endereço (ADDRESS). Este endereço deve ser o IP da sua VPS.

4. Acesse o site: Abra http://seu-dominio.com e https://seu-dominio.com no seu navegador. Se o HTTPS não funcionar de imediato, pode ser que o Cert-Manager ainda esteja emitindo o certificado (pode levar alguns minutos). Você pode verificar o status do certificado com:

Bash
```
kubectl get certificate -n tcc-app
kubectl describe certificate -n tcc-app tcc-tls-secret # ou o nome do seu secret
```

## Como o Spring Boot se comunicar com a API Python
O Spring Boot se comunicará com a API Python da mesma forma que se comunica com qualquer outra API externa: fazendo requisições HTTP.

Você usará bibliotecas HTTP client no Spring Boot para isso, como:

 - RestTemplate (legado, mas ainda funcional para casos simples): Para fazer requisições HTTP síncronas.
 - WebClient (recomendado, reativo e mais moderno): Parte do Spring WebFlux, ideal para requisições assíncronas e não-bloqueantes, melhor para performance e resiliência em microserviços.
Exemplo de comunicação com WebClient no Spring Boot:
Java
```
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class PythonApiService {

    private final WebClient webClient;

    // Injetar a URL da API Python via construtor ou @Value
    public PythonApiService(WebClient.Builder webClientBuilder) {
        // A URL base será configurada via variável de ambiente
        this.webClient = webClientBuilder.baseUrl(System.getenv("PYTHON_API_URL")).build();
    }

    public Mono<String> getDataFromPythonApi() {
        return webClient.get()
                .uri("/seu-endpoint-python") // O endpoint específico da sua API Python
                .retrieve()
                .bodyToMono(String.class); // Ou uma classe de objeto que represente a resposta
    }

    // Exemplo de como usar no Controller
    // @RestController
    // public class MyController {
    //     private final PythonApiService pythonApiService;
    //     public MyController(PythonApiService pythonApiService) {
    //         this.pythonApiService = pythonApiService;
    //     }
    //
    //     @GetMapping("/data-from-python")
    //     public Mono<String> getData() {
    //         return pythonApiService.getDataFromPythonApi();
    //     }
    // }
}
```
### Como colocar a variável de ambiente (PYTHON_API_URL)?
A chave aqui é que a URL da API Python será diferente dependendo do ambiente (local, VPS, etc.). Por isso, variáveis de ambiente são a melhor prática.

1. No Spring Boot (código)
Conforme o exemplo acima, o Spring Boot deve ler a URL da API Python de uma variável de ambiente.

 - Usando System.getenv() (simples):

Java
```
// No construtor ou método de configuração do WebClient
String pythonApiUrl = System.getenv("PYTHON_API_URL");
this.webClient = webClientBuilder.baseUrl(pythonApiUrl).build();
```
 - Usando @Value (recomendado Spring):

Java
```
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class PythonApiService {

    private final WebClient webClient;

    public PythonApiService(@Value("${python.api.url}") String pythonApiUrl, WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl(pythonApiUrl).build();
    }

    // ... resto da classe
}
```
Com @Value, o Spring tentará encontrar uma propriedade chamada python.api.url. Esta propriedade pode vir de diversas fontes, incluindo variáveis de ambiente (o que é ideal para o Docker/Kubernetes).

2. No application.properties (para desenvolvimento local)
Para facilitar o desenvolvimento local, você pode definir um valor padrão no seu application.properties:

application.properties

Properties
```
python.api.url=http://localhost:5000 # Ou a porta que sua API Python roda localmente
```
Quando o Spring Boot for executado em um ambiente onde a variável de ambiente PYTHON_API_URL (ou python.api.url se usar @Value e mapeamento automático) estiver definida, o valor da variável de ambiente terá precedência sobre o valor no application.properties.

3. No Container Docker (e qual container Docker)
A variável de ambiente PYTHON_API_URL deve ser definida no container Docker do Spring Boot, pois é ele quem precisa se comunicar com a API Python.

No seu manifesto Kubernetes (spring-deployment.yaml):

YAML
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-backend-deployment
  namespace: tcc-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spring-backend
  template:
    metadata:
      labels:
        app: spring-backend
    spec:
      containers:
      - name: spring-backend
        image: seu-repositorio-docker/spring-backend:latest
        ports:
        - containerPort: 8080
        env: # <--- Adicione esta seção
        - name: PYTHON_API_URL # Nome da variável de ambiente que o Spring Boot vai ler
          value: "http://python-api-service.tcc-app.svc.cluster.local:5000" # <--- URL interna do serviço Python
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "200m"
```
Explicação da value da variável de ambiente:

 - http://python-api-service.tcc-app.svc.cluster.local:5000
     - python-api-service: É o nome do Kubernetes Service que você criará para sua API Python.
     - tcc-app.svc.cluster.local: É o nome de domínio completo (FQDN) padrão de um serviço dentro do mesmo cluster Kubernetes. tcc-app é o namespace onde seu serviço Python estará, svc indica que é um serviço, e cluster.local é o sufixo de domínio padrão do cluster.
     - 5000: É a targetPort do seu serviço Kubernetes do Python (a porta que a API Python escuta internamente no seu container).
Você precisará criar um Deployment e um Service Kubernetes para sua API Python, semelhante ao que você fez para o Spring Boot.

Exemplo de manifestos Kubernetes para a API Python:
python-api-deployment.yaml
YAML
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-api-deployment
  namespace: tcc-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-api
  template:
    metadata:
      labels:
        app: python-api
    spec:
      containers:
      - name: python-api
        image: seu-repositorio-docker/python-api:latest # Imagem Docker da sua API Python
        ports:
        - containerPort: 5000 # A porta que sua aplicação Python escuta (ex: Flask, FastAPI)
        resources:
          limits:
            memory: "256Mi"
            cpu: "200m"
          requests:
            memory: "128Mi"
            cpu: "100m"
```
python-api-service.yaml
YAML
```
apiVersion: v1
kind: Service
metadata:
  name: python-api-service # Este é o nome do serviço usado na URL interna
  namespace: tcc-app
spec:
  selector:
    app: python-api
  ports:
    - protocol: TCP
      port: 5000 # Porta que outros serviços do cluster usarão para acessar a API Python
      targetPort: 5000 # Porta interna do container Python
  type: ClusterIP # Este serviço não precisa ser exposto externamente, apenas dentro do cluster
```

## Passos Adicionais para a API Python:
1. Crie um Dockerfile para sua API Python:

Dockerfile
```
# Exemplo para Flask/FastAPI
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000 # A porta que sua aplicação Python irá escutar
CMD ["python", "app.py"] # Ou "gunicorn", "uvicorn", etc.
```
Ajuste a porta (5000) e o comando CMD conforme o framework Python que você está usando (Flask, FastAPI, Django, etc.).

2. Atualize seu GitLab CI/CD:
Adicione estágios para construir e fazer push da imagem Docker da sua API Python, e depois aplique os novos manifestos Kubernetes (python-api-deployment.yaml e python-api-service.yaml) no estágio de deploy.

Exemplo de adição no .gitlab-ci.yml:

YAML
```
variables:
  # ...
  DOCKER_REGISTRY_IMAGE_PYTHON: $DOCKER_HUB_USERNAME/python-api:$CI_COMMIT_SHORT_SHA # Nova variável

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD
    # Build e push do Spring Boot
    - docker build -t $DOCKER_REGISTRY_IMAGE_SPRING ./spring-backend-project
    - docker push $DOCKER_REGISTRY_IMAGE_SPRING
    # Build e push do Angular
    - docker build -t $DOCKER_REGISTRY_IMAGE_ANGULAR ./angular-frontend-project
    - docker push $DOCKER_REGISTRY_IMAGE_ANGULAR
    # Build e push do Python API (novo)
    - docker build -t $DOCKER_REGISTRY_IMAGE_PYTHON ./python-api-project # Caminho para a pasta do seu projeto Python
    - docker push $DOCKER_REGISTRY_IMAGE_PYTHON
  only:
    - main

deploy:
  stage: deploy
  image: alpine/git
  before_script:
    # ... (mesmas configurações SSH e kubectl)
  script:
    # ... (atualizar sed para as novas imagens)
    - sed -i "s|seu-repositorio-docker/python-api:latest|$DOCKER_REGISTRY_IMAGE_PYTHON|" k8s/python-api-deployment.yaml # Novo sed
    # Aplicar os manifestos Kubernetes
    - kubectl apply -f k8s/namespace.yaml
    - kubectl apply -f k8s/spring-deployment.yaml
    - kubectl apply -f k8s/spring-service.yaml
    - kubectl apply -f k8s/angular-deployment.yaml
    - kubectl apply -f k8s/angular-service.yaml
    - kubectl apply -f k8s/python-api-deployment.yaml # Novo
    - kubectl apply -f k8s/python-api-service.yaml # Novo
    - kubectl apply -f k8s/ingress.yaml
    - kubectl apply -f k8s/cluster-issuer.yaml
  only:
    - main
```
Ao seguir esses passos, seu Spring Boot será capaz de se comunicar com sua API Python de forma eficiente e segura dentro do cluster Kubernetes, utilizando variáveis de ambiente para a configuração da URL.