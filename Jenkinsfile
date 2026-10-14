pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-2'
        AWS_ACCOUNT_ID = '201971881499'
        ECR_REPO       = 'myapp'
        IMAGE_TAG      = 'v2'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Nit-98/foreksdeploy.git'
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
                        --password-stdin \
                        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag ${ECR_REPO}:${IMAGE_TAG} \
                        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}

                    docker push \
                        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --kubeconfig="${KUBECONFIG}" \
                        set image deployment/myapp \
                        myapp=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}

                    kubectl --kubeconfig="${KUBECONFIG}" \
                        rollout status deployment/myapp \
                        --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD completed: Image pushed to ECR and deployed to Kubernetes!'
        }
        failure {
            echo 'CI/CD failed. Check the failed stage in the Jenkins console output.'
        }
    }
}
