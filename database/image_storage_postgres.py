"""
Store images into postgres database
"""

import os
import tempfile
import logging
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters
db_params = {
    "dbname": "image_database",
    "user": "postgres_user",
    "password": "postgres123",
    "host": "localhost",
}


def save_image_to_database(image_path, image_name):
    """
    Get the image path and name and store into database
    :param image_path: pass the image path
    :param image_name: pass the image name
    :return: None
    """
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        with open(image_path, "rb") as file:
            image_data = file.read()

        # Insert the image into the database
        cursor.execute(
            "INSERT INTO mywork.images (name, image_data) VALUES (%s, %s)",
            (image_name, psycopg2.Binary(image_data)),
        )
        connection.commit()
        logging.info("Image saved successfully!")

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error while saving image to PostgreSQL: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection is closed.")


# # Example usage
# image_path = '../uploads/sample.jpg'
# image_name = 'sample.jpg'
# save_image_to_database(image_path, image_name)


# Route to retrieve all images
@app.route("/images", methods=["GET"])
def get_all_images():
    """

    :return: JSON format of all images stored in database
    """
    try:
        # Connect to the database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Retrieve all images from the database
        cursor.execute("SELECT name, image_data FROM mywork.images")
        images = cursor.fetchall()

        # Close the database connection
        cursor.close()
        connection.close()

        # Create a temporary directory to store the images
        temp_dir = tempfile.mkdtemp()

        # Save each image to a temporary file and add its path to the response
        image_paths = []
        for name, image_data in images:
            temp_file_path = os.path.join(temp_dir, name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(image_data)
            image_paths.append(temp_file_path)

        # Return the list of image paths
        return jsonify({"images": image_paths}), 201

    except (Exception, psycopg2.Error) as error:
        logging.error(f"error {str(error)}")
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
