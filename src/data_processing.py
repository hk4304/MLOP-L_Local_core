#data_processing.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import yaml
import os

def preprocess_data(config_path):
    """
    Loads, preprocesses, and splits the dataset.
    - Handles categorical features using one-hot encoding.
    - Splits data into training and testing sets.
    - Saves the processed datasets.
    """
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Paths
    raw_data_path = config['data_processing']['raw_data_path']
    processed_dir = config['data_processing']['processed_dir']
    train_path = os.path.join(processed_dir, 'train.csv')
    test_path = os.path.join(processed_dir, 'test.csv')
    os.makedirs(processed_dir, exist_ok=True)

    # Load data
    df = pd.read_csv(raw_data_path)

    # Feature Engineering (simple example)
    df['registration_ratio'] = df['actual_attendance'] / (df['registered_volunteers'] + 1e-6)

    # Define features and target
    target = config['data_processing']['target_column']
    features = [col for col in df.columns if col not in [target, 'event_id', 'registration_ratio']]
    
    X = df[features]
    y = df[target]

    # One-Hot Encode categorical features
    categorical_features = X.select_dtypes(include=['object', 'category']).columns
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_cols = pd.DataFrame(encoder.fit_transform(X[categorical_features]), 
                                index=X.index, 
                                columns=encoder.get_feature_names_out(categorical_features))
    
    X = X.drop(columns=categorical_features)
    X = pd.concat([X, encoded_cols], axis=1)

    # Split data
    test_size = config['data_processing']['test_size']
    random_state = config['base']['random_state']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Save processed data
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Data processed and saved to {processed_dir}")

if __name__ == '__main__':
    preprocess_data('params.yaml')
