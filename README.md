# Virtual Try On App

A FastAPI-based web service for virtual clothing try-on using AI-powered image processing.

## Features

- Upload a user image and a clothing image to generate a try-on result.
- Automatic background removal from clothing images.
- Face and neck detection for realistic overlay.
- Uses OpenCV, Pillow, rembg, and MediaPipe.

## Getting Started

### Clone the repository

```sh
git clone https://github.com/varun19424/virtual-tryon-app.git
cd virtual-tryon-app
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Run the server

```sh
uvicorn main:app --reload
```

## API Usage

### Endpoint

`POST /tryon/`

#### Form Data

- `user_img`: User image file (PNG/JPG)
- `cloth_img`: Clothing image file (PNG/JPG)

#### Response

- Returns the generated try-on image (`image/png`) or error message.

## File Structure

- `main.py`: FastAPI server and API endpoint.
- [`utils.py`](utils.py): Image processing utilities.
- `requirements.txt`: Python dependencies.
- `output/`: Stores generated result images.
- `uploads/`: Stores uploaded images.