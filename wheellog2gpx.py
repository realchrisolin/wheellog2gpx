import argparse
import csv
import os.path
import gpxpy
from datetime import datetime
import time


def csv2gpx(file, verbose=False, debug=False):
    # This function is essentially a wrapper for gpxpy, which is really
    # creating the GPX file under the hood.
    csv_data = open(file, 'r')
    csv_reader = csv.reader(csv_data)
    gpx_data = gpxpy.gpx.GPX()
    gpx_file = file[:-3] + 'gpx' # export to the same directory/filename as .csv but with .gpx extension
    reader_index = 0
    wrapper = {}
    headers = next(csv_reader, None)
    print(headers)

    # idiot proofing
    if 'date' and 'time' and 'latitude' and 'longitude' and 'gps_speed' and 'gps_alt' and 'gps_heading' and 'gps_distance' and 'speed' and 'voltage' and 'phase_current' and 'current' and 'power' and 'torque' and 'pwm' and 'battery_level' and 'distance' and 'totaldistance' and 'system_temp' and 'temp2' and 'tilt' and 'roll' and 'mode' and 'alert' not in headers:

        print('required header columns missing, check input CSV file (was it generated by WheelLog?)')
        return RuntimeError
    else:
        for h in headers:
            wrapper[h] = None
        print("CSV file: valid")
        print("starting conversion")

    # instantiate gpx object
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_data.tracks.append(gpx_track)
    gpx_track.segments.append(gpx_segment)

    for row in csv_reader:
        reader_index += 1
        if verbose is True:
            print(f'Processing line {reader_index}')
        for id, data in zip(headers, row):
            wrapper[id] = data
        # TODO: finish sanitizing date/time and pass it to gpxpy
        sanitized_time = datetime.strptime(f"{wrapper['date']} {wrapper['time']}", '%Y-%m-%d %H:%M:%S.%f')
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=wrapper['latitude'], longitude=wrapper['longitude'],
                                                          elevation=wrapper['gps_alt'], time=sanitized_time,
                                                          speed=wrapper['speed']))
        if debug is True:
            print(f'{wrapper}')
            print('-'*10)
    try:
        gpx_writer = open(gpx_file, 'x')
    except FileExistsError:
        gpx_writer = open(gpx_file, 'w')
    gpx_writer.write(gpx_data.to_xml(version='1.1'))


def parse_args():
    parser = argparse.ArgumentParser(description="WheelLog2GPX")
    parser.add_argument("csv_file")
    parser.add_argument('-v', '--verbose', help="additional console logging", action="store_true")
    parser.add_argument('-d', '--debug', help="print each line from input CSV", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    csv2gpx(args.csv_file, verbose=args.verbose, debug=args.debug)

if __name__ == '__main__':
    main()
