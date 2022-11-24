import json
from django.core.management.base import BaseCommand, CommandError
import numpy as np

from symbols_analyzer.models import CellImage

class Command(BaseCommand):
    def handle(self, *args, **options):
        row_data  = CellImage.objects.all().exclude(symbol='')
        row_data = row_data .values_list('image_array', 'symbol')
        images = []
        targets = []
        for tpl in row_data:
            array = json.loads(tpl[0])
            array = np.array(array)
            array = abs(array - 1)
            images.append(array)

            if tpl[1] == 'n':
                target = 6
            else:
                target = float(tpl[1])
            targets.append(target)
        
        images = np.array(images)
        targets = np.array(targets)

        np.save('../../data/images', images, allow_pickle=True)
        np.save('../../data/targets', targets, allow_pickle=True)