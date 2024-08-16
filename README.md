# Automated Construction Invoicing Application

## Overview

This application is designed to improve data interoperability within the Architecture, Engineering, and Construction (AEC) industry by integrating heterogeneous data sources. By leveraging Linked Data principles, the application automates the generation of construction invoices by combining data from Industry Foundation Class (IFC) models and CSV files. The prototype uses a Model-View-Controller (MVC) design pattern to ensure scalability, maintainability, and ease of testing.

## Features

- **Data Integration**: Extracts and integrates data from IFC files and CSV spreadsheets.
- **SPARQL Querying**: Utilizes SPARQL Anything to transform non-RDF data into RDF triples for querying.
- **Graph Database Storage**: Stores integrated data in a Neo4j graph database for efficient querying and analysis.
- **Automated Invoicing**: Generates accurate and timely invoices based on the integrated data.

## System Requirements

- **Python 3.7+**
- **Flask**: For web development and routing.
- **IfcOpenShell**: For extracting and processing IFC files.
- **SPARQL Anything**: For querying non-RDF data as RDF.
- **Neo4j**: For storing and managing graph-based data.
- **Other Python Libraries**: `Werkzeug`, `os`, `logging`, `csv`, `json`, etc.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository-name.git
    cd your-repository-name
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Neo4j**:
    - Install and configure Neo4j on your local machine or server.
    - Ensure that Neo4j is running and accessible from the application.

## Configuration

1. **Environment Variables**:
    - Set the necessary environment variables for Flask and Neo4j in a `.env` file.
    ```plaintext
    FLASK_APP=app.py
    FLASK_ENV=development
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=password
    UPLOAD_FOLDER=uploads
    ```

2. **File Storage**:
    - Ensure that the `uploads` folder exists in the root directory for storing uploaded files.

## Usage

1. **Run the Application**:
    ```bash
    flask run
    ```

2. **Access the Application**:
    - Open your web browser and navigate to `http://localhost:5000`.
    - Upload the CSV and IFC files through the provided interface.
    - Enter your Neo4j credentials to connect to the database.

3. **Process Data**:
    - The application will extract GUIDs and relevant properties from the IFC files, query the CSV data using SPARQL, and store the results in the Neo4j database.

4. **View Results**:
    - The results will be displayed on the web interface, showing the calculated costs and other relevant information.

## UML Diagrams

- **Structural Diagram**: Provides an overview of the application's architecture.
- **Behavioral Diagram**: Illustrates the flow of data and user interactions.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [Your Name](mailto:your.email@example.com).
