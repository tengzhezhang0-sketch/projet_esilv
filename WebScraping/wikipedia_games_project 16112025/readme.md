# Best-selling Video Games Analysis 

This project scrapes data from Wikipedia and performs a simple exploratory analysis of the **best-selling video games of all time**.  
The workflow is split into two main parts:

1. **`scrape_games.ipynb`** – Web scraping & data preparation  
2. **`analysis.ipynb`** – KPI calculation & visualization

The goal is to demonstrate basic web scraping with BeautifulSoup and simple data analysis with pandas and matplotlib.

---

## 1. Data Source

All data in this project comes from the Wikipedia page:

> **“List of best-selling video games”**  
> <https://en.wikipedia.org/wiki/List_of_best-selling_video_games>

From this page, we focus on the main table of best-selling video games.

---

## 2. Tools and Libraries

The project is implemented in **Python** and uses the following tools:

- **Python 3.x**
- **Jupyter Notebook**
- **Libraries**
  - `requests` – send HTTP requests to download the webpage
  - `beautifulsoup4` – parse the HTML and extract the table
  - `pandas` – store, clean, and analyze tabular data
  - `matplotlib` – create basic bar charts for visualization
  - `re` – regular expressions for extracting numbers and years from strings

---

## 3. Project Structure

The project consists of the following files:

    .
    ├─ README.md              # Project description (this file)
    ├─ requirements.txt       # Python dependencies
    ├─ scrape_games.ipynb     # Web scraping + data preparation
    └─ analysis.ipynb         # Exploratory analysis + visualizations

- `scrape_games.ipynb` handles downloading the HTML, parsing the table, and transforming the raw text into a clean dataset.  
- `analysis.ipynb` loads the cleaned data and computes descriptive statistics and visualizations.  
- `requirements.txt` lists all libraries needed to run the notebooks in a fresh environment.  

---

## 4. Scraping & Data Preparation (`scrape_games.ipynb`)

This notebook is responsible for collecting and preparing the dataset used in the analysis.

### 4.1. Steps

1. **Import libraries**  
   Import `requests`, `BeautifulSoup` from `bs4`, `pandas`, `re`, and any other utilities needed.

2. **Download the Wikipedia page**  
   Use `requests.get()` to fetch the HTML content from the *“List of best-selling video games”* URL and check the status code.

3. **Parse the HTML**  
   - Create a `BeautifulSoup` object with the HTML and `"html.parser"`.  
   - Locate the main table containing the best-selling video games.

4. **Extract table data**  
   For each row in the table (skipping the header), extract columns such as:

   - `Title`  
   - `Sales (million units)`  
   - `Platform(s)`  
   - `Initial release date`  
   - `Developer` / `Publisher` 

   Clean up raw strings, remove footnote markers (for example `[1]`, `[a]`), and strip whitespace.

5. **Convert to a DataFrame**  
   - Store all rows in a Python list of dictionaries.  
   - Convert the list to a `pandas.DataFrame` with clear column names, such as:
     - `title`  
     - `sales_millions`  
     - `platforms`  
     - `release_date`  
     - `developer`  
     - `publisher`  

6. **Data cleaning & type conversion**  
   Use `re` and pandas string methods to:

   - Extract numeric sales values from strings (for example `"82.90 million"` → `82.9`).  
   - Extract the release year from the date string (for example `"November 18, 2011"` → `2011`).  

   Convert:

   - `sales_millions` → `float`  
   - `release_year` → `int`  

7. **Save the cleaned dataset**  
   Save the final DataFrame to a CSV file so it can be reused in the analysis notebook, for example:

        df.to_csv("best_selling_games.csv", index=False)

At the end of this notebook, you should have a clean dataset that mirrors the Wikipedia table of best-selling video games.

---

## 5. Analysis & KPIs (`analysis.ipynb`)

This notebook performs a simple exploratory analysis on the cleaned dataset and calculates several key performance indicators (KPIs).

### 5.1. Data Overview

- Load the cleaned CSV file exported from `scrape_games.ipynb`.  
- Inspect the main columns (title, series, platform, sales, year, etc.).  
- Check for missing or inconsistent values and apply basic cleaning if needed.  

### 5.2. Example KPIs

The notebook implements ten KPIs. Examples include:

1. **Top 10 Best-selling Games (Bar Chart)**  
   - Sort the games by `Sales_million` in descending order.  
   - Take the top 10 and visualize game title vs. sales in a bar chart.  

2. **Total Sales of All Games**  
   - Sum the `Sales_million` column to obtain total sales (in millions of units) for all games in the dataset.  

3. **Median Sales of All Games**  
   - Compute the median of `Sales_million` to understand the “middle” sales level and compare it with the average.  

4. **Share of Top 5 Games (%)**  
   - Sum the sales of the top 5 games.  
   - Divide by total sales and multiply by 100 to see how much of the market the top hits capture.  

5. **Number of Games by Release Year**  
   - Count how many games were released in each year.  
   - Show the result as a bar chart of year vs. number of games.  

6. **Total Sales by Release Year**  
   - Aggregate `Sales_million` by release year.  
   - Visualize total sales per year to see which years contributed the most.  

7. **Sales Distribution by Range**  
   - Bucket games into sales ranges (e.g. 0–20, 20–40, 40–60, 60–80, 80+ million).  
   - Count how many games fall into each range to understand the overall sales distribution.  

8. **Sales by Series**  
   - Group games by franchise/series.  
   - Sum sales within each series and rank them to see which series are the most successful overall.  

9. **Single-platform vs Multi-platform Games**  
   - Classify each title as “Single-platform” or “Multi-platform” based on the platform column.  
   - Count how many games fall into each category to compare their prevalence.  

10. **Oldest vs Newest Game Sales**  
    - Identify the oldest and most recently released games using the `Year` column.  
    - Report their titles, release years, and sales to compare early and recent best-sellers.  

### 5.3. Visualizations

- Bar charts for rankings (e.g. Top 10 Best-selling Games, number of games per year).  
- Aggregated charts over time (e.g. total sales by release year).  
- Simple distribution plots or tables summarizing sales ranges, series-level sales, and platform categories.  

---

## 6. How to Run the Project

### 6.1. Install dependencies

1. Ensure **Python 3.x** is installed.  
2. Create and activate a virtual environment.  
3. Install the required libraries using `requirements.txt`:

        pip install -r requirements.txt

### 6.2. Run the scraping notebook

1. Start Jupyter Notebook or JupyterLab:

        jupyter notebook

2. Open `scrape_games.ipynb`.  
3. Run all cells from top to bottom.  
4. Verify that the CSV file is created in the project folder.

### 6.3. Run the analysis notebook

1. In the same Jupyter session, open `analysis.ipynb`.  
2. Make sure the path to `best_selling_games.csv` matches the actual location.  
3. Run all cells from top to bottom.  
4. Review the KPIs and charts produced by the notebook.

---



