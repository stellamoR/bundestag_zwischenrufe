import pandas as pd
import os

path = './data/comments_for_labeling_robin_labeled_labeled.csv'
df = pd.read_csv(path)


# Create a new column for sentiment

if 'sentiment' not in df.columns:
    df['sentiment'] = -1

start_index = df[df['sentiment'] == -1].index[0]

print(start_index)

for index, row in df.iloc[start_index:].iterrows():
    os.system('cls') # clear console
    print(f"Gelabelt: {index}/{len(df)} | Enter -1 to abort and save progress")

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
            elif sentiment == -1:
                print(f"Aborting, your current labeling process will be saved to {path.replace('.csv', '_labeled.csv')}")
                print(f"Next time, set 'path'-variable to {path.replace('.csv', '_labeled.csv')} in order to not lose your progress")
                output_file = path.replace('.csv', '_labeled.csv')
                df.to_csv(output_file, index=False)
                exit()
            else:
                print("Input muss in {0,1,2} sein")
        except ValueError:
            print("Input muss in {0,1,2} sein")
    

    df.at[index, 'sentiment'] = sentiment


# Save the updated dataframe to a new CSV file
output_file = path.replace('.csv', '_labeled.csv')
df.to_csv(output_file, index=False)
print(f"Labeling saved to {output_file}")

