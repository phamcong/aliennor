from ecocases.models import *
import json

ecocases = Ecocase.objects.all()
print(len(ecocases))

