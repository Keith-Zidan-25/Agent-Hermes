import pandas as pd
import json

def calculate_and_rank_issues(classified_data_json: str, weights_json: str) -> str:
    """
    Calculates the absolute frequency count and a composite Priority Score for each 
    unique local issue type, then ranks them for final prioritization.

    This tool groups all classified reports, aggregates their scores, and applies 
    policy-driven weights to determine the final urgency ranking.

    Args:
        classified_data_json (str): A JSON string containing a list of dictionaries 
                                    from the Classifier Agent. Must include 'issue_Type' 
                                    and 'severity_score'.
                                    Example: [{'issue_Type': 'Pothole', 'severity_score': -0.4, 'frequency_count': 500}, ...]
        weights_json (str): A JSON string defining the policy weights for each metric.
                            Weights must sum to a constant (e.g., 1.0 or 100) and must 
                            include keys for: 'Severity_Weight' and 'Frequency_Weight'.
                            Example: {"Severity_Weight": 0.65, "Frequency_Weight": 0.35}

    Returns:
        str: A JSON-formatted string containing the ranked list of unique issues, 
             including the new 'Total_Frequency' and 'Priority_Score', sorted 
             in descending order of Priority_Score.
    """
    
    df = pd.DataFrame(json.loads(classified_data_json))
    weights = json.loads(weights_json)
    
    frequency_df = df.groupby('issue_Type').size().reset_index(name='Total_Frequency')
    severity_agg_df = df.groupby('issue_Type')['severity_score'].mean().reset_index(name='Average_Severity_Score')
    final_df = pd.merge(frequency_df, severity_agg_df, on='issue_Type')
    
    max_freq = final_df['Total_Frequency'].max()
    final_df['Norm_Frequency'] = final_df['Total_Frequency'] / max_freq

    final_df['Crisis_Factor'] = 1 - ((final_df['Average_Severity_Score'] + 1) / 2)
    final_df['Priority_Score'] = (
        final_df['Crisis_Factor'] * weights['Severity_Weight'] +
        final_df['Norm_Frequency'] * weights['Frequency_Weight']
    )
    
    df_ranked = final_df.sort_values(by='Priority_Score', ascending=False)
    return df_ranked[['issue_Type', 'Total_Frequency', 'Average_Severity_Score', 'Priority_Score']].to_json(orient='records')