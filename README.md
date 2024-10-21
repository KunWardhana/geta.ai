# Running Andrea.ai

This guide will walk you through running the Andrea.ai application using Docker. Follow the steps below to set up and run the application.

## Instructions

1. **Make sure you have Docker installed**
   - Verify Docker installation by running the following command in your terminal or command prompt:
     ```bash
     docker --version
     ```

2. **Run Docker**
   - Start Docker on your system. This might vary depending on your operating system:
     - **Windows**: Start Docker Desktop.
     - **macOS**: Open Docker Desktop from the Applications folder.
     - **Linux**: Use the command below if Docker isn’t running as a service:
       ```bash
       sudo systemctl start docker
       ```

3. **Go to Command Prompt/Terminal**
   - Open your terminal (Linux/macOS) or command prompt (Windows).

4. **Go to the project's directory**
   - Navigate to the directory where the project is located. Use the `cd` command as shown below:
     ```bash
     cd /path/to/your/project
     ```

5. **Run the application**
   - Once in the project directory, execute the following command to build and run the application:
     ```bash
     docker-compose up --build
     ```

6. **Access the Application**
   - After the containers are up and running, access the application through your browser at `http://localhost:3000` for the Frontend

## Additional Notes
- If you encounter any issues, ensure Docker is running properly and that your system meets the requirements for Docker and Docker Compose.
- To stop the application, press `Ctrl + C` in the terminal or run:
  ```bash
  docker-compose down