
pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-2'
        AWS_ACCOUNT_ID = '201971881499'
        ECR_REPO       = 'myapp'
        IMAGE_TAG      = "${BUILD_NUMBER}"
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
        ECR_REGISTRY   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                sh '''
                    aws ecr get-login-password \
                        --region ${AWS_REGION} |
                    docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag ${ECR_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s|IMAGE_TAG|${IMAGE_TAG}|g" \
                        deployment.yaml > deployment-rendered.yaml

                    kubectl --kubeconfig="${KUBECONFIG}" \
                        apply -f deployment-rendered.yaml

                    kubectl --kubeconfig="${KUBECONFIG}" \
                        rollout status deployment/myapp \
                        --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Image pushed to ECR and Kubernetes deployment completed!'
        }

        failure {
            echo 'FAILED: Check the Jenkins Console Output for the error.'
        }
    }
}

