import pandas as pd
import repository as repo
import plotly.express as plt
import re

# TODO - avg score of trip advisor set
# show more columns
pd.set_option('display.max_columns', 12)
pd.options.mode.chained_assignment = None

############################################################### Clean kaggle Set #######################################

kaggle_df = pd.read_csv('Hotel_Reviews.csv')

kaggle_df = kaggle_df[
    (kaggle_df['Review_Total_Negative_Word_Counts'] >= 5) & (kaggle_df['Review_Total_Positive_Word_Counts'] >= 5)]
kaggle_df = kaggle_df[
    ['Hotel_Name', 'Reviewer_Nationality', 'Negative_Review', 'Review_Total_Negative_Word_Counts', 'Positive_Review',
     'Review_Total_Positive_Word_Counts', 'Positive_Review', 'Review_Total_Positive_Word_Counts', 'Reviewer_Score']]
kaggle_df['Status'] = ''
kaggle_df['Word_Count'] = ''
kaggle_df['Review'] = ''


def extract_positive_reviews(df):
    df_pos = df.copy()
    df_pos['Review'] = df_pos['Positive_Review']
    df_pos['Word_Count'] = df_pos['Review_Total_Positive_Word_Counts']
    df_pos.Status = 1
    del df_pos['Negative_Review']
    del df_pos['Review_Total_Negative_Word_Counts']
    del df_pos['Positive_Review']
    del df_pos['Review_Total_Positive_Word_Counts']
    return df_pos


def extract_negative_reviews(df):
    df_neg = df.copy()
    df_neg['Review'] = df_neg['Negative_Review']
    df_neg['Word_Count'] = df_neg['Review_Total_Negative_Word_Counts']
    df_neg.Status = 0
    del df_neg['Negative_Review']
    del df_neg['Review_Total_Negative_Word_Counts']
    del df_neg['Positive_Review']
    del df_neg['Review_Total_Positive_Word_Counts']
    return df_neg


df_posi = extract_positive_reviews(kaggle_df)
df_nega = extract_negative_reviews(kaggle_df)
df_combined = df_posi.append(df_nega)
print('KG :', df_combined.columns)
# repo.save_dataframe(df_combined,"kaggle")

############################################################### Clean Tripadvisor Set ##################################

def clean_trip_advisorset():
    tripadvisor_df = pd.read_csv('tripadvisor.csv')
    tripadvisor_df["Reviewer_Score"] = (tripadvisor_df["Reviewer_Score"] / 10) * 2
    tripadvisor_df["Reviewer_Nationality"] = ''
    tripadvisor_df['Word_Count'] = ''
    tripadvisor_df["Word_Count"] = tripadvisor_df["Review"].str.count(' ') + 1
    tripadvisor_df['Review'] = tripadvisor_df['Review_Title'] + ' ' + tripadvisor_df['Review']
    tripadvisor_df['Status'] = ''
    tripadvisor_df.Status[tripadvisor_df['Reviewer_Score'] >= 6] = 1
    tripadvisor_df.Status[tripadvisor_df['Reviewer_Score'] < 6] = 0
    del tripadvisor_df['Review_Title']
    del tripadvisor_df['date']
    return tripadvisor_df


trip_advisor_cleaned = clean_trip_advisorset()
df_combined = df_combined.append(trip_advisor_cleaned)

print('TA :', trip_advisor_cleaned.columns)

# print(kaggle_df.columns)

############################################################### Clean booking.com Set ##################################

def clean_bookingset():
    booking = pd.read_csv('booking.csv')
    booking['review_title'] = booking['review_title'].str.replace('\n', '')
    booking['Hotel_Name'] = booking['Hotel_Name'].str.replace('\n', '')
    booking['date'] = booking['date'].str.replace('\n', '')
    booking['Status'] = ''
    booking['Review'] = ''
    booking['Word_Count'] = ''
    booking['Reviewer_Nationality'] = ''
    booking = booking.dropna()


    pos = extract_pos_booking(booking)
    neg = extract_neg_booking(booking)
    booking = pos.append(neg)
    booking['Review'] = booking['review_title'] + ' ' + booking['Review']
    booking["Word_Count"] = booking["Review"].str.count(' ') + 1
    booking = booking[booking['Word_Count'] >= 5]

    del booking['review_title']
    del booking['review_negative']
    del booking['review_positive']
    del booking['date']

    return booking


def extract_pos_booking(df):
    pos = df.copy()
    pos['Review'] = pos['review_positive']
    pos['Status'] = 1

    return pos

def extract_neg_booking(df):
    neg = df.copy()
    neg['Review'] = neg['review_negative']
    neg['Status'] = 0

    return neg


df_combined = df_combined.append(clean_bookingset())


# def preprocess_reviews(reviews):
#     REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
#     REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
#     NO_SPACE = ""
#     SPACE = " "
#     reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
#     reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
#
#     return reviews
#
# df_combined = preprocess_reviews(df_combined)

repo.save_dataframe(df_combined,"kaggle_clean")
print(df_combined.head())