from collections import defaultdict


class PrincetonBuildingLatLng(object):
    LOCATION_DESIGNATOR_WORDS = ['in', 'at', 'near', 'behind', 'outside']

    def __init__(self,
                 look_ahead=5,
                 reference_file_name='princeton_building_locations.txt'):
        self.look_ahead = look_ahead
        f = open(reference_file_name)

        self.name_to_latlng = {}
        for line in f:
            name, lat, lng = line.replace('\n', '').split(',')
            self.name_to_latlng[name.lower()] = (float(lat), float(lng))

    def __standardize_text(self, text):
        exclude = set('!"#$%()*+,-./;&:<=>?@[]^_`{|}~')
        text = ''.join(ch for ch in text if ch not in exclude)
        return text.lower()

    def parse_building_name(self, text):
        std_text = self.__standardize_text(text)

        targets = [' %s ' % x for x in self.LOCATION_DESIGNATOR_WORDS]
        candidates = defaultdict(int)
        for target in targets:
            spot = std_text.find(target)
            while spot > -1:
                # find the self.look_ahead # of words after spot, and check if
                # any are a part of a building location
                lookahead_words = std_text[spot + len(target) - 1:].split(
                )[:self.look_ahead]
                for word in lookahead_words:
                    for building_name in self.name_to_latlng.keys():
                        if word in building_name.split():
                            candidates[building_name] += 1
                spot = std_text.find(target, spot + 1)

        # return the building with the most word matches
        if candidates:
            best_name, best_score = max(candidates.items(), key=lambda x: x[1])
            return best_name

        # if no candidates, check if the capitalized version of the full
        # building name is mentioned anywhere as a backup (for cases with punct.)
        for building_name in self.name_to_latlng.keys():
            if building_name.capitalize() in text:
                return building_name
        return None

    def get_lat_lng(self, building_name):
        if building_name is None:
            return None, None
        return self.name_to_latlng[building_name.lower()]
