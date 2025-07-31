# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import random

# For actual Vertex AI integration, you would import the client library:
# from google.cloud import aiplatform
# from google.oauth2 import service_account

app = Flask(__name__)
# Enable CORS for all origins, which is suitable for development.
# In production, you should restrict this to your frontend's domain(s).
CORS(app)

# --- Vertex AI Model Configuration (PLACEHOLDER) ---
# In a real application, these would be your actual Vertex AI details.
# For this example, we'll simulate the model's response.
# PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
# REGION = os.environ.get("GCP_REGION", "us-central1")
# ENDPOINT_ID = os.environ.get("VERTEX_AI_ENDPOINT_ID", "your-vertex-ai-endpoint-id")

# Initialize Vertex AI client (COMMENTED OUT FOR SIMULATION)
# try:
#     # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set
#     # or provide service account key file path directly.
#     # For Cloud Run, the default service account will handle authentication
#     # if it has the 'Vertex AI User' role.
#     # client_options = {"api_endpoint": f"{REGION}-aiplatform.googleapis.com"}
#     # client = aiplatform.PredictionServiceClient(client_options=client_options)
#     # print("Vertex AI PredictionServiceClient initialized successfully.")
# except Exception as e:
#     print(f"Error initializing Vertex AI PredictionServiceClient: {e}")
#     # In a real app, you might want to exit or log a critical error.

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Receives a question from the frontend, simulates a call to a Vertex AI model,
    and returns a generated answer.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    print(f"Received question: {question}")

    try:
        # --- SIMULATED VERTEX AI MODEL PREDICTION ---
        # In a real scenario, you would replace this with actual Vertex AI API calls.
        # Example of what a real Vertex AI call might look like:
        # instances = aiplatform.gapic.types.Instance(content=question)
        # parameters = aiplatform.gapic.types.PredictionService.PredictRequest.Parameters(
        #     temperature=0.7, max_output_tokens=200
        # )
        # endpoint = client.endpoint_path(PROJECT_ID, REGION, ENDPOINT_ID)
        # response = client.predict(endpoint=endpoint, instances=[instances], parameters=parameters)
        # # Assuming the model returns text directly in 'predictions'
        # generated_answer = response.predictions[0].struct_value.fields['text'].string_value

        # Simulate network latency
        time.sleep(random.uniform(0.5, 2.0))

        # Simple simulated answers based on keywords
        if "ISO 27001" in question:
            generated_answer = "ISO 27001 is an international standard for information security management systems (ISMS). It helps organizations manage the security of assets such as financial information, intellectual property, employee details or information entrusted by third parties."
        elif "SOC 2" in question:
            generated_answer = "SOC 2 (Service Organization Control 2) is an auditing procedure that ensures your service providers securely manage your data to protect the interests of your organization and the privacy of its clients."
        elif "HIPAA" in question:
            generated_answer = "HIPAA (Health Insurance Portability and Accountability Act) is a US law designed to provide privacy standards to protect patients' medical records and other health information provided to health plans, doctors, hospitals and other health care providers."
        elif "GDPR" in question:
            generated_answer = "GDPR (General Data Protection Regulation) is a comprehensive data protection law in the European Union and the European Economic Area. It aims to give individuals control over their personal data and simplify the regulatory environment for international business."
        elif "PCI-DSS" in question:
            generated_answer = "PCI-DSS (Payment Card Industry Data Security Standard) is a set of security standards designed to ensure that all companies that process, store, or transmit credit card information maintain a secure environment."
        elif "CCPA" in question or "CPRA" in question:
            generated_answer = "The CCPA (California Consumer Privacy Act) and CPRA (California Privacy Rights Act) are California state laws that grant consumers more control over their personal information. They provide rights such as knowing what personal information is collected and the right to opt-out of its sale."
        elif "NIST CSF" in question:
            generated_answer = "The NIST Cybersecurity Framework (CSF) is a set of guidelines for private sector organizations to assess and improve their ability to prevent, detect, and respond to cyber attacks. It's widely adopted for managing cybersecurity risks."
        elif "ESG" in question:
            generated_answer = "ESG (Environmental, Social, and Governance) refers to the three central factors in measuring the sustainability and ethical impact of an investment in a company or business. It's increasingly important for corporate responsibility and investor decisions."
        else:
            generated_answer = "I'm sorry, I can only provide information related to ISO 27001, SOC 2, HIPAA, GDPR, PCI-DSS, CCPA/CPRA, NIST CSF, and ESG compliance services based on my current knowledge base. Could you please ask about one of these topics?"

        return jsonify({"answer": generated_answer}), 200

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred while processing your request. Please try again later."}), 500

if __name__ == '__main__':
    # For local development:
    # Set FLASK_RUN_PORT environment variable if you want a different port.
    # e.g., export FLASK_RUN_PORT=8080
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

    # To deploy to Cloud Run:
    # 1. Containerize your application (Dockerfile needed).
    # 2. Build and push the image to Google Container Registry or Artifact Registry.
    # 3. Deploy to Cloud Run:
    #    gcloud run deploy YOUR_SERVICE_NAME --image gcr.io/YOUR_PROJECT_ID/YOUR_IMAGE_NAME --platform managed --region YOUR_REGION --allow-unauthenticated
    #    Make sure the Cloud Run service account has 'Vertex AI User' role.
