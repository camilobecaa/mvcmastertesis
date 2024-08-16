import csv
import ifcopenshell
import logging

logger = logging.getLogger(__name__)

def extract_guids_from_csv(csv_file_path, guid_col_name):
    guids = []
    timestamps = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            guid = row.get(guid_col_name, "").strip()
            timestamp = row.get("Updated At", "").strip()
            if guid and timestamp:
                guids.append(guid)
                timestamps.append(timestamp)
    return guids, timestamps

def get_area_type_classification(ifc_file, guid):
    def get_all_properties(element):
        properties_dict = {}
        properties_dict['GlobalId'] = element.GlobalId
        properties_dict['Name'] = element.Name
        properties_dict['Description'] = element.Description

        if hasattr(element, 'IsDefinedBy'):
            for definition in element.IsDefinedBy:
                if hasattr(definition, 'RelatingPropertyDefinition'):
                    property_set = definition.RelatingPropertyDefinition
                    if hasattr(property_set, 'HasProperties'):
                        for prop in property_set.HasProperties:
                            prop_name = prop.Name
                            prop_value = prop.NominalValue.wrappedValue if hasattr(prop.NominalValue, 'wrappedValue') else prop.NominalValue
                            properties_dict[prop_name] = prop_value
        
        if hasattr(element, 'IsTypedBy'):
            for type_relation in element.IsTypedBy:
                type_obj = type_relation.RelatingType
                properties_dict['IfcType'] = type_obj.is_a()
                if hasattr(type_obj, 'HasPropertySets'):
                    for property_set in type_obj.HasPropertySets:
                        if hasattr(property_set, 'HasProperties'):
                            for prop in property_set.HasProperties:
                                prop_name = prop.Name
                                prop_value = prop.NominalValue.wrappedValue if hasattr(prop.NominalValue, 'wrappedValue') else prop.NominalValue
                                properties_dict[prop_name] = prop_value
        
        if hasattr(element, 'HasAssociations'):
            for association in element.HasAssociations:
                if hasattr(association, 'RelatingClassification'):
                    classification = association.RelatingClassification
                    if classification.is_a("IfcClassificationReference"):
                        properties_dict['IFCCLASSIFICATIONREFERENCE'] = classification.Identification
        
        return properties_dict

    def get_quantity_area(element):
        if hasattr(element, 'IsDefinedBy'):
            for relDefines in element.IsDefinedBy:
                if relDefines.is_a("IfcRelDefinesByProperties"):
                    property_set = relDefines.RelatingPropertyDefinition
                    if property_set.is_a("IfcElementQuantity"):
                        for quantity in property_set.Quantities:
                            if quantity.is_a("IfcQuantityArea"):
                                return quantity.AreaValue

    element = ifc_file.by_guid(guid)
    if not element:
        return None, None, None
    
    properties = get_all_properties(element)
    area = get_quantity_area(element)
    
    ifc_type = properties.get('IfcType', 'Unknown')
    classification_reference = properties.get('IFCCLASSIFICATIONREFERENCE', 'None')

    logger.info(f"Extracted properties for GUID {guid} - Area: {area}, IFC Type: {ifc_type}, Classification Reference: {classification_reference}")
    return area, ifc_type, classification_reference
