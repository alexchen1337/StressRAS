import kagglehub

# Download latest version
path = kagglehub.dataset_download("ryanluong1/valorant-champion-tour-2021-2023-data")

print("Path to dataset files:", path)