import json
import logging
from typing import Any
from typing import Dict
from typing import Iterable
from polygenic.lib.model.seqql import PolygenicRiskScoreResult
from polygenic.lib.data_access.dto import ModelDescriptionInfo

logger = logging.getLogger('description_language.' + __name__)


# def create_res_representation_for_models(results: Dict[str, PolygenicRiskScoreResult],
#                                          descriptions: Dict[str, Iterable[Dict[str, Any]]],
#                                          populations: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
#     ret = {}
#     for k, v in results.items():
#         ret[k] = create_res_representation_for_model(v, descriptions[k], populations[k])
#     return ret


def create_res_representation_for_model(result: PolygenicRiskScoreResult, model_description_info: ModelDescriptionInfo,
                                        population: str) -> Dict[str, Any]:
    ordered_dict_representation = result._asdict()
    ordered_dict_representation['trait_was_prepared_for_population'] = population
    descriptions = {}
    for f_path in model_description_info.desc_paths:
        with open(f_path) as f:
            descriptions[f_path] = json.load(f)
    if model_description_info.plot_data_path:
        with open(model_description_info.plot_data_path) as f:
            ordered_dict_representation['plot_data'] = json.load(f)
    else:
        ordered_dict_representation['plot_data'] = None
    ordered_dict_representation['descriptions'] = {k:get_proper_values_depending_on_category_name(v, result.category) for k, v in descriptions.items()}
    return dict(ordered_dict_representation)


def get_proper_values_depending_on_category_name(description:Dict[str, Any], category:str) -> Dict[str, Any]:
    out = {}
    for k, v in description.items():
        if k.endswith('_choice'):
            out[k] = v[category]
        else:
            out[k] = v
    return out
