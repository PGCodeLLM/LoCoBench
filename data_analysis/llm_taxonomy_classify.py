import json
import tqdm
import re
import multiprocessing as mp

from prompts import TAXONOMY_PROMPT
from llm import llm_request

ROOT_DIR = "/shared_workspace_mfs/kirill/code_architect/LoCoBench/data_analysis"
SOURCE_QUESTIONS_FNAME = "arch_understanding_questions.jsonl"
OUTPUT_FNAME = "arch_understanding_questions_taxonomy_classified.jsonl"


# builds the system prompt
sys_prompt_template = """Please categorize the following software engineering question according to the provided taxonomy. The question is made up of a title, description, and relevant context files. When replying, select the most appropriate one or more top-level taxonomy categories (the ones marked by ###), as well as one or more sub-level categories (marked by * in the taxonomy). Use <top_level></top_level> tags to encompass the top-level categories (separated by a ,), and <sub_level></sub_level> for the sub-level categories (separated by a ,). Make sure to always follow this format exactly, and reply with the name of the category and not just the numbers!

<taxonomy>
{taxonomy_prompt}
</taxonomy>"""

sys_prompt = sys_prompt_template.format(taxonomy_prompt=TAXONOMY_PROMPT.strip())

# user prompt template
usr_prompt_template = """
<task_title>
{title}
</task_title>

<description>
{description}
</description>

<context_files>
{context_files}
</context_files>"""

# parallel vars
concurrency = 15
MUTEX = mp.Lock()


def main():
    """
    LLM-based categorization of samples into taxonomy; batched parallel with ID-based recovery
    """

    print(f"Source data file: {ROOT_DIR}/{SOURCE_QUESTIONS_FNAME}")
    print(f"Output data file: {ROOT_DIR}/{OUTPUT_FNAME}")

    # import raw data
    with open(f"{ROOT_DIR}/{SOURCE_QUESTIONS_FNAME}", 'r', encoding='utf-8') as fin, open(f"{ROOT_DIR}/{OUTPUT_FNAME}", 'r', encoding='utf-8') as fout:
        raw_data = [json.loads(line.strip()) for line in fin]
        print(f"Total dataset size: {len(raw_data)}")

        # crash recovery: check for completed IDs, and skip
        completed_ids = [json.loads(line.strip())["id"] for line in fout]
        raw_data = [data for data in raw_data if data["id"] not in completed_ids]
        print(f"Remaining samples to process: {len(raw_data)}")

    # async parallel processing of all samples with a recovery mechanism based on 'id'
    with open(f"{ROOT_DIR}/{OUTPUT_FNAME}", 'a', encoding='utf-8') as fout:
        
        # parallel processing
        with mp.Pool(processes=concurrency) as pool:
            for single_result in tqdm.tqdm(pool.imap_unordered(process_single_sample, raw_data, chunksize=concurrency),
                                           total=len(raw_data)):
                
                # save to jsonl (mutex protected just in case)
                with MUTEX:
                    if single_result:
                        fout.write(json.dumps(single_result) + "\n")
    print('Done!')


def process_single_sample(data: dict) -> dict:
    """
    Process single sample
    """
    usr_prompt = usr_prompt_template.format(title=data['title'],
                                            description=data['description'],
                                            context_files=",\n".join(data['context_files']))

    # if LLM request part fails, just skip this sample and return, can be re-run later
    try:
        raw_response = llm_request(sys_prompt, usr_prompt, "deepseek/deepseek-v3.2")
        resp, reason = raw_response['content'], raw_response['reasoning']
    except Exception:
        return None
    
    # extract response and tags
    top_matched = re.search(r"<top_level>(.*?)</top_level", resp)
    sub_matched = re.search(r"<sub_level>(.*?)</sub_level", resp)

    # save to data dict
    data['tax_top_level'] = top_matched.group(1) if top_matched else None
    data['tax_sub_level'] = sub_matched.group(1) if sub_matched else None
    data['tax_resp'] = resp
    data['tax_reason'] = reason

    return data


if __name__ == "__main__":
    main()