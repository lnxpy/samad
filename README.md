### Installation

Clone this repo. `cd` into it and..

```sh
pip install -r requirements.txt
```

Start the server via:

```sh
uvicorn main:app --reload --host 0.0.0.0
```

Create a local network with your phone and laptop and reach the service from `LAPTOP_IP:8000/docs`. `LAPTOP_IP` is your laptop's local IP address.

### Requirements
- Python >= 3.10
- pip
