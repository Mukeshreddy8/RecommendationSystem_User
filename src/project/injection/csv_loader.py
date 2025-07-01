import pandas as pd

def load_users_data(path:str)->pd.DataFrame:
    """ Loading the users data from csv file"""
    path="/Users/mukeshreddy/Desktop/RecommendationSytem_User/dummy_users_400_full_profile.csv"
    df=pd.read_csv(path)
    return df


if __name__ == "__main__":
    csv_path = "/Users/mukeshreddy/Desktop/RecommendationSytem_User/dummy_users_400_full_profile.csv"
    df = load_users_data(csv_path)
    print(df.head())

