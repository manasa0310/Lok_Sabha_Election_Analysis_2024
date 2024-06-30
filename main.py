import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


# Function to scrape and parse the ECI data
def scrape_eci_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: Status code {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table')

    if not table:
        raise Exception("Could not find the results table on the page")

    data = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 4:
            party = cols[0].text.strip()
            won = int(cols[1].text.strip())
            leading = int(cols[2].text.strip())
            total = int(cols[3].text.strip())
            party_link = cols[1].find('a')['href']  # Extract party-wise results page link
            data.append({
                'Party': party,
                'Won': won,
                'Leading': leading,
                'Total': total,
                'Link': party_link
            })

    return pd.DataFrame(data)


def scrape_candidate_data(url, party_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}: {str(e)}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table-striped')

    if not table:
        print(f"Could not find the candidate data table on the page: {url}")
        return pd.DataFrame()

    data = []
    rows = table.find_all('tr')

    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 5:
            total_votes = cols[3].text.strip().replace(',', '')
            margin = cols[4].text.strip().replace(',', '')

            data.append({
                'Serial Number': cols[0].text.strip(),
                'Constituency': cols[1].text.strip(),
                'Winning Candidate': cols[2].text.strip(),
                'Total Votes': int(total_votes) if total_votes != '-' else 0,
                'Margin': int(margin) if margin != '-' else 0,
                'Party': party_name  # Add the party name to each candidate's data
            })

    if not data:
        print(f"No data found in the table for URL: {url}")

    return pd.DataFrame(data)


def dominance_of_top_parties(df):
    total_seats = df['Total'].sum()
    top_5_share = df.nlargest(5, 'Total')['Total'].sum() / total_seats
    top_10_share = df.nlargest(10, 'Total')['Total'].sum() / total_seats

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Top 5 Parties', 'Top 10 Parties'], [top_5_share, top_10_share])
    ax.set_title("Dominance of Top Parties")
    ax.set_ylabel("Share of Total Seats")
    ax.set_ylim(0, 1)
    for i, v in enumerate([top_5_share, top_10_share]):
        ax.text(i, v, f'{v:.2%}', ha='center', va='bottom')
    plt.tight_layout()
    fig.savefig('dominance_of_top_parties.png')

    return f"Dominance of top parties:\nTop 5 parties hold {top_5_share:.2%} of seats\nTop 10 parties hold {top_10_share:.2%} of seats"


def total_number_of_parties(df):
    total_parties = len(df)
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Total Parties'], [total_parties])
    plt.title('Total Number of Parties')

    # Annotate the bar with the total number of parties
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom',
                 ha='center')

    plt.savefig('total_number_of_parties.png')
    return f"Total number of parties: {total_parties}"


def parties_with_more_than_10_seats(df):
    large_parties = df[df['Total'] > 10]
    plt.figure(figsize=(12, 6))
    bars = plt.bar(large_parties['Party'], large_parties['Total'])
    plt.title('Parties with More Than 10 Seats')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=45, ha='right')

    # Annotate bars with the number of seats
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval),
                 va='bottom')  # va='bottom' positions the text above the bar

    plt.tight_layout()
    plt.savefig('parties_with_more_than_10_seats.png')
    return f"Parties with more than 10 seats:\n{large_parties[['Party', 'Total']].to_string(index=False)}"


def top_5_parties_analysis(df):
    top_5 = df.nlargest(5, 'Total')
    total_seats = df['Total'].sum()
    top_5['Percentage'] = top_5['Total'] / total_seats * 100
    plt.figure(figsize=(12, 6))
    plt.bar(top_5['Party'], top_5['Percentage'])
    plt.title('Top 5 Parties Analysis')
    plt.ylabel('Percentage of Total Seats')
    plt.xticks(rotation=45, ha='right')
    for i, v in enumerate(top_5['Percentage']):
        plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig('top_5_parties_analysis.png')
    return f"Top 5 parties analysis:\n{top_5[['Party', 'Total', 'Percentage']].to_string(index=False)}"


