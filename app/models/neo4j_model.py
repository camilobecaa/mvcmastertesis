from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

def connect_graph_db(uri, user, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("Connected to Neo4j database successfully.")
        return driver
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j database: {e}")
        raise

def create_or_update_node(driver, guid, area, total_cost, timestamp, file_location, ifc_type, classification_reference):
    with driver.session() as session:
        try:
            session.run('''
                MERGE (e:Element {guid: $guid})
                SET e.area = $area, e.total_cost = $total_cost, e.timestamp = $timestamp, e.file_location = $file_location
            ''', guid=guid, area=area, total_cost=total_cost, timestamp=timestamp, file_location=file_location)
            logger.info(f"Element node created/updated for GUID {guid}.")
            
            session.run('''
                MERGE (t:IFCType {name: $ifc_type})
            ''', ifc_type=ifc_type)
            logger.info(f"IFCType node created/updated for type {ifc_type}.")
            
            session.run('''
                MATCH (t:IFCType {name: $ifc_type}), (e:Element {guid: $guid})
                MERGE (t)-[:HAS_ELEMENT]->(e)
            ''', ifc_type=ifc_type, guid=guid)
            logger.info(f"Relationship created between IFCType and Element for GUID {guid}.")
            
            session.run('''
                MERGE (c:ClassificationReference {name: $classification_reference})
            ''', classification_reference=classification_reference)
            logger.info(f"ClassificationReference node created/updated for {classification_reference}.")
            
            session.run('''
                MATCH (c:ClassificationReference {name: $classification_reference}), (e:Element {guid: $guid})
                MERGE (c)-[:CLASSIFIES]->(e)
            ''', classification_reference=classification_reference, guid=guid)
            logger.info(f"Relationship created between ClassificationReference and Element for GUID {guid}.")
        except Exception as e:
            logger.error(f"An error occurred while creating/updating nodes in Neo4j: {e}")
