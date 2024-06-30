# Lok Sabha Election Analysis(2024)

This project analyzes election data from the Election Commission of India (ECI) website for the June 2024 elections, providing insights into party-wise and candidate-wise results.

## Overview

The project uses web scraping techniques to extract data from the ECI results website and performs detailed analysis and visualization using Python libraries like `pandas` for data manipulation and `matplotlib` for visualization.

## Features

- **Data Scraping**: Scrapes election results data including party-wise seat distribution and candidate details.
- **Visualization**: Generates various charts and graphs to visualize election insights, such as seat share distribution, top parties, and candidate margins.
- **Insight Generation**: Summarizes key findings in a text file (`election_insights.txt`) for easy reference.

## Project Structure

- **`main.py`**: Python script for data scraping, analysis, and visualization.
- **`election_insights.txt`**: Text file containing summarized insights from the analysis.

- **Visualization Outputs**:
  - `dominance_of_top_parties.png`: Bar chart showing top parties by seat share.
  - `total_number_of_parties.png`: Bar chart displaying the total number of contesting parties.
  - `parties_with_more_than_10_seats.png`: Bar chart showing parties with more than 10 seats.
  - `top_5_parties_analysis.png`: Bar chart and analysis of the top 5 parties by seat share.
  - `seat_share_analysis.png`: Pie chart illustrating the seat share distribution among parties.
  - `parties_with_minimum_5percent_seats.png`: Bar chart showing parties with more than 5% of total seats.
  - `single_seat_parties.png`: Bar chart displaying parties with only one seat.
  - `top_5_candidates_by_margin.png`: Bar chart and analysis of the top 5 winning candidates by margin.
  - `least_5_candidates_by_margin.png`: Bar chart and analysis of the least 5 winning candidates by margin.
  - `top_5_candidates_by_margin_top_10_parties.png`: Multiple bar charts showing top 5 candidates by margin for each of the top 10 parties.
  - `least_5_candidates_by_margin_top_10_parties.png`: Multiple bar charts showing least 5 candidates by margin for each of the top 10 parties.

## Usage

1. **Setup**: Ensure Python 3.x and required libraries (`requests`, `BeautifulSoup`, `pandas`, `matplotlib`) are installed.
   
2. **Execution**: Run `main.py` to initiate data scraping, analysis, and visualization.

3. **Results**: Review generated charts and graphs in the `plots` directory and insights in `election_insights.txt` for detailed election analysis.

## Dependencies

- `requests`: HTTP library for making requests.
- `BeautifulSoup`: Library for parsing HTML content.
- `pandas`: Data manipulation library.
- `matplotlib`: Visualization library for creating charts and graphs.

## Notes

- Adjustments may be needed for any changes in the ECI website structure or data format.
- Proper exception handling is implemented to manage errors during data scraping.


## Acknowledgments

- Data sourced from the Election Commission of India (ECI).
- Inspired by the need for transparent and accessible election data analysis.
