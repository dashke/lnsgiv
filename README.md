# lnsgiv
Local Nintendo Switch Game Info Viewer

This project provides a user-friendly interface for viewing detailed information about various games, with features like filtering by rating, genre, and title. The viewer also supports dark mode for better readability in different lighting conditions.

![lnsgiv](https://github.com/dashke/lnsgiv/assets/77551811/389ac662-fd56-48f3-aa3f-b233acd48961)

## Features

- **Filtering:** Filter games based on rating, genre, and title.
- **Dark Mode:** Toggle between light and dark mode.
- **Game Details:** View detailed information about each game, including ratings, summary, genres, platforms, and screenshots.
- **Interactive Tags:** Click on tags to filter games by genre.

## Getting Started

### Prerequisites

- Python 3.x installed on your machine
- IGDB API key (sign up at [IGDB](https://www.igdb.com/api) to get your API key)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/dashke/lnsgiv.git
    cd lnsgiv
    ```

2. Install the required Python packages:
    ```sh
    pip install requests
    ```

3. Add your IGDB API key to the `ns_db_scraper.py` script:
    ```python
    API_KEY = 'your_igdb_api_key'
    ```

### Usage

1. **Scrape Game Data:**
    - Place your dumped game files in a folder. Games should have titles like "name [NSP]" or "name [NSZ]".
    - Run the scraper script:
        ```sh
        python ns_db_scraper.py
        ```
    - The script will remove obsolete information, append only new games, or start scraping from the start based on your preference.

2. **Upload JSON File:**
    - Open the `index.html` file in your preferred web browser.
    - Click on the "Select JSON File" button and choose the JSON file created by the scraper script.
    - The data will be loaded and displayed on the page.

3. **Filter Games:**
    - Use the filter section to input minimum and maximum ratings, tags, and titles to narrow down the game list.
    - Click "Filter" to apply the filters or "Clear Filters" to reset them.

4. **Toggle Dark Mode:**
    - Click the moon icon (🌙) in the header to switch to dark mode.
    - Click the sun icon (🌞) to switch back to light mode.

5. **View Game Details:**
    - Click on any game to view its detailed information.
    - Detailed view includes summary, genres, platforms, and screenshots if available.

## Project Structure

- `index.html`: The main HTML file containing the structure and layout of the application.
- `ns_db_scraper.py`: A Python script for scraping game data.


## Feel free to contact me
Spread the word and share this project with others. Thanks!
