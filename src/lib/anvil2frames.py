from bs4 import BeautifulSoup

TRACK_NAME = 'scene breaks'
def get_breaks_with_time_from_anvil_file_path(anvil_xml_file_path):
    xml_file = open(anvil_xml_file_path, encoding='utf-16')
    xml_contents = xml_file.read()
    soup = BeautifulSoup(xml_contents, 'lxml')

    annotation_elements = soup.find('track', {'name': TRACK_NAME}).find_all('el')
    annotation_times = list(map(lambda a: a['time'], annotation_elements))
    break_types = list(map(lambda a: a.attribute.getText(), annotation_elements))
    breaks_with_time = zip(break_types, annotation_times)

    return list(breaks_with_time)

def get_annotation_frames(anvil_xml_file_path, frameRate):
    get_annotation_times_from_anvil_file_path(anvil_xml_file_path)
    #map for each element of each array of the dict the conversion from times to frames

get_breaks_with_time_from_anvil_file_path('misc/AT-full-episode-annotations.anvil')
