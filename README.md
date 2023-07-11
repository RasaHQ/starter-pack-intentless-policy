# Intentless Policy

This repository contains a starter pack with a bot that uses the
`IntentlessPolicy`. It's a good starting point for trying out
the policy and for extending it.

The new intentless policy leverages large language models (LLMs) to
complement existing rasa components

Please see the [documentation on the Intentless Policy](https://rasa.com/docs/rasa/next/llms/llm-intentless/).

## Beta State Notice 🚨

The `IntentlessPolicy` is a Rasa Pro **beta feature**. The current version of
the policy is a prototype that we're releasing to gather feedback. Its use
should be limited to development and experimentation. We are iterating on the
model regularly, so expect model predictions to also change for the duration of the beta.

The beta allows you to try out the concept and to anticipate and influence
our further developments of this feature.

## Demo

[Webinar demo](https://hubs.ly/Q01CLhyG0) showing that this policy can already handle
some advanced linguistic phenomena out of the box.

The examples in the webinar recording are also part of the end-to-end
tests defined in this repo (`tests/e2e_test_stories.yml`).

## Installing this Example Project

The starter pack in this repository is ready to go after a few short steps:

- Install the dependencies using `poetry install`
- set-up the necessary environment variables, e.g. by putting them into a `.env` file:

  ```bash
  RASA_PRO_LICENSE=eyJhbGciOiJSU...
  RASA_PRO_BETA_INTENTLESS=true
  OPENAI_API_KEY=sk-...
  ```

  Please do not use any quotation for the values otherwise the makefile will
  not be able to read the values correctly.

- activate the poetry environment with `poetry shell`

You can use the commands in the makefile, to train

```bash
make train
```

and run the bot:

```bash
make run
```

## Generating End-to-End stories from existing training data

In this starter pack we provide a script that combines existing NLU data and stories
to create end-to-end stories. You can use this script to compare different
configurations and combinations of policies. For example, you can split your
existing data, create more test cases and compare the performance with and without the
intentless policy:

First, split your NLU data into train and test sets:

```bash
rasa data split nlu -u data/nlu.yml --training-fraction 0.5
```

Then run End-to-End test creation script from this starter pack. This script combines
your NLU test data with your bot's stories:

```bash
python scripts/create_test_cases.py -u train_test_split/test_data.yml -s 'data/core/*yml'
```

Replacing the `-s` argument with the path to your stories file or a glob to match multiple filenames.

Inspect the `generated_test_cases.yml` to check that these test cases make sense.

Re-train your model- ensuring you only use the **training** data from your split for NLU training.

Run your test cases:

```bash
rasa test e2e -f generated_test_cases.yml
```

You can then try different policies, parameters, etc. in your `config.yml` to compare test performance.

## Disclaimer

This software release, including the Intentless Policy feature, is beta software.
It’s provided to you only for trial and evaluation, “as is”. You cannot use this beta software release
as part of any production environment. Beta software releases are not intended for processing sensitive
or personal data. There may be bugs or errors. We may never commercialize some beta software.
We disclaim all liabilities, warranties, representations, or covenants related to this beta release.

Your use of the Intentless Policy feature and any other software or material included in this release
is subject to the [Beta Software Terms](https://rasa.com/beta-terms/).

Please make sure you read these terms and conditions prior to using this beta release.
