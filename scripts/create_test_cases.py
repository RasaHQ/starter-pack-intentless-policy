import random
import glob
import argparse

from rasa.shared.utils.io import read_yaml_file, write_yaml
from rasa.shared.nlu.training_data.loading import load_data

### setup
random.seed(666)


def example_for_intent(intent, nlu_data):
    if nlu_data.number_of_examples_per_intent.get(intent):
        ex = [
            e.get("text") for e in nlu_data.intent_examples if e.get("intent") == intent
        ]
        return random.choice(ex)
    else:
        return f"/{intent}"


def test_case_from_story(story, nlu_data):
    e2e_test_case = {"test_case": story["story"], "steps": []}

    for step in story["steps"]:
        e2e_step = {}
        if "intent" in step:
            e2e_step["user"] = example_for_intent(step["intent"], nlu_test_data)
        elif "action" in step and step["action"].startswith("utter"):
            e2e_step["utter"] = step["action"]
        if e2e_step:
            e2e_test_case["steps"].append(e2e_step)
    return e2e_test_case


parser = argparse.ArgumentParser(description="Create e2e test cases.")
parser.add_argument(
    "-u",
    "--nlu-test-data",
    type=str,
    required=True,
    help="File or folder containing NLU test data.",
)
parser.add_argument(
    "-s",
    "--stories",
    type=str,
    required=True,
    help="Glob expression for finding stories, e.g. 'data/stories/.*yml'.",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="generated_test_cases.yml",
    help="File to write test cases to.",
)
parser.add_argument(
    "-N",
    "--max-cases",
    type=int,
    default=100,
    help="maximum number of test cases to generate. default 100",
)

args = parser.parse_args()


### Read NLU test data
nlu_test_data = load_data(args.nlu_test_data)

### Load bot training stories
stories = []
for story_file in glob.glob(args.stories):
    story_data = read_yaml_file(story_file)
    stories.extend(story_data["stories"])


### Create test cases using NLU test data
e2e_test_cases = {"test_cases": []}
for story in stories:
    if len(e2e_test_cases["test_cases"]) == args.max_cases:
        break
    e2e_test_cases["test_cases"].append(test_case_from_story(story, nlu_test_data))


write_yaml(e2e_test_cases, args.output)
