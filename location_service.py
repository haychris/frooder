from collections import defaultdict

class PrincetonBuildingLatLng(object):
    def __init__(self, reference_file_name='princeton_building_locations.txt'):
        f = open(reference_file_name)

        self.name_to_latlng = {}
        for line in f:
            name, lat, lng = line.replace('\n', '').split(',')
            self.name_to_latlng[name.lower()] = (float(lat), float(lng))

    def parse_location(self, text):
        original_text = text
        exclude = set('!"#$%()*+,-./;&:<=>?@[]^_`{|}~')
        text = ''.join(ch for ch in text if ch not in exclude)
        text = text.lower()
        targets = ['in', 'at', 'near', 'behind', 'outside']
        targets = [' %s ' % x for x in targets]
        candidates = defaultdict(int)
        for target in targets:
            spot = text.find(target)
            while spot > -1:
                split_text = text[spot+len(target)-1:].split()
                for word in split_text[:5]:
                    for building_name in self.name_to_latlng.keys():
                        if word in building_name.split():
                            candidates[building_name] += 1
                spot = text.find(target, spot+1)
        if candidates:
            best_name, best_score = max(candidates.items(), key=lambda x: x[1])
            return best_name
        for building_name in self.name_to_latlng.keys():
            if building_name.capitalize() in original_text:
                return building_name
        return None
        # print 'No match found:', text

    def get_lat_lng(self, building_name):
        if building_name is None:
            return None, None
        return self.name_to_latlng[building_name.lower()]
