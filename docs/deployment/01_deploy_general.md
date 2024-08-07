# Guide to Deploy ML Models through an API on a Cloud Provider

This guide provides step-by-step instructions to deploy ML models through an API using a virtual machine in a cloud provider. It assumes a general cloud provider setup and covers the following steps:

## Step 1: Choose a Cloud Provider

1. Research and select a cloud provider that best suits for you. Popular options include AWS, Azure, and Google Cloud Platform. In this repo we use the free-tier account from each considered provider. However, this limits the computational resources to work on.

2. Sign up for an account on the chosen cloud provider and follow the instructions to enable the free-tier access.

### Cloud Providers Comparison
| Cloud Provider | Free compute hours/month | Free GPU hours/month | Free storage                                   | Max Memory offered                  | Free tier duration  |
| -------------- | ------------------------ | -------------------- | ---------------------------------------------- | ----------------------------------- | ------------------- |
| AWS            | 750 hours                | 0                    | 5 GB (S3) and 30 GB (EBS)                      | 1 GB                                | 12 months           |
| Azure          | 750 hours                | 0                    | 5 GB (Blob Storage) and 128 GB (Managed disks) | 1 to 4 GB depending on the instance | 12 months           |
| GCP            | 750 hours                | 0                    | 30 GB                                          | 0.6 GB                              | 12 months + 300 USD |
| Okteto         | Unlimited                | 0                    | 5 GB                                           | 3 GB                                | Unlimited           |
| Virtech        | Unlimited                | 0                    | 20 GB                                          | 4 GB                                | 1 semester          |

For more information about the free-tier options of each cloud provider, please refer to the following official documentation.

## Step 2: Provision a Virtual Machine

1. Navigate to the cloud provider's management console.

2. Create a new virtual machine instance with the desired specifications (CPU, RAM, storage, ...). Ensure that you select the free-tier option if available.

3. Set up the virtual machine with the required operating system and configurations.

4. Note down the IP address or hostname of the virtual machine for future reference.

## Step 3: Connect via SSH to VM

1.  Generate your SSH keys
```shell
ssh-keygen -t ed25519 -f ~/.ssh/my-key -C "my_user@my_hostname"
```
2. Add your public ssh key (my-key.pub) into your cloud provider's allowed keys.
```shell
ssh-copy-id -i ~/.ssh/my-key.pub cloud_user@X.X.X.X
```
3. Connect to the VM using your private key and the public IP (X.X.X.X) of the VM
```shell
ssh -i ~/.ssh/my-key cloud_user@X.X.X.X
```
## Step 4: Clone the Repository

1. Install Git on the virtual machine if it's not already installed.

2. Clone the GitHub repository containing the ML model and API code using the following command:

```shell
git clone https://github.com/fjdurlop/deploy-GAISSA.git
```
## Step 5: Set Up the Environment

1. Create a virtual environment for the API using [venv](https://docs.python.org/3/library/venv.html), [virtualenv](https://virtualenv.pypa.io/en/latest/), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), [poetry](https://python-poetry.org/), or any other tool of your choice. For example, using venv:

```shell
python3 -m venv venv
```

2. Activate the virtual environment.

```shell
source venv/bin/activate
```

3. Install the necessary dependencies and packages required for running the API.

```shell
./scripts/setenv.sh
```

```shell

python3 -m pip install -r requirements.txt

```

## Step 6: Run the API

1. Change into the cloned repository directory on the virtual machine.

2. Start the API server:

    ```bash
    uvicorn app.api:app  --host 0.0.0.0 --port 80
    ```

## Step 7: Access the API
1. Open a web browser (http://X.X.X.X) or use a tool like cURL or Postman to make HTTP requests to the API endpoints.

2. Send requests to the API with the required input data and parameters to obtain predictions.

## Step 8: Conigure a proxy server (Optional)
1. Stop the API process. You can use tools like [htop](https://htop.dev/) to find the process id (PID) and kill it.

2. Install [nginx](https://www.nginx.com/) on the virtual machine. For example, on Ubuntu:
```shell
sudo apt update
sudo apt install nginx
```

3. Configure nginx
```shell
sudo vim /etc/nginx/sites-available/fastapi-app
```

4. Copy the following configuration into the file and replace the X.X.X.X with the IP address of your server.
```shell
server {
    listen 80;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    server_name X.X.X.X;

    location / {
        proxy_pass http://localhost:5000;
    }
}
```

Then run the following command to add a soft link into the sites-enabled folder of nginx:
```shell
sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/fastapi-app
```

5. Restart nginx
```shell
sudo systemctl restart nginx
```

6. Relaunch the API
```shell
uvicorn app.api:app  --host 0.0.0.0 --port 5000
```
