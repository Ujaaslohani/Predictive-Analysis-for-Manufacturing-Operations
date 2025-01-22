# Predictive Analysis API

This is a RESTful API designed to predict machine downtime using a manufacturing dataset. It allows users to upload data, train a machine learning model, and make predictions through easy-to-use endpoints.

## Features
- Upload a dataset for training the model.
- Train a Logistic Regression model to predict machine downtime.
- Make predictions based on input parameters like temperature, pressure, etc.
- Preprocess missing values in the dataset automatically.

## Requirements
- Python 3.8+
- Libraries: FastAPI, scikit-learn, joblib, pandas, uvicorn

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ujaaslohani/Predictive-Analysis-for-Manufacturing-Operations.git
   cd Predictive-Analysis-for-Manufacturing-Operations
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate   
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn scikit-learn pandas joblib
   ```

## Running the Application
1. **Start the server**:
   ```bash
   uvicorn predictive_analysis_api:app --reload
   ```

2. **Access the API**:
   - The API will be running at: `http://127.0.0.1:8000`

## Endpoints
### 1. Upload Dataset
**POST** `/upload`
- **Description**: Upload a CSV file containing the dataset.
- **Expected Columns**:
  - `Hydraulic_Pressure`
  - `Coolant_Pressure`
  - `Air_System_Pressure`
  - `Coolant_Temperature`
  - `Hydraulic_Oil_Temperature`
  - `Spindle_Bearing_Temperature`
  - `Spindle_Vibration`
  - `Tool_Vibration`
  - `Spindle_Speed`
  - `Voltage`
  - `Torque`
  - `Cutting`
  - `Downtime`

- **Request Example**:
  Use Postman or cURL to upload a file:
  ```bash
  curl -X POST "http://127.0.0.1:8000/upload" -F "file=@dataset.csv"
  ```
- **Response**:
  ```json
  {
    "message": "Data uploaded successfully."
  }
  ```

### 2. Train the Model
**POST** `/train`
- **Description**: Train a Logistic Regression model on the uploaded dataset.
- **Preprocessing**: Automatically fills missing values with column means.
- **Response Example**:
  ```json
  {
    "message": "Model trained successfully.",
    "accuracy": 0.95,
    "f1_score": 0.93
  }
  ```

### 3. Make Predictions
**POST** `/predict`
- **Description**: Provide input features to get a downtime prediction.
- **Request Format**:
  ```json
  {
    "Hydraulic_Pressure": 125.33,
    "Coolant_Pressure": 4.93,
    "Air_System_Pressure": 6.19,
    "Coolant_Temperature": 35.3,
    "Hydraulic_Oil_Temperature": 47.4,
    "Spindle_Bearing_Temperature": 34.6,
    "Spindle_Vibration": 1.382,
    "Tool_Vibration": 25.274,
    "Spindle_Speed": 19856,
    "Voltage": 368,
    "Torque": 14.202,
    "Cutting": 2.68
  }
  ```
- **Response Example**:
  ```json
  {
    "Downtime": "Machine_Failure",
    "Confidence": 0.87
  }
  ```

## Testing the API
Use Postman or cURL to test each endpoint.

### Example Workflow
1. **Upload Dataset**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/upload" -F "file=@dataset.csv"
   ```

2. **Train the Model**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/train"
   ```

3. **Make a Prediction**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{
       "Hydraulic_Pressure": 125.33,
       "Coolant_Pressure": 4.93,
       "Air_System_Pressure": 6.19,
       "Coolant_Temperature": 35.3,
       "Hydraulic_Oil_Temperature": 47.4,
       "Spindle_Bearing_Temperature": 34.6,
       "Spindle_Vibration": 1.382,
       "Tool_Vibration": 25.274,
       "Spindle_Speed": 19856,
       "Voltage": 368,
       "Torque": 14.202,
       "Cutting": 2.68
   }'
   ```

## Notes
- Ensure the dataset follows the required format.
- Missing values are handled automatically by filling with the column mean.
- Use Postman for an interactive testing experience.

## License
This project is licensed under the MIT License.
