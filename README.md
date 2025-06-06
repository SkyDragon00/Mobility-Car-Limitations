# Pico y Placa project
## Author: Doménica Escobar
A Django web application to check if your vehicle can circulate on a given date and time based on local "Pico y Placa" restrictions.

![Can Circulate Screenshot](img/CheckInformation.png)


## Features

- User-friendly web interface to input license plate, date, and time.
- Validates license plate format and checks restrictions based on local rules.
- Displays clear messages if your vehicle can or cannot circulate:

**Vehicle can circulate:**
![Can Circulate Screenshot](img/CanCirculate.png)

**Vehicle cannot circulate:**
![Can Circulate Screenshot](img/CannotCirculate.png)
- Responsive design using Tailwind CSS.

## Requirements

- Python 3.10+
- Django 5.1+
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/SkyDragon00/Mobility-Car-Limitations.git
   cd CarMobility/Backend/carmobility

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    venv\Scripts\activate
3. **Install dependencies:**
    ```sh
    pip install django
4. **Run migrations:**
    ```sh
    python manage.py migrate
5. **Start the development server**
    ```sh
    python manage.py runserver
6. **Open your browser and go to:**
http://127.0.0.1:8000/

## Project Structure
```
CarMobility/
├── Backend/
│   └── carmobility/
│       ├── carmobility/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── ...
│       ├── restrictions/
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── templates/
│       │   │   └── index.html
│       │   └── ...
│       ├── manage.py
│       └── db.sqlite3
└── README.md
```

## Libraries Used
**Django:** Web framework

**Tailwind CSS:** For frontend styling (via CDN)

**Font Awesome:** For icons (via CDN)

**BeautifulSoup:** For testing (only in tests)

## Running Tests
From the Backend/carmobility directory,  run:

    python manage.py test

## What It Can Do
* Check if a vehicle can circulate based on license plate and date/time.
* Handles validation and displays helpful error messages.
* Designed for easy extension to support more complex rules.

## License
[MIT](https://choosealicense.com/licenses/mit/)


Made with Django.
