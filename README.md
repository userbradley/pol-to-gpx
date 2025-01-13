# Police Data CSV merger

## Stop and Search

Navigate to [https://data.police.uk](https://police.data.uk) and select **Data** at the top

Select all the forces, or just the ones you care about, and then select stop and search

### How to run

Create a python venv

Modify the `main` function to point to the downloaded and **extracted** directory that holds the CSV files

```python
if __name__ == "__main__":
    directory_path = ''
    output_gpx_file = 'stop_and_search_national.gpx'
    main(directory_path, output_gpx_file)
```

To run

```shell
python3 ./main.py
```