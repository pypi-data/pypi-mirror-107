import json
from halohalo.experimentation import cohort

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

# class cohort:
#     def __init__(self, variant_dict):
#         self.name = variant_dict['cohort_name']
#         self.model_id = variant_dict['model_id']
#         self.endpoint_name = variant_dict['endpoint_name']
#         self.weight = variant_dict['weight']
    
#     def show(self):
#         print(vars(self))
#         return vars(self)

class waiter:
    def __init__(self, experiments_dict):
        self.experiments = experiments_dict

    def order_model(self, target_use_case, target_experiment, target_cohort = 'control'):

        exp_config = self.experiments

        forced_use_case = _extract_json(exp_config['use_cases'], 'use_case_name', target_use_case)
        forced_experiment = _extract_json(forced_use_case['experiments'], 'experiment_name', target_experiment)
        forced_cohort = _extract_json(forced_experiment['cohorts'], 'model_id', target_cohort)

        return cohort(forced_cohort)