@Library("To-do") _

pipeline 
{
    agent any

    stages 
    {
        stage('Docker build') 
        {
            steps 
            {
                script
                {
                    build("vatsal","latest","vatsalsolanki3")
                }
            }
        }

        stage('Docker push') 
        {
            steps 
            {
                script
                {
                    push("vatsal","latest","vatsalsolanki3")
                }
            }
        }

        stage('Deploy to nginx')
        {
            steps
            {
                sh '''

                    echo "Stopping container if already exists"
                    docker rm -f vatsal || true

                    echo "Pulling latest image"
                    docker pull vatsalsolanki3/vatsal:latest

                    echo "Running the container via NGINX"
                    docker run -d --name vatsal --network pav vatsalsolanki3/vatsal:latest

                    echo "Restarting NGINX"
                    sudo systemctl restart nginx

                '''
            }
        }
    }
}
