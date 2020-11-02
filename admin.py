from helpcentre.models import Query, Faq
from omniport.admin.site import omnipotence

omnipotence.register(Query)
omnipotence.register(Faq)
