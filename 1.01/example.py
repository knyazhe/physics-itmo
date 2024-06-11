import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Read in data and examine first 10 rows
flights = pd.read_csv('data.csv')
print(flights.head(10))

# matplotlib histogram
plt.hist(flights['data'], color='blue', edgecolor='black',
         bins=int(180 / 5))


# Add labels
plt.title('Histogram of Arrival Delays')
plt.xlabel('Delay (min)')
plt.ylabel('Flights')
