import json
import tqdm
import re

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

skip_count = 35

# process raw samples one-by-one with the prompt, then save to the output file
with open(f"{ROOT_DIR}/{SOURCE_QUESTIONS_FNAME}", 'r', encoding='utf-8') as fin, open(f"{ROOT_DIR}/{OUTPUT_FNAME}", 'a', encoding='utf-8') as fout:
    for idx,line in tqdm.tqdm(enumerate(fin)):
        
        # resume feature that skips already processed
        if idx <= skip_count:
            continue

        print(f"Processing item {idx}")
        data = json.loads(line.strip())

        usr_prompt = usr_prompt_template.format(title=data['title'],
                                                description=data['description'],
                                                context_files=",\n".join(data['context_files']))


        raw_response = llm_request(sys_prompt, usr_prompt, "deepseek/deepseek-v3.2")
        resp, reason = raw_response['content'], raw_response['reasoning']
        
        # extract response and tags
        top_matched = re.search(r"<top_level>(.*?)</top_level", resp)
        sub_matched = re.search(r"<sub_level>(.*?)</sub_level", resp)

        # save to data dict
        data['tax_top_level'] = top_matched.group(1) if top_matched else None
        data['tax_sub_level'] = sub_matched.group(1) if sub_matched else None
        data['tax_resp'] = resp
        data['tax_reason'] = reason

        # save to jsonl
        fout.write(json.dumps(data) + "\n")

        # break


