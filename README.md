# A Geospatial Analysis of London

This is a Streamlit web app designed for London residents, allowing them to explore crime, TfL, air quality, and health data for every borough in London.

## How Does It Work?

---

This project implements a three-tiered architecture. The key components are organised into `controllers`, `services`, and `repositories` directories:

### `controllers`

- Responsible for managing the frontend of the application, using the `streamlit` package to create interactive and user-friendly interfaces.

### `services`

- Handles data cleaning and processing. This layer uses `pandas` and `geopandas` to transform raw data into meaningful insights.

### `repositories`

- Manages data retrieval. Repository classes fetch data from various APIs for crime, TfL, and air quality. Health data is directly retrieved from a database.