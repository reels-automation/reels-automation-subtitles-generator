import unicodedata
import re
import requests
import os
import zipfile
import shutil
import tempfile
from setttings import MODELS_PATH

def sanitize_attribute(attribute: str):
    """Sanitiza un input para que no contenga caracteres que no puedan ser parseados

    Args:
        attribute (str):

    Returns:
        (str):
    """
    if attribute is not None:
        result = (
            unicodedata.normalize("NFKD", attribute)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        # Modify the regex to exclude dots
        result = re.sub(r"[^a-zA-Z0-9._-]", " ", result)
        result = result.strip()
        return result
    return None

def download_and_extract_voice_models(api_url, download_dir=MODELS_PATH):
    os.makedirs(download_dir, exist_ok=True)

    response = requests.get(api_url)
    response.raise_for_status()
    model_list = response.json()

    for model in model_list:
        model_name = model["object_name"]
        model_url = model["object_url"]
        extracted_folder = os.path.join(download_dir, model_name.replace('.zip', ''))

        if os.path.exists(extracted_folder):
            print(f"Model folder '{extracted_folder}' already exists. Skipping download and extraction.")
            continue

        print(f"Downloading {model_name} from {model_url}...")
        file_path = os.path.join(download_dir, model_name)
        with requests.get(model_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"Extracting {model_name}...")
        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)

            # Check if extracted folder has a single top-level directory
            entries = os.listdir(tmpdirname)
            if len(entries) == 1 and os.path.isdir(os.path.join(tmpdirname, entries[0])):
                nested_folder = os.path.join(tmpdirname, entries[0])
                os.makedirs(extracted_folder, exist_ok=True)
                for item in os.listdir(nested_folder):
                    shutil.move(os.path.join(nested_folder, item), extracted_folder)
            else:
                # If no single folder, move all extracted files directly
                os.makedirs(extracted_folder, exist_ok=True)
                for item in entries:
                    shutil.move(os.path.join(tmpdirname, item), extracted_folder)

        # Delete the ZIP file after extraction
        os.remove(file_path)

    print("All models downloaded and extracted or already present.")


