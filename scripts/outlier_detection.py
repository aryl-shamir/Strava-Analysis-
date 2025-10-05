def remove_outliers(df):
    #detecting outliers based on the scatter plot of distance and avg_pace, I don't Run at a pace of 8min/km
    # So i will let the Threshold = 9, for the avg_pace 
    outlier_indices = df[(df['distance'] > 0) & (df['distance'] < 15) & (df['avg_pace'] > 9) ].index.tolist()

    return df.drop(outlier_indices)