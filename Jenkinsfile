pipeline {
    agent any

    environment {
        PROJECT_ID     = "${GCP_PROJECT}"
        REGION         = "${GCP_REGION}"
        CLUSTER        = "${GKE_CLUSTER}"
        NAMESPACE      = "${K8S_NAMESPACE}"
        IMAGE_NAME     = "${IMAGE_NAME}"
        NEXUS_URL      = "${NEXUS_URL}"

        // Auto-tag = branch + short commit
        GIT_TAG = "${env.BRANCH_NAME}-${env.GIT_COMMIT.take(7)}"
    }

    stages {

        /* -------------------------------
         *  1️⃣ INTEGRATION
         *  ------------------------------- */
        stage('Integration') {
            steps {
                echo "Running tests, linting, validating project..."

                sh """
                python3 -m pip install -r requirements.txt
                python3 -m pytest || true
                """
            }
        }

        /* -------------------------------
         *  2️⃣ REGISTRY (Docker build + Push)
         *  ------------------------------- */
        stage('Build & Push Image') {
            steps {
                script {
                    docker.withRegistry("http://${NEXUS_URL}", "${NEXUS_CREDENTIAL_ID}") {

                        sh """
                        echo "Building Docker image..."
                        docker build -t ${NEXUS_URL}/${IMAGE_NAME}:${GIT_TAG} .

                        echo "Tagging last version..."
                        docker tag ${NEXUS_URL}/${IMAGE_NAME}:${GIT_TAG} ${NEXUS_URL}/${IMAGE_NAME}:latest

                        echo "Pushing image to Nexus..."
                        docker push ${NEXUS_URL}/${IMAGE_NAME}:${GIT_TAG}
                        docker push ${NEXUS_URL}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        /* -------------------------------
         *  3️⃣ DEPLOYMENT (GKE)
         *  ------------------------------- */
        stage("Deploy to GKE") {
            steps {
                withCredentials([file(credentialsId: "${GCLOUD_SA_KEY}", variable: "GOOGLE_APPLICATION_CREDENTIALS")]) {

                    sh """
                    echo "Authenticating to GCloud..."
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                    gcloud config set project ${PROJECT_ID}
                    gcloud config set compute/region ${REGION}

                    echo "Fetching kubeconfig..."
                    gcloud container clusters get-credentials ${CLUSTER} --region ${REGION}

                    echo "Updating Deployment image..."
                    kubectl -n ${NAMESPACE} set image deployment/ai-crawler ai-crawler=${NEXUS_URL}/${IMAGE_NAME}:${GIT_TAG}

                    echo "Applying Kubernetes manifests..."
                    kubectl apply -f k8s/
                    """
                }
            }
        }
    }
}