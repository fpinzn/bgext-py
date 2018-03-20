from bs4 import BeautifulSoup
import util
import os

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

def convert_time_to_frame (time, frame_rate):
    return int(float(frame_rate) * float(time))

def convert_breaks_with_time_dict_to_frame_csv_text (break_list, frame_rate):
    csv_text = 'frame,break-type\n'
    for e in break_list:
        csv_text += str(convert_time_to_frame(e[1], frame_rate)) + ',' + e[0] + '\n'
    return csv_text

def get_annotation_frames(anvil_xml_file_path, frame_rate):
    breaks_with_time = get_breaks_with_time_from_anvil_file_path(anvil_xml_file_path)
    return convert_breaks_with_time_dict_to_frame_csv_text(breaks_with_time, frame_rate)

def convert_anvil_file_to_annotation_csv_frames_given_frame_rate_and_save_to_file(anvil_xml_file_path, frame_rate, file_path):
    ## input validation
    if not (os.path.exists(anvil_xml_file_path)):
        print('anvil xml file', anvil_xml_file_path, 'does not exist')
        sys.exit()

    if (os.access(file_path, os.W_OK)):
        print('cannot write to', file_path)
        sys.exit()

    csv_text = get_annotation_frames(anvil_xml_file_path, frame_rate)
    util.write_to_file(csv_text, file_path)
