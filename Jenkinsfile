pipeline {
agent any

environment {
    DOCKERHUB_USER    = 'sauravnirala'
    TODO_REPO         = 'pythoncalculator'
    IMAGE_TAG         = "${env.BUILD_NUMBER}"

    TODO_IMAGE        = "${DOCKERHUB_USER}/pythoncalculator:${IMAGE_TAG}"
    TODO_LATEST       = "${DOCKERHUB_USER}/pythoncalculator:latest"

    GIT_REPO_URL      = 'https://github.com/sauravnirala/calculatorwithpython.git'
    GIT_BRANCH        = 'main'

    K8S_NAMESPACE     = 'calapp'
    CAL_PORT          = '5000'
    SONARQUBE_ENV     = 'sq'
}

stages {

    stage('Checkout') {
        steps {
            echo "Cloning ${GIT_REPO_URL} @ ${GIT_BRANCH}"
            git branch: "${GIT_BRANCH}", url: "${GIT_REPO_URL}"
        }
    }

    stage('Install Dependencies') {
        steps {
            sh """
                pip install -r requirements.txt
                pip install --upgrade pip
            """
        }
    }

    stage('Test') {
        steps {
            sh """
               pip install pytest pytest-cov
               python3 -m pytest --cov=.
            """
        }
    }

    stage('Sonarqube Analysis') {
        steps {
            withSonarQubeEnv("${SONARQUBE_ENV}") {
                sh """
                /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonar-scanner/bin/sonar-scanner \
                  -Dsonar.projectKey=calculatorwithpython \
                  -Dsonar.sources=. \
                  -Dsonar.exclusions=venv/**,__pycache__/** \
                  -Dsonar.host.url=$SONAR_HOST_URL \
                  -Dsonar.login=$SONAR_AUTH_TOKEN
                """
            }
        }
    }

    stage('Quality Gate') {
        steps {
            timeout(time: 2, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }

    stage('Build Artifact') {
        steps {
            sh """
            pip3 install build setuptools wheel twine
            python3 -m build
            """
        }
    }

    stage('Upload to Nexus') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'nexuscred', passwordVariable: 'passwd', usernameVariable: 'username')]) {
                sh """
                python3 -m twine upload --repository-url http://13.200.137.224:8081/repository/pypi-hosted/ \
                -u $username -p $passwd dist/*
                """
            }
        }
    }

    stage('Build Docker Images') {
        steps {
            sh """
                docker build --no-cache -t ${TODO_IMAGE} -t ${TODO_LATEST} -f Dockerfile .
                echo "Built ${TODO_IMAGE}"
            """
        }
    }

    stage('Push to DockerHub') {
        steps {
            echo "Logging in to DockerHub as ${DOCKERHUB_USER}..."
            withCredentials([usernamePassword(
                credentialsId: 'dockerhub',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )]) {
                sh """
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${TODO_IMAGE}
                    docker push ${TODO_LATEST}
                    docker logout
                """
            }
        }
    }

    stage('Deploy to Kubernetes') {
        steps {
            sh """
                kubectl apply -f namespace.yml

                cp projectdeploy.yml /tmp/all-apps.yml

                sed -i 's|sauravnirala/pythoncalculator:v1|${TODO_IMAGE}|g' /tmp/all-apps.yml

                kubectl apply -f /tmp/all-apps.yml

                kubectl rollout status deployment/mycalcapp -n ${K8S_NAMESPACE}
            """
        }
    }

    // ================= NEW STAGES =================

    stage('Install Prometheus') {
        steps {
            sh """
            helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
            helm repo update

            helm upgrade --install prometheus prometheus-community/prometheus \
              -n monitoring --create-namespace \
              --set alertmanager.enabled=false \
              --set server.persistentVolume.enabled=false
            """
        }
    }

    stage('Install Grafana') {
        steps {
            sh """
            helm repo add grafana https://grafana.github.io/helm-charts || true
            helm repo update

            helm upgrade --install grafana grafana/grafana \
              -n monitoring \
              --set persistence.enabled=false
            """
        }
    }

    stage('Expose Monitoring') {
        steps {
            sh """
            nohup kubectl port-forward svc/prometheus-server 9090:80 -n monitoring --address 0.0.0.0 > prometheus.log 2>&1 &
            nohup kubectl port-forward svc/grafana 3000:80 -n monitoring --address 0.0.0.0 > grafana.log 2>&1 &
            """
        }
    }

    stage('Get Grafana Password') {
        steps {
            sh """
            kubectl get secret grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode > grafana_pass.txt
            cat grafana_pass.txt
            """
        }
    }
}

}