def seat_share_analysis(df):
    total_seats = df['Total'].sum()
    df['Seat Share'] = df['Total'] / total_seats

    # Group parties with less than 1% seat share into 'Others'
    threshold = 0.01
    small_parties = df[df['Seat Share'] < threshold]
    if not small_parties.empty:
        other_share = small_parties['Seat Share'].sum()
        other_total_seats = other_share * total_seats
        df = df[df['Seat Share'] >= threshold]

        # Create a new DataFrame for "Others"
        others_df = pd.DataFrame([['Others', other_share, other_total_seats]], columns=['Party', 'Seat Share', 'Total'])
        df = pd.concat([df, others_df], ignore_index=True)

    plt.figure(figsize=(20, 12))
    plt.pie(df['Seat Share'], labels=df['Party'], autopct='%1.1f%%', textprops={'fontsize': 14})  # Adjust fontsize here
    plt.title('Seat Share Analysis', fontsize=16)  # Adjust title fontsize
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('seat_share_analysis.png')

    return f"Seat Share Analysis:\n{df[['Party', 'Seat Share']].to_string(index=False)}"


def parties_with_minimum_5percent_seats(df):
    total_seats = df['Total'].sum()
    relevant = df[df['Total'] > total_seats * 0.05]  # Parties with more than 5% seats

    plt.figure(figsize=(12, 6))
    bars = plt.bar(relevant['Party'], relevant['Total'], color='skyblue')

    plt.title('Parties with More than 5% of Seats')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=45, ha='right')

    # Adding labels within the bars to avoid overflow
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval - 10, int(yval), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig('parties_with_minimum_5percent_seats.png')

    return f"Number of relevant parties (>5% of seats): {len(relevant)}\n{relevant[['Party', 'Total']].to_string(index=False)}"


def single_seat_parties(df):
    single_seat = df[df['Total'] == 1]
    num_parties = len(single_seat)

    # Adjusting the figure size based on the number of parties
    plt.figure(figsize=(num_parties * 0.5, 8))

    bars = plt.bar(single_seat['Party'], single_seat['Total'], color='skyblue')
    plt.title('Single-Seat Parties')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=90)

    # Adding value labels on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, int(yval), ha='center', va='bottom')

    # Adjust y-axis limits to provide space for the labels
    plt.ylim(0, max(single_seat['Total']) * 1.2)

    plt.tight_layout()
    plt.savefig('single_seat_parties.png')
    return f"Number of single-seat parties: {num_parties}\n{single_seat['Party'].to_string(index=False)}"


# candidate data

def top_5_candidates_by_margin(candidate_df):
    top_5 = candidate_df.nlargest(5, 'Margin')

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top_5['Winning Candidate'], top_5['Margin'])
    ax.set_title("Top 5 Candidates by Winning Margin")
    ax.set_ylabel("Margin")
    plt.xticks(rotation=45, ha='right')
    for i, v in enumerate(top_5['Margin']):
        ax.text(i, v, f'{v:,}', ha='center', va='bottom')
    plt.tight_layout()
    fig.savefig('top_5_candidates_by_margin.png')

    return f"Top 5 candidates by winning margin:\n{top_5[['Winning Candidate', 'Party', 'Constituency', 'Margin']].to_string(index=False)}"


def least_5_candidates_by_margin(candidate_df):
    least_5 = candidate_df.nsmallest(5, 'Margin')

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(least_5['Winning Candidate'], least_5['Margin'])
    ax.set_title("Least 5 Candidates by Winning Margin")
    ax.set_ylabel("Margin")
    plt.xticks(rotation=45, ha='right')
    for i, v in enumerate(least_5['Margin']):
        ax.text(i, v, f'{v:,}', ha='center', va='bottom')
    plt.tight_layout()
    fig.savefig('least_5_candidates_by_margin.png')

    return f"Least 5 candidates by winning margin:\n{least_5[['Winning Candidate', 'Party', 'Constituency', 'Margin']].to_string(index=False)}"


