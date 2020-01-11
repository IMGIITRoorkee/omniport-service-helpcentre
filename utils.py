from django.conf import settings

from categories.models.category import Category


def get_base_category():
    """
    This function returns the category node corresponding to this service
    :return: the Category object with slug field equal to service name
    """

    service_nomenclature = settings.DISCOVERY.get_app_configuration(
        'helpcentre'
    ).nomenclature
    cat_obj, created = Category.objects.get_or_create(
        slug=service_nomenclature.name,
        name=service_nomenclature.verboseName
    )
    return cat_obj
