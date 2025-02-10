import os
import pandas as pd
from collections import Counter
import zipfile
from read_conf import setup_logging, get_file_directry_conf

def run_trials_and_save_results(num_trials, base_output_dir):
    for i in range(num_trials):
        trial_number = i + 1
        output_dir = os.path.join(base_output_dir, f'trial/{trial_number}/submit')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_file = os.path.join(output_dir, 'predictions.csv')
        os.system(f'python answer_semistructured_store.py > {output_file}')
        print(f'Trial {trial_number} completed and saved to {output_file}')

def majority_vote(*rows):
    return [Counter(row).most_common(1)[0][0] for row in zip(*rows)]

def filter_unknowns(row):
    return ["わからない" if all(element == "わからない" for element in row) else element for element in row]

def combine_results(base_output_dir, num_trials, final_output_file):
    dataframes = []
    for i in range(num_trials):
        trial_number = i + 1
        output_file = os.path.join(base_output_dir, f'trial/{trial_number}/submit/predictions.csv')
        df = pd.read_csv(output_file)
        dataframes.append(df)

    rows_list = [df.values.tolist() for df in dataframes]
    final_rows = [majority_vote(*rows) for rows in zip(*rows_list)]
    final_df = pd.DataFrame(final_rows, columns=dataframes[0].columns)

    final_df = final_df.apply(filter_unknowns, axis=1)
    final_df.to_csv(final_output_file, index=False)
    print(f'Final results saved to {final_output_file}')

def zip_results(final_output_file, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(final_output_file, os.path.basename(final_output_file))
    print(f'Results zipped to {zip_file_path}')

fd_conf = get_file_directry_conf()
# 試行の数とベースディレクトリを指定
num_trials = fd_conf['num_trials']
base_output_dir = fd_conf['base_output_dir']
run_trials_and_save_results(num_trials, base_output_dir)

# 最終結果のファイル名を指定
final_output_file = os.path.join(base_output_dir, 'submit/predictions.csv')
combine_results(base_output_dir, num_trials, final_output_file)

# ZIPファイルのパスを指定
zip_file_path = os.path.join(base_output_dir, 'submit/predictions.zip')
zip_results(final_output_file, zip_file_path)
