import os
import yaml

from categories.models.category import Category


def get_base_category():
    """
    :return: the Category object with slug field equal to service name
    """

    config_path = os.path.join('services', 'helpcentre', 'config.yml')
    with open(config_path, 'r') as file_object:
        app_configuration = yaml.safe_load(file_object)
    nomenclature = app_configuration['nomenclature']
    service_name = nomenclature['name']
    service_verbose = nomenclature['verboseName']
    cat_obj, created = Category.objects.get_or_create(
        slug=service_name,
        name=service_verbose
    )
    return cat_obj
