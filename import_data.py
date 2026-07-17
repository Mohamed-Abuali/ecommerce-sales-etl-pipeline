import kagglehub


def download_data():
    path = kagglehub.dataset_download("kandeelai22/messy-e-commerce-sales-dataset")

    print("Path to dataset files:", path)
    # Append the filename to the path
    path = path + "/messy_e_commerce_sales.csv"
    return path