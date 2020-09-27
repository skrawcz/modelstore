import json
import os

import click
import tensorflow as tf
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

from modelstore import ModelStore


def create_model_store(backend) -> ModelStore:
    if backend == "filesystem":
        # By default, create a new local model store one directory up
        #  from the current example that is being run
        return ModelStore.from_file_system(root_directory="..")
    if backend == "gcloud":
        # The modelstore library assumes you have already created
        # a Cloud Storage bucket and will raise an exception if it doesn't exist
        return ModelStore.from_gcloud(
            os.environ["GCP_PROJECT_ID"], os.environ["GCP_BUCKET_NAME"],
        )
    if backend == "aws":
        # The modelstore library assumes that you already have
        # created an s3 bucket where you want to store your models, and
        # will raise an exception if it doesn't exist.
        return ModelStore.from_aws_s3(os.environ["AWS_BUCKET_NAME"])


def train():
    diabetes = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(
        diabetes.data, diabetes.target, test_size=0.1, random_state=13
    )
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(5, activation="relu", input_shape=(10,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=10)
    # Skipped for brevity (but important!) evaluate the model
    return model


@click.command()
@click.option(
    "--storage",
    type=click.Choice(["filesystem", "gcloud", "aws"], case_sensitive=False),
)
def main(storage):
    model_type = "tensorflow"
    model_domain = "diabetes-boosting-demo"

    # Create a model store instance
    model_store = create_model_store(storage)

    # In this demo, we train a single layer net
    # Replace this with the code to train your own model
    print(f"🤖  Training a {model_type} model...")
    model = train()

    # Create an archive containing the trained model
    print("📦  Creating a model archive...")
    archive = model_store.tensorflow.create_archive(model=model)

    # Upload the archive to the model store
    # The first string is the model's domain - which helps you to group
    # many models that are trained on the same target together
    print(f"⤴️  Uploading the archive to the {model_domain} domain.")
    meta = model_store.upload(model_domain, archive)

    # Optional: the artifacts.tar.gz file is generated into the current
    # working directory and you can remove them if you do not
    # need a local copy
    os.remove(archive)

    # The upload returns meta-data about the model that was uploaded
    # This meta-data has also been sync'ed into the cloud storage
    #  bucket
    print(f"✅  Finished uploading the {model_type} model!")
    print(json.dumps(meta, indent=4))


if __name__ == "__main__":
    main()