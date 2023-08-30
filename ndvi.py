import openeo

#conect to backennd, uncomment to authenticate using oidc
connection = openeo.connect("openeo.cloud")#.authenticate_oidc()

# Get all collection ids
print(connection.list_collection_ids())

# print all processes
#print(connection.list_processes())

# Load Sentinel-2 collection
datacube = connection.load_collection(
        "SENTINEL2_L2A",
        spatial_extent={"west": 7.5, "south": 50.1, "east": 8.5, "north": 51.1},
        temporal_extent=["2021-01-01", "2021-01-31"],
        bands=["B04", "B08"]
        )

# Compute NDVI vegetation index
#datacube = datacube.ndvi(nir = "B08", red = "B04", target_band = "NDVI")
datacube = datacube.process(
        process_id="ndvi", 
        arguments={
            "data": datacube, 
            "nir": "B08", 
            "red": "B04"}
        )

# Compute maximum over time
datacube = datacube.reduce_dimension(
        reducer="max",
        dimension = "t"
        )

# Export as GeoTIFF
result = datacube.save_result("GTiff")

# login:
connection.authenticate_oidc()

# Execute processes
# Creating a new job at the back-end by sending the datacube information.
job = result.create_job()

# Starts the job and waits until it finished to download the result.
job.start_and_wait()
job.get_results().download_files(".")

