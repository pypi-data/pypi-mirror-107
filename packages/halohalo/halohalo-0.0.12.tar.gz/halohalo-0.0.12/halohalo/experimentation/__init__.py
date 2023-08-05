import json
import random

'''
Sample experiments.json configuration file
{
    "use_cases": [
        {
            "use_case_name": "Use Case A",
            "experiments": [
                {
                    "experiment_name": "Experiment A",
                    "cohorts": [
                        {
                            "cohort_name": "control",
                            "model_id": "control",
                            "endpoint_name": "NULL",
                            "weight": 1
                        },
                        {
                            "cohort_name": "treatment",
                            "model_id": "treatment",
                            "endpoint_name": "NULL",
                            "weight": 1
                        }
                    ]
                }
            ]
        }
    ]
}
'''

def _extract_json(list_obj, key_name, key_value):
    val = next((item for item in list_obj
        if item[key_name] == key_value), None)
    return val

class cohort:
    def __init__(self, variant_dict):
        self.name = variant_dict['cohort_name']
        self.model_id = variant_dict['model_id']
        self.endpoint_name = variant_dict['endpoint_name']
        self.weight = variant_dict['weight']
    
    def show(self):
        print(vars(self))
        return vars(self)

class abController:
    def __init__(self, experiments_dict):
        self.experiments = experiments_dict

    def get_cohort(self, target_use_case, target_experiment, is_test = True):

        exp_config = self.experiments

        for use_case in exp_config['use_cases']:
            if use_case['use_case_name'] == target_use_case:

                for experiment in use_case['experiments']:
                    if experiment['experiment_name'] == target_experiment:
                        
                        weighted_randomizer = list()

                        # Get total weights
                        for variant in experiment['cohorts']:
                            for x in range(0, int(variant['weight'])):
                                weighted_randomizer.append(variant)
                        
                        break
                break

        # print(weighted_randomizer)
        res = random.choice(weighted_randomizer)

        return cohort(res)