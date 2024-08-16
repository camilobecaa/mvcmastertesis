

# Now you can import sparql_model
from sparql_model import run_sparql_query, aggregate_costs
def test_sparql():
    # Sample classification references to test the query
    classification_references = [
        "331","331","361"
    ]

    # Run the SPARQL query
    try:
        results = run_sparql_query(classification_references)
        if results:
            print("SPARQL Query Results:")
            for result in results['results']['bindings']:
                print(result)
            
            # Aggregate the costs by classification reference (GUID)
            aggregated_costs = aggregate_costs(results)
            
            # Print the aggregated costs
            print("\nAggregated Costs:")
            for guid, cost_info in aggregated_costs.items():
                print(f"GUID: {guid}, Total Cost: {cost_info['total_cost']}, File Location: {cost_info['file_location']}")
        else:
            print("No results returned from SPARQL query.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_sparql()
