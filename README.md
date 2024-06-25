# 📄✏ Wafer Fault Detection Project

**Brief:** In electronics, a **wafer** (also called a slice or substrate) is a thin slice of semiconductor, such as a crystalline silicon (c-Si), used for the fabrication of integrated circuits and, in photovoltaics, to manufacture solar cells. The wafer serves as the substrate(serves as foundation for contruction of other components) for microelectronic devices built in and upon the wafer.

It undergoes many microfabrication processes, such as doping, ion implantation, etching, thin-film deposition of various materials, and photolithographic patterning. Finally, the individual microcircuits are separated by wafer dicing and packaged as an integrated circuit.

## Overview

This project aims to detect faults in wafers using a Random Forest classification machine learning model. It features a comprehensive data ingestion, transformation, and training pipeline, along with a prediction pipeline. The entire process is designed to be highly automated, scalable, and user-friendly.

## Features

- **Data Ingestion**: Fully functional pipeline for ingesting data.
- **Data Transformation**: Automated transformation of ingested data.
- **Model Training**: Training pipeline that builds and stores the model.
- **Prediction Pipeline**: Upload an Excel file, and the system predicts faults for all inputs.
- **AWS Integration**:
  - All training data and models are stored in AWS S3.
  - Docker container creation and deployment using GitHub Actions.
  - Containers are pushed to AWS Elastic Container Registry (ECR).
  - AWS App Runner scales and runs the container.
- **API**:
  - One-click training initiation through API.
  - Handles all heavy computational loads.
- **Web Serving**: Utilizes Flask for serving the web application.
- **CI/CD**: Continuous integration and deployment with GitHub Actions for automatic updates.

## Getting Started

### Prerequisites

- **AWS Account**: For S3, ECR, and App Runner.
- **GitHub Account**: For code repository and actions.
- **Docker**: For containerization.

### Running Locally

1. **Clone the Repository**:

   ```bash
    git clone https://github.com/Code8Soumya/Wafer-Fault-Detection-Project.git
    cd wafer-fault-detection

   ```

2. **In Terminal Run**
   ```bash
    conda create -p venv python==3.12
    pip install -r requirements.txt  
    python app.py
   ```
