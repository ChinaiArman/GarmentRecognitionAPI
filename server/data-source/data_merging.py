import pandas as pd

def merge_datasets(images_csv_path, styles_csv_path, output_csv_path):
    """
    Merges two datasets: one containing image URLs and another containing styles information.
    """
    # Load the datasets
    images_df = pd.read_csv(images_csv_path)
    styles_df = pd.read_csv(styles_csv_path)

    # Convert 'id' in styles_df from int to string to match 'filename' in images_df
    styles_df['id'] = styles_df['id'].astype(str)

    # Remove '.jpg' from filenames in the images dataframe to match the ID format in the styles dataframe
    images_df['filename'] = images_df['filename'].str.replace('.jpg', '', regex=False)

    # Merge the dataframes based on the cleaned 'filename' in images_df and 'id' in styles_df
    merged_df = pd.merge(images_df, styles_df, left_on='filename', right_on='id')

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_csv_path, index=False)
    print(f"Merged dataset saved to {output_csv_path}")

if __name__ == "__main__":
    # Paths to your CSV files (please change this to your own absolute paths if needed to run again)
    images_csv_path = './data-files/images.csv'
    styles_csv_path = './data-files/styles.csv'
    output_csv_path = './data-files/initial_data.csv'

    # Call the merge function
    merge_datasets(images_csv_path, styles_csv_path, output_csv_path)
