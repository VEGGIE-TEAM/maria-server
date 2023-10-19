from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

# Load model
model = tf.keras.models.load_model("model_sayur.h5")

# Initialize Flask app
app = Flask(__name__)


# Define API endpoint for prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get image file from request
        file = request.files["image"]
        # Load and preprocess the image
        image = Image.open(file).convert("RGB")
        image = image.resize(
            (224, 224)
        )  # Adjust the size according to your model's input shape
        image = np.array(image) / 255.0  # Normalize the image

        # Perform prediction
        prediction = model.predict(np.expand_dims(image, axis=0))
        predicted_class = np.argmax(prediction)

        # Return the predicted class as JSON response
        response = {"predicted_class": str(predicted_class)}
        return jsonify(response)
    except Exception as e:
        print(f"Error during prediction: {e}")  # Print the error for debugging purposes
        return jsonify({"error": "Internal server error"}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3936)
