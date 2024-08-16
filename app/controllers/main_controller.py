from flask import Blueprint, request, render_template, jsonify, current_app
import ifcopenshell
from werkzeug.utils import secure_filename
import logging
import os
import sys

from ..models.ifc_model import extract_guids_from_csv, get_area_type_classification
from ..models.neo4j_model import connect_graph_db, create_or_update_node

# Add the root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import sparql_model using absolute import
from sparql_model import run_sparql_query, aggregate_costs

# The rest of your code remains unchanged


main = Blueprint('main', __name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/')
def upload_form():
    return render_template('upload.html')

@main.route('/process', methods=['POST'])
def process():
    if 'csv_file' not in request.files or 'ifc_file' not in request.files:
        return 'No file part', 400

    csv_file = request.files['csv_file']
    ifc_file = request.files['ifc_file']

    if csv_file.filename == '' or ifc_file.filename == '':
        return 'No selected file', 400

    if csv_file and allowed_file(csv_file.filename):
        csv_filename = secure_filename(csv_file.filename)
        csv_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], csv_filename)
        csv_file.save(csv_file_path)
    else:
        return 'Invalid CSV file type', 400

    if ifc_file and allowed_file(ifc_file.filename):
        ifc_filename = secure_filename(ifc_file.filename)
        ifc_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], ifc_filename)
        ifc_file.save(ifc_file_path)
    else:
        return 'Invalid IFC file type', 400

    uri = request.form['uri']
    user = request.form['user']
    password = request.form['password']

    try:
        results = main_logic(csv_file_path, ifc_file_path, uri, user, password)
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")
        return str(e), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def main_logic(csv_file_path, ifc_file_path, uri, user, password):
    driver = connect_graph_db(uri, user, password)
    guids, timestamps = extract_guids_from_csv(csv_file_path, "IFC/GAMMA Object ID")

    try:
        ifc_file = ifcopenshell.open(ifc_file_path)
        logger.info("IFC file opened successfully.")
    except Exception as e:
        logger.error(f"An error occurred while opening the IFC file: {e}")
        return {"error": f"Unable to open IFC file: {str(e)}"}

    final_results = {}
    classification_references = []
    guid_to_classification = {}

    for guid, timestamp in zip(guids, timestamps):
        area, ifc_type, classification_reference = get_area_type_classification(ifc_file, guid)
        if area is not None and ifc_type is not None:
            classification_references.append(classification_reference)
            guid_to_classification[guid] = {
                "Area": area, 
                "Timestamp": timestamp, 
                "IFC Type": ifc_type, 
                "Classification Reference": classification_reference
            }

    results = run_sparql_query(classification_references)
    costs_by_classification_reference = aggregate_costs(results)

    for guid, info in guid_to_classification.items():
        classification_reference = info["Classification Reference"]
        area = info["Area"]
        timestamp = info["Timestamp"]
        ifc_type = info["IFC Type"]
        cost_info = costs_by_classification_reference.get(classification_reference, {})
        total_cost = cost_info.get('total_cost', 0) * area
        file_location = cost_info.get('file_location', ifc_file_path)

        final_results[guid] = {
            "Area": area, 
            "Total Cost": total_cost, 
            "Timestamp": timestamp, 
            "File Location": file_location, 
            "IFC Type": ifc_type, 
            "Classification Reference": classification_reference
        }
        logger.info(f"Processed GUID {guid}: Area={area}, Total Cost={total_cost}, IFC Type={ifc_type}, Classification Reference={classification_reference}")
        create_or_update_node(driver, guid, area, total_cost, timestamp, file_location, ifc_type, classification_reference)

    driver.close()
    return final_results
