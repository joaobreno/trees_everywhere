from dal import autocomplete
from home.models import *

class TreesAutocomplete(autocomplete.Select2QuerySetView): 

    def get_queryset(self):
        trees = Tree.objects.all()

        if self.q:
            trees = trees.filter(name__icontains=self.q)

        return trees
    
    def get_result_label(self, item):
        return item.templ_autocomplete()

