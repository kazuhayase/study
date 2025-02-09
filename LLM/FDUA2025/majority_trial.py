import os
import pandas as pd
from collections import Counter
import zipfile
from tqdm import tqdm

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_next_trial_number(base_output_dir):
    existing_dirs = [d for d in os.listdir(base_output_dir) if os.path.isdir(os.path.join(base_output_dir, d))]
    existing_numbers = [int(d) for d in existing_dirs if d.isdigit()]
    if existing_numbers:
        return max(existing_numbers) + 1
    else:
        return 1

def run_trials_and_save_results(num_trials, base_output_dir):
    trial_dir = os.path.join(base_output_dir, f'trial')
    ensure_directory_exists(trial_dir)
    next_trial_number = get_next_trial_number(trial_dir)
    
    for i in tqdm(range(num_trials), desc="Running trials"):
        trial_number = next_trial_number + i
        output_dir = os.path.join(base_output_dir, f'trial/{trial_number}/submit')
        ensure_directory_exists(output_dir)
        
        output_file = os.path.join(output_dir, 'predictions.csv')
        os.system(f'python answer_semistructured_store.py > {output_file}')
        print(f'Trial {trial_number} completed and saved to {output_file}')

def majority_vote(*rows):
    filtered_rows = [
        [elem for elem in row if not (isinstance(elem, str) and elem.startswith("わからない"))]
        for row in rows
    ]
    return [Counter(row).most_common(1)[0][0] if row else "わからない" for row in zip(*filtered_rows)]

def filter_unknowns(row):
    return ["わからない" if all(isinstance(element, str) and element.startswith("わからない") for element in row) else element for element in row]

def combine_results(base_output_dir, final_output_file):
    trial_dir = os.path.join(base_output_dir, f'trial')
    ensure_directory_exists(trial_dir)
    trial_dirs = [os.path.join(trial_dir, d) for d in os.listdir(trial_dir) if os.path.isdir(os.path.join(trial_dir, d))]
    dataframes = []
    
    for trial_dir in trial_dirs:
        output_file = os.path.join(trial_dir, 'submit', 'predictions.csv')
        if os.path.exists(output_file):
            #print(f'output_file: {output_file}')
            df = pd.read_csv(output_file, header=None)
            dataframes.append(df)

    if not dataframes:
        print("No predictions found.")
        return
    
    #print(f'#dataframes = {len(dataframes)}')

    rows_list = [df.values.tolist() for df in dataframes]
    #print(f'rows_list: {rows_list}')

    final_rows = [majority_vote(*rows) for rows in tqdm(zip(*rows_list), desc="Combining results", total=len(rows_list[0]))]
    #final_df = pd.DataFrame(final_rows, columns=dataframes[0].columns)
#    print(f'Final rows: {final_rows}')

    # フィルタリングを直接適用しない
    filtered_final_rows = [filter_unknowns(row) for row in final_rows]
    print(f'Filtered Final rows: {filtered_final_rows}')

    # ヘッダ行を除き、インデックスを0から始まる整数に
    ensure_directory_exists(os.path.dirname(final_output_file))
    with open(final_output_file, 'w', newline='') as f:
        for i, row in enumerate(filtered_final_rows):
            # ネストされたリストをアンラップ
            if len(row) >= 2:
                f.write(f'{i},"{row[1]}"\n')
            else:
                #print(f"Skipping row {i} with insufficient elements: {row}")
                f.write(f'{i},"わからない"\n')
                      
    print(f'Final results saved to {final_output_file}')

def zip_results(submit_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(submit_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(submit_dir))
                zipf.write(file_path, arcname)
    print(f'Results zipped to {zip_file_path}')

from read_conf import get_file_directry_conf
fd_conf = get_file_directry_conf()
# 試行の数とベースディレクトリを指定
num_trials = fd_conf['num_trials']
base_output_dir = fd_conf['base_output_dir']
run_trials_and_save_results(num_trials, base_output_dir)

# 最終結果のファイル名を指定
submit_dir = os.path.join(base_output_dir, 'submit')
final_output_file = os.path.join(submit_dir, 'predictions.csv')
combine_results(base_output_dir, final_output_file)

# ZIPファイルのパスを指定
zip_file_path = './submit.zip'
zip_results(submit_dir, zip_file_path)
