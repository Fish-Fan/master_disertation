from app import history_pattern_location
import os
import json

HISTORY_PATTERN_LOCATION = DATASET_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), history_pattern_location)
class RecipeGenerator:
    def __init__(self, domain_knowledge):
        self.domain_knowledge = domain_knowledge
        with open(HISTORY_PATTERN_LOCATION, 'r') as f:
            self.history_pattern = json.load(f)


    def generate(self):
        result = []
        if self.domain_knowledge['needClean'] == "Yes":
            result.append({
                "type": "clean",
                "description": "Remove target columns from this dataset or fill missing value in target columns",
                "steps": [
                ]
            })
        if self.domain_knowledge['needSplit'] == "Yes":
            result.append( {
                "type": "enrich",
                "description": "Choose a delimiter to split target columns or change column format, make it more semantic.",
                "steps": []
              })
        if self.domain_knowledge['singleOrMultiple'] == "Multiple":
            result.append({
                "type": "integration",
                "description": "Integrate another file into this dataset.",
                "steps": [
                  ]
              })
        result.append({
            "type": "filter",
            "description": "Filter datasets in given conditions.",
            "steps": []
        })
        if self.domain_knowledge['needAggregation'] == "Yes":
            result.append({
                "type": "aggregation",
                "description": "Choose your groupby column then apply aggregate functions.",
                "steps": []
              })

        return result


