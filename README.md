# movie-sorter

A Python CLI for managing a DVD ripping workflow. Handles each stage of the pipeline:
sorting ripped files, compressing via HandBrakeCLI, and uploading to a NAS.

## Workflow
1. **Sort** — moves ripped `.mkv` files into compression or upload queues based on size
2. **Compress** — runs HandBrakeCLI on queued files, tracks ETA and stats
3. **Upload** — transfers ready files to a NAS

## Requirements
- Python 3
- [HandBrakeCLI](https://handbrake.fr/downloads2.php)
- External hard drive mounted at the configured path

## Usage
```sh
python main.py
```
