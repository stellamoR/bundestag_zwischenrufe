import pandas as pd
import os

path = './data/comments_for_labeling.csv'
df = pd.read_csv(path)

# Create a new column for sentiment
df['sentiment'] = None


for index, row in df.iterrows():
    os.system('cls') # clear console
    print(f"Gelabelt: {index}/{len(df)}")

    print(f"Comment Text: {row['comment_text']}")
    print(f"Date: {row['date']}")
    print(f"Preceding Context: {row['preceding_context']}")
    print('-' * 50)
    
    # sentiment input
    while True:
        try:
            sentiment = int(input("Enter sentiment (0 = neutral, 1 = negative, 2 = positive): "))
            if sentiment in [0, 1, 2]:
                break
            else:
                print("Input muss in {0,1,2} sein")
        except ValueError:
            print("Input muss in {0,1,2} sein")
    

    df.at[index, 'sentiment'] = sentiment

# Save the updated dataframe to a new CSV file
output_file = path.replace('.csv', '_labeled.csv')
df.to_csv(output_file, index=False)
print(f"Labeling saved to {output_file}")

