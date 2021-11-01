"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            if result.neo.name is None:
                result.neo.name = ''
            if result.neo.diameter is float('nan'):
                result.neo.diameter = ''
            if result.neo.hazardous is True:
                result.neo.hazardous = 'True'
            if result.neo.hazardous is False:
                result.neo.hazardous = 'False'
            row = [{'datetime_utc': result.time.date(),
                    'distance_au': result.distance,
                    'velocity_km_s': result.velocity,
                    'designation': result.designation,
                    'name': result.neo.name,
                    'diameter_km': result.neo.diameter,
                    'potentially_hazardous': result.neo.hazardous}]
            writer.writerows(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as outfile:
        writable_results = []
        for result in results:
            if result.neo.name is None:
                result.neo.name = ''
            writable_results.append({'datetime_utc': datetime_to_str(result.time),
                                     'distance_au': float(result.distance),
                                     'velocity_km_s': float(result.velocity),
                                     'neo': {'designation': str(result.neo.designation),
                                             'name': str(result.neo.name),
                                             'diameter_km': result.neo.diameter,
                                             'potentially_hazardous': result.neo.hazardous}})
        json.dump(writable_results, outfile, indent=2)