def top_5_candidates_by_margin_top_10_parties(df, candidate_df):
    top_10_parties = df.nlargest(10, 'Total')['Party'].tolist()
    results = []
    fig, axs = plt.subplots(5, 2, figsize=(20, 25))
    axs = axs.ravel()

    for i, party in enumerate(top_10_parties):
        party_candidates = candidate_df[candidate_df['Party'] == party]
        top_5 = party_candidates.nlargest(5, 'Margin')
        results.append(f"\n{party}:\n{top_5[['Winning Candidate', 'Constituency', 'Margin']].to_string(index=False)}")

        axs[i].bar(top_5['Winning Candidate'], top_5['Margin'])
        axs[i].set_title(f"{party}")
        axs[i].set_xticklabels(top_5['Winning Candidate'], rotation=45, ha='right')
        axs[i].set_ylabel('Margin')
        for j, v in enumerate(top_5['Margin']):
            axs[i].text(j, v, f'{v:,}', ha='center', va='bottom')

    plt.tight_layout()
    fig.savefig('top_5_candidates_by_margin_top_10_parties.png')
    return "Top 5 candidates by margin for each top 10 party:" + '\n'.join(results)


def least_5_candidates_by_margin_top_10_parties(df, candidate_df):
    top_10_parties = df.nlargest(10, 'Total')['Party'].tolist()
    results = []
    fig, axs = plt.subplots(5, 2, figsize=(20, 25))
    axs = axs.ravel()

    for i, party in enumerate(top_10_parties):
        party_candidates = candidate_df[candidate_df['Party'] == party]
        least_5 = party_candidates.nsmallest(5, 'Margin')
        results.append(f"\n{party}:\n{least_5[['Winning Candidate', 'Constituency', 'Margin']].to_string(index=False)}")

        axs[i].bar(least_5['Winning Candidate'], least_5['Margin'])
        axs[i].set_title(f"{party}")
        axs[i].set_xticklabels(least_5['Winning Candidate'], rotation=45, ha='right')
        axs[i].set_ylabel('Margin')
        for j, v in enumerate(least_5['Margin']):
            axs[i].text(j, v, f'{v:,}', ha='center', va='bottom')

    plt.tight_layout()
    fig.savefig('least_5_candidates_by_margin_top_10_parties.png')
    return "Least 5 candidates by margin for each top 10 party:" + '\n'.join(results)


def main():
    url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
    df = scrape_eci_data(url)

    # Scrape candidate data for all parties
    candidate_data = []
    for _, row in df.iterrows():
        try:
            party_url = f"https://results.eci.gov.in/PcResultGenJune2024/{row['Link']}"
            print(f"Scraping data for party {row['Party']} from URL: {party_url}")
            party_data = scrape_candidate_data(party_url, row['Party'])
            if not party_data.empty:
                candidate_data.append(party_data)
            else:
                print(f"No data found for party {row['Party']}")
        except Exception as e:
            print(f"Error scraping data for party {row['Party']}: {str(e)}")

    if not candidate_data:
        print("No candidate data could be scraped. Please check the website structure and URLs.")
        candidate_df = pd.DataFrame()
    else:
        candidate_df = pd.concat(candidate_data, ignore_index=True)

    insights = [
        top_5_parties_analysis(df),
        seat_share_analysis(df),
        single_seat_parties(df),
        dominance_of_top_parties(df),
        total_number_of_parties(df),
        parties_with_minimum_5percent_seats(df),
        parties_with_more_than_10_seats(df),
    ]

    if not candidate_df.empty:
        insights.extend([
            top_5_candidates_by_margin(candidate_df),
            top_5_candidates_by_margin_top_10_parties(df, candidate_df),
            least_5_candidates_by_margin(candidate_df),
            least_5_candidates_by_margin_top_10_parties(df, candidate_df)
        ])
    else:
        print("No candidate-specific insights could be generated due to lack of data.")

    # Print insights and save to file
    with open('election_insights.txt', 'w') as f:
        for insight in insights:
            print(insight)
            f.write(insight + '\n\n')


if __name__ == "__main__":
    main()
