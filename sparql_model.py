import pysparql_anything as sa
import logging


logger = logging.getLogger(__name__)

def run_sparql_query(classification_references):
    # Add "KG" prefix to each classification reference
    prefixed_classification_references = [f"KG{classification_reference}" for classification_reference in classification_references]
    logger.info(f"Classification references being used for SPARQL query: {prefixed_classification_references}")
    
    # Create the VALUES clause with the prefixed classification references
    values_clause = "VALUES ?classification_reference { " + " ".join([f'"{classification_reference}"' for classification_reference in prefixed_classification_references]) + " }"
    print(values_clause)
    q = f"""
    PREFIX xyz:  <http://sparql.xyz/facade-x/data/>
    PREFIX fx:   <http://sparql.xyz/facade-x/ns/>

    SELECT ?classification_reference ?s1 ?unit_price ?file1
    WHERE
      {{ {values_clause}
         SERVICE <x-sparql-anything:location=uploads>
          {{ fx:properties
                      fx:archive.matches  ".*txt|.*xlsx" .
            ?s        fx:anySlot          ?file1
            SERVICE <x-sparql-anything:blank-nodes=false>
              {{ fx:properties
                          fx:location      ?file1 ;
                          fx:from-archive  "uploads" .
                 fx:properties fx:spreadsheet.headers true .
                 fx:properties fx:spreadsheet.evaluate-formulas true .
                ?s1 xyz:CostCode ?classification_reference .
                ?s1 xyz:Price ?unit_price .
              }}
          }}
      }}
    """
    logger.info(f"Running SPARQL query: {q}")
    engine = sa.SparqlAnything()
    try:
        results = engine.select(q=q)
        if results and 'results' in results and 'bindings' in results['results']:
            logger.info(f"SPARQL query returned results: {results['results']['bindings']}")
            for binding in results['results']['bindings']:
                logger.info(f"Binding: {binding}")
                if 'classification_reference' in binding and 'unit_price' in binding and 'file1' in binding:
                    logger.info(f"Complete binding: {binding}")
                else:
                    logger.warning(f"Incomplete data in binding: {binding}")
            return results
        else:
            logger.warning("No results or incomplete results returned from SPARQL query.")
            return None
    except Exception as exc:
        logger.error(f"An error occurred while executing SPARQL query: {exc}")
        return None

def aggregate_costs(results):
    costs_by_classification_reference = {}
    if results and 'results' in results and 'bindings' in results['results']:
        for binding in results['results']['bindings']:
            if 'classification_reference' in binding and 'unit_price' in binding and 'file1' in binding:
                classification_reference = binding['classification_reference']['value']
                unit_price = float(binding['unit_price']['value'])
                file_location = binding['file1']['value']
                if classification_reference in costs_by_classification_reference:
                    costs_by_classification_reference[classification_reference]['total_cost'] += unit_price
                else:
                    costs_by_classification_reference[classification_reference] = {'total_cost': unit_price, 'file_location': file_location}
            else:
                logger.warning(f"Incomplete data in binding: {binding}")
    else:
        logger.warning("No results or incomplete results returned from aggregation.")
    return costs_by_classification_reference
