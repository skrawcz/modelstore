import json
import os

import click
from modelstore import ModelStore
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

import catboost as ctb


def create_model_store(backend) -> ModelStore:
    if backend == "filesystem":
        # By default, create a new local model store
        # in our home directory
        home_dir = os.path.expanduser("~")
        return ModelStore.from_file_system(root_directory=home_dir)
    if backend == "gcloud":
        # The modelstore library assumes you have already created
        # a Cloud Storage bucket and will raise an exception if it doesn't exist
        return ModelStore.from_gcloud(
            os.environ["GCP_PROJECT_ID"],
            os.environ["GCP_BUCKET_NAME"],
        )
    if backend == "aws":
        # The modelstore library assumes that you already have
        # created an s3 bucket where you want to store your models, and
        # will raise an exception if it doesn't exist.
        return ModelStore.from_aws_s3(os.environ["AWS_BUCKET_NAME"])
    if backend == "hosted":
        # To use the hosted model store, you need an API key
        return ModelStore.from_api_key(
            os.environ["MODELSTORE_KEY_ID"], os.environ["MODELSTORE_ACCESS_KEY"]
        )
    raise ValueError(f"Unknown model store: {backend}")


def train():
    diabetes = load_diabetes()
    X_train, _, y_train, _ = train_test_split(
        diabetes.data, diabetes.target, test_size=0.1, random_state=13
    )
    model = ctb.CatBoostRegressor()
    model.fit(X_train, y_train)
    # Skipped for brevity (but important!) evaluate the model
    return model


@click.command()
@click.option(
    "--storage",
    type=click.Choice(
        ["filesystem", "gcloud", "aws", "hosted"], case_sensitive=False
    ),
)
def main(storage):
    model_type = "catboost"
    model_domain = "diabetes-boosting-demo"

    # Create a model store instance
    model_store = create_model_store(storage)

    # In this demo, we train a CatBoostRegressor
    # Replace this with the code to train your own model
    print(f"🤖  Training a {model_type} model...")
    model = train()

    # Create an archive containing the trained model
    print(f"⤴️  Uploading the model to the {model_domain} domain.")
    meta_data = model_store.catboost.upload(model_domain, model=model)

    # The upload returns meta-data about the model that was uploaded
    # This meta-data has also been sync'ed into the cloud storage
    #  bucket
    print(f"✅  Finished uploading the {model_type} model!")
    print(json.dumps(meta_data, indent=4))


if __name__ == "__main__":
    main()
