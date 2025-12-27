pipeline {
  agent {
    kubernetes {
      namespace 'jobs'
      defaultContainer 'py'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  nodeSelector:
    cloud.google.com/gke-nodepool: jobs-pool
  containers:
    - name: py
      image: python:3.12-slim
      command: ['sh', '-c', 'cat']
      tty: true
    - name: kaniko
      image: gcr.io/kaniko-project/executor:debug
      command: ['/busybox/cat']
      tty: true
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker
  volumes:
    - name: docker-config
      secret:
        secretName: nexus-regcred
        items:
          - key: .dockerconfigjson
            path: config.json
"""
    }
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    skipDefaultCheckout(true)
  }

  environment {
    REGISTRY   = "nexus.drop-robot.com"
    IMAGE_NAME = "drop-robot/crawler"
    IMAGE_TAG  = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    IMAGE      = "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install') {
      steps {
        container('py') {
          sh '''
            set -eux
            python -V
            pip install -U pip
            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          '''
        }
      }
    }

    stage('Lint') {
      steps {
        container('py') {
          sh '''
            set -eux
            pip install -U ruff
            ruff check .
          '''
        }
      }
    }

    stage('Tests') {
      steps {
        container('py') {
          sh '''
            set -eux
            pip install -U pytest
            pytest -q
          '''
        }
      }
    }

    stage('Build Image (Kaniko)') {
      steps {
        container('kaniko') {
          sh '''
            set -eux
            /kaniko/executor \
              --context "${WORKSPACE}" \
              --dockerfile "${WORKSPACE}/Dockerfile" \
              --destination "${IMAGE}" \
              --cache=true \
              --cache-ttl=24h
          '''
        }
      }
    }

    stage('Tag latest (main only)') {
      when { branch 'main' }
      steps {
        container('kaniko') {
          sh '''
            set -eux
            /kaniko/executor \
              --context "${WORKSPACE}" \
              --dockerfile "${WORKSPACE}/Dockerfile" \
              --destination "${REGISTRY}/${IMAGE_NAME}:latest" \
              --cache=true \
              --cache-ttl=24h
          '''
        }
      }
    }
  }

  post {
    always {
      echo "Built image: ${env.IMAGE}"
    }
  }
}
