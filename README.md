# 🌥️ Cloud Algorithm Simulator - Frontend

**Cloud Algorithm Simulator** is a web-based application developed using **Flask**, designed to **simulate and analyze various cloud scheduling algorithms** utilizing **CloudSim**. The application follows a **microservices architecture**, where the **frontend (Flask-based UI)** interacts with **backend microservices (Spring Boot)** for executing scheduling algorithms.

## 📚 Table of Contents
1. [Features](#features)  
2. [Tech Stack](#tech-stack)  
3. [Project Structure](#project-structure)  
4. [Supported Algorithms](#supported-cloud-scheduling-algorithms)
5. [Microservices Architecture](#microservices-architecture)  
6. [Installation & Setup](#installation--setup)  
7. [Authors](#authors)  
8. [License](#license)  

---

## Features

- **Microservices-Based Cloud Algorithm Simulation** – The frontend (Flask) interacts with backend microservices (Spring Boot) for cloud scheduling.  
- **Real-Time Execution & Results** – Immediate feedback on scheduling performance.  
- **CloudSim Integration** – Utilizes CloudSim for simulating cloud workloads.  
- **Scalability & Performance** – Hosted on **AWS EC2**, with **Dockerized microservices** for efficient deployment.  
- **CI/CD Pipeline** – Automated deployment using **Jenkins Master-Slave Architecture**.  
- **Containerization** – Uses **Docker** for consistent deployment across environments.  

---

## Tech Stack

- **Frontend:** Python (Flask), HTML, CSS, JavaScript  
- **Backend:** Spring Boot (Microservices)  
- **Cloud Simulation:** CloudSim  
- **Deployment:** AWS EC2  
- **Containerization:** Docker  
- **CI/CD:** Jenkins  
- **Version Control:** Git & GitHub  

---

## Project Structure

```plaintext
Cloud_Algorithm_Simulator_Frontend/
├── static/                 # Static assets (CSS)
│   ├── styles.css            
├── templates/              # HTML templates with integrated JavaScript 
│   ├── index.html  
│   ├── result.html           
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration
├── Jenkinsfile             # Jenkins pipeline configuration
├── README.md               # Project documentation
├── app.py                  # Main Flask application (Frontend)
└── requirements.txt        # Python dependencies
```

---

## Supported Cloud Scheduling Algorithms

This simulator supports the following **cloud scheduling and resource allocation algorithms**, processed via backend microservices:

1. **Round Robin (RR):** Distributes tasks evenly across virtual machines in a cyclic order.  
2. **First Come First Serve (FCFS):** Assigns tasks in the order of arrival.  
3. **Ant Colony Optimization (ACO):** Uses swarm intelligence for task scheduling.  
4. **Genetic Algorithm (GA):** Applies evolutionary techniques for optimization.  
5. **Shortest Job First (SJF):** Prioritizes shorter tasks for execution.  

---

## Microservices Architecture

The **Cloud Algorithm Simulator** follows a **microservices-based design**, ensuring modularity and scalability:

- **Frontend:**  
  - Developed in **Flask** for UI rendering and user interactions.  
  - Sends API requests to backend microservices for execution.  

- **Backend (Microservices):**  
  - **Spring Boot** services handle cloud scheduling logic.  
  - Each scheduling algorithm runs in an isolated microservice.  
  - **RESTful APIs** allow communication between frontend and backend.  

- **CloudSim Integration:**  
  - Backend microservices process tasks using CloudSim.  
  - Results are returned to Flask for visualization.  

This architecture enhances **scalability, fault tolerance, and maintainability**.  

---

## Installation & Setup

You can run the application **manually** or using **Docker**.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Abhishek-2502/Cloud_Algorithm_Simulator_Frontend.git
cd Cloud_Algorithm_Simulator_Frontend
```

### 2️⃣ Run Manually

#### (A) Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### (B) Install Dependencies

```bash
pip install -r requirements.txt
```

#### (C) Start the Flask Application

```bash
python app.py
```

The frontend will be running at **`http://localhost:5000`**.

---

### 3️⃣ Run with Docker

#### (A) Build the Docker Image

```bash
docker build -t cloudsim-frontend .
```

#### (B) Run the Docker Container

```bash
docker run -d -p 5000:5000 cloudsim-frontend
```

Access the frontend at **`http://localhost:5000`**.

---

## Authors

- **Abhishek Rajput** - [GitHub](https://github.com/Abhishek-2502)  

---

## License

This project is licensed under the **MIT License**.  
