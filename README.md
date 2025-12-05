# Easy VPS Deployment Guide for Business Analysis AI

This guide will walk you through deploying the Business Analysis AI on a Virtual Private Server (VPS). This tutorial is designed for users who may not have a deep background in server infrastructure. By the end, you'll have a private, running instance of the AI analyst.

## Part 1: Choosing Your Virtual Private Server (VPS)

### What is a VPS?
Think of a VPS as your own personal computer that lives in a professional data center, connected to the internet 24/7. You can rent one from various providers, giving you a clean slate to run applications like this one.

### Server Requirements
The AI model is the most resource-intensive part of this application. For the `Llama-3.2-1B` model used in this project, here are the recommended minimum server specifications:

*   **Operating System**: A modern Linux distribution (e.g., **Ubuntu 22.04 LTS**).
*   **CPU**: **2 vCPUs** or more.
*   **RAM**: **8 GB** of RAM. While the model might run on less, 8 GB provides a comfortable buffer for the operating system, Docker, and the AI model itself.
*   **Storage**: **30 GB SSD** or more. The base OS, Docker, and the AI models will take up several gigabytes.

### Recommended VPS Providers
You can get a VPS that meets these requirements from many cloud providers. Here are a few popular options known for their ease of use:
*   AWS
*   DigitalOcean
*   Linode (by Akamai)
*   Hetzner Cloud

Choose a provider, create an account, and "spin up" a new server with the Ubuntu 22.04 image and the specs listed above.

---

## Part 2: One-Time Server Setup

Once your VPS is running, the provider will give you an IP address. You'll use this to connect.

### Step 2.1: Connect to Your Server
Open a terminal on your local machine (Terminal on Mac/Linux, PowerShell or WSL on Windows) and connect to the server using SSH (Secure Shell).

```bash
ssh root@<your_vps_ip>
```
*(Replace `<your_vps_ip>` with the actual IP address of your server.)*

You may be asked to confirm the authenticity of the host. Type `yes` and press Enter. Then, provide the password given to you by your VPS provider.

### Step 2.2: Install Docker
Docker is the technology we'll use to run the application in isolated "containers." It makes deployment incredibly simple and clean.

Run the following commands to update your server and install Docker and Docker Compose.

```bash
# Update package lists
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker and Docker Compose
sudo apt-get install -y docker.io docker-compose
```

### Step 2.3: Add Your User to the Docker Group (Optional, but Recommended)
To avoid having to type `sudo` for every Docker command, you can add your user to the `docker` group.

```bash
# This command assumes you are logged in as a non-root user.
# If you are 'root', you can skip this.
sudo usermod -aG docker ${USER}

# You will need to log out and log back in for this to take effect.
exit
```
After running `exit`, reconnect to your server using the same `ssh` command as before.

---

## Part 3: Deploying the AI Application

Now for the exciting part! Let's get the application code and run it.

### Step 3.1: Clone the Project
First, you need to copy the project files onto your server. We'll do this using `git`. If you don't have `git` installed, you can install it with `sudo apt-get install -y git`.

```bash
git clone https://github.com/tndor/bas-ai.git
```
*(Note: This URL is a placeholder. Replace it with the actual URL of your Git repository if it's different.)*

### Step 3.2: Start the Application
Navigate into the newly created project directory and use a single command to start everything.

```bash
cd bas-ai
docker-compose up --build -d
```

### What's Happening in the Background?
This one command does a lot of work for you:
1.  **Builds the App**: Docker reads the `Dockerfile` to create a self-contained "image" of your Python application with all its dependencies.
2.  **Starts Services**: It reads the `docker-compose.yml` file and starts two services: `app` (your Flask API) and `ollama` (the AI engine).
3.  **Downloads the Model**: The startup script (`start.sh`) automatically tells the `ollama` service to download the `Llama-3.2-1B-Instruct-GGUF` model. This may take 5-10 minutes, depending on the server's network speed.
4.  **Exposes the App**: The `docker-compose.yml` file is configured to map port 80 on your VPS to the application's port 5000. This means you can access the app using the standard web port, without needing to specify a port number.

---

## Part 4: Getting Your First AI Analysis

Once the `docker-compose` command finishes, the application is live.

Open a web browser on your computer and navigate to the following URL:

**`http://<your_vps_ip>/chat`**

*(Again, replace `<your_vps_ip>` with your server's IP address.)*

The first request might be a bit slow as the AI model is loaded into memory. Subsequent requests will be faster. You should see a JSON response in your browser containing the full business analysis report.

---

## Part 5: Managing Your Application

Here are a few useful commands to manage your running application. Run these from inside your project directory (`/root/bas-ai` or similar).

*   **To view the application logs in real-time:**
    ```bash
    docker-compose logs -f
    ```
    This is useful for debugging or seeing what the application is doing. Press `Ctrl+C` to stop viewing the logs.

*   **To stop the application:**
    ```bash
    docker-compose down
    ```
    This will gracefully stop and remove the running containers. Your downloaded AI model will be preserved.

*   **To restart the application:**
    Simply run the start command again.
    ```bash
    docker-compose up --build -d
    ```
