import csv
import os
import glob
import pandas as pd
import gpxpy
import gpxpy.gpx

def merge_csv_files(directory):
    """
    Traverses a directory recursively, finds all files with "stop-and-search.csv"
    in their name, and merges them into a single CSV file.

    Args:
      directory: The root directory to search.
    """

    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if "stop-and-search.csv" in file:
                all_files.append(os.path.join(root, file))

    if not all_files:
        print("No 'stop-and-search.csv' files found in the directory.")
        return

    # Use pandas to efficiently concatenate the CSV files
    df_list = [pd.read_csv(file) for file in all_files]
    merged_df = pd.concat(df_list, ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv("merged_stop-and-search.csv", index=False)
    print("Merged data saved to 'merged_stop-and-search.csv'")

def csv_to_gpx(csv_file, gpx_file):
    """
    Converts a CSV file of stop and search data to a GPX file.

    Args:
      csv_file: Path to the CSV file.
      gpx_file: Path to the output GPX file.
    """
    gpx = gpxpy.gpx.GPX()

    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])

                # Create a waypoint for the stop and search
                waypoint = gpxpy.gpx.GPXWaypoint(latitude=lat, longitude=lon)

                # Add description with details from the CSV
                description = (
                    f"Type: {row['Type']}\n"
                    f"Date: {row['Date']}\n"
                    f"Gender: {row['Gender']}\n"
                    f"Age range: {row['Age range']}\n"
                    f"Self-defined ethnicity: {row['Self-defined ethnicity']}\n"
                    f"Officer-defined ethnicity: {row['Officer-defined ethnicity']}\n"
                    f"Legislation: {row['Legislation']}\n"
                    f"Object of search: {row['Object of search']}\n"
                    f"Outcome: {row['Outcome']}"
                )
                waypoint.description = description

                gpx.waypoints.append(waypoint)
            except ValueError:
                # Skip rows with missing or invalid coordinates
                pass

    # Write the GPX data to the output file
    with open(gpx_file, 'w', encoding='utf-8') as gpxfile:
        gpxfile.write(gpx.to_xml())

def main(directory, gpx_file):
    """
    Merges all CSV files in a directory and then converts the merged data to a GPX file.

    Args:
      directory: The directory containing the CSV files.
      gpx_file: The name of the output GPX file.
    """
    merge_csv_files(directory)
    csv_to_gpx('merged_stop-and-search.csv', gpx_file)

# Example usage:
if __name__ == "__main__":
    directory_path = '/Users/bradley.stannard/Downloads/0bc332da6631433b8289ab4bdf40bcb9016d0bb4'
    output_gpx_file = 'stop_and_search_national.gpx'
    main(directory_path, output_gpx_file)