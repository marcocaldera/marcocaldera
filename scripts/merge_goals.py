# import os
import json
from pathlib import Path

def merge_goals():
    goals_dir = Path('data/goals')
    merged_goals = []

    # Iterate through all subdirectories in the goals directory
    for year_dir in goals_dir.iterdir():
        if year_dir.is_dir():
            # Check for a goals.json file in each year directory
            goals_file = year_dir / 'goals.json'
            if goals_file.exists():
                with open(goals_file, 'r') as f:
                    try:
                        year_goals = json.load(f)
                        if year_goals:  # Check if the file is not empty
                            merged_goals.extend(year_goals)
                    except json.JSONDecodeError:
                        print(f"Warning: {goals_file} is empty or not a valid JSON file.")

    # Sort the merged goals by year and quarter
    merged_goals.sort(key=lambda x: (x['year'], x['quarter']))

    # Write the merged goals to data/goals.json
    output_file = Path('data/goals/goals.json')
    with open(output_file, 'w') as f:
        json.dump(merged_goals, f, indent=2)

if __name__ == '__main__':
    merge_goals()
