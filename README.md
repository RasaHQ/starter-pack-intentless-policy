# Intentless Policy

The new intentless policy aims to solve two problems:

- Making it faster to bootstrap a new assistant without first defining a bunch of Rasa primitives.
- Making it possible for Rasa bots to handle conversations where messages [don't fit in intents](https://rasa.com/blog/were-a-step-closer-to-getting-rid-of-intents/).

The `IntentlessPolicy` is a Rasa Pro **beta feature**. The current version of
the policy is a prototype that we're releasing to gather feedback. Its use
should be limited to development and experimentation. We are iterating on the
model regularly, so expect model predictions to also change for the duration of the beta.

The beta allows you to try out the concept and to anticipate and influence
our further developments of this feature.

## Demo

[Webinar demo](https://hubs.ly/Q01CLhyG0)

## Installation of the beta

Ensure that you have the required authentication setup to install Rasa Plus locally
(see [here](https://rasa.com/docs/rasa/installation/rasa-pro/installation/#installing-with-pip)).

Usage of the beta requires a license for Rasa Pro. You can set the license
as an environment variable:

```bash
export RASA_PRO_LICENSE="eyJhbGciOiJSU..."
```

With the license being set, you should be able to run `rasa run`
or `rasa train` as usual.

### Installation (your project)

You can install the beta by updating your Rasa Plus dependency to version
`3.5.0b2`:

- using pip: `pip install rasa-plus==3.5.0b2`
- using poetry: `poetry add rasa-plus==3.5.0b2`

### Installation (starter pack)

This repository contains a starter pack with a bot that uses the
new `IntentlessPolicy`. It's a good starting point for trying out
the policy and for extending it. The starter
pack contains a set of example banking FAQs. Replacing these with
a different set of answers is enough to modify the bot.
You can optionally provide a canonical phrasing of the question corresponding
to each answer in the `metadata` field of each response.

First, setup [Poetry](https://python-poetry.org/docs/#installation)
using `curl -sSL <https://install.python-poetry.org> | python3 -`. It is
recommended use Poetry 1.2.0 and newer.

Then, clone this repo and install the dependencies:

```bash
git clone http://github.com/rasahq/starter-pack-intentless-policy
cd starter-pack-intentless-policy
make install
```

You can see a list of available commands in this starter pack by running `make help`.

The examples in the webinar recording are also part of the end-to-end
tests defined in this repo (`tests/e2e_test_stories.yml`).

## IntentlessPolicy

You can build a bot with the new `IntentlessPolicy` just by adding/editing
the set of responses in the domain file. You can also train the policy using
[end-to-end stories](https://rasa.com/docs/rasa/training-data-format/#end-to-end-training).
Rules and normal (non end-to-end) stories are not used to train this policy.

After adding the policy, do kick the tires on your bot and see how well
it deals with digressions, follow-ups, ambiguous input, etc. Once you've
got a sense of what does and doesn't work out of the box, you can start
extending what your bot can do.

As shown in the webinar linked above, this policy can already handle
some advanced linguistic phenomena out of the box.

### Usage

Add the `IntentlessPolicy` to your `config.yml` file:

```yaml
policies:
  # ... any other policies you have
  - name: rasa_plus.ml.IntentlessPolicy
```

And set `use_nlu_confidence_as_score: True` for any rule-based policies in
your pipeline. Otherwise the rule-based policies will always make predictions
with confidence value 1.0, ignoring any uncertainty stemming from the NLU prediction.

```yaml
- name: MemoizationPolicy
  max_history: 5
  use_nlu_confidence_as_score: True
- name: RulePolicy
  use_nlu_confidence_as_score: True
  core_fallback_threshold: 0.22
```

The policy uses a remote service to train and predict and needs to be
able to make requests to a Rasa hosted ML service. During training, the policy will
send the training data to the remote service. When predicting next actions,
the tracker will be send to the remote service.

After adding the policy to your configuration, you can train your bot
as usual:

```bash
rasa train
```

Once trained, you can test your bot by running the following command:

```bash
rasa shell
```

If a flow you'd like to implement doesn't already work out of the box, you
can add Rasa primitives like you normally would. You can also add additional
e2e training stories to `data/e2e_stories.yml`.

The `IntentlessPolicy` will kick in only when it can't find a matching rule or story.

### Configuration

The `IntentlessPolicy` can be configured with the following parameters:

- `max_history`: The maximum number of turns to take into account
  when predicting the next action. Defaults to `null`, which means that all
  conversation history is taken into account.
- `nlu_abstention_threshold`: The threshold for the NLU prediction confidence.
  Defaults to `0.9`. Above this threshold NLU prediction confidence is considered high.
  Head over to [this section](#how-does-the-intentlesspolicy-work-with-other-rasa-primitives) to see
  how the `IntentlessPolicy` interacts with other Rasa primitives.

The configuration of the `IntentlessPolicy` should be specified in the `config.yml` file.
The following example shows the default configuration:

```yaml
policies:
  # ... any other policies you have
  - name: rasa_plus.ml.IntentlessPolicy
    max_history: null
    nlu_abstention_threshold: 0.9
```

### Can I use this with TED?

There is no reason why you can’t also have TED in your configuration. However,

- TED frequently makes predictions with very high confidence values (~0.99)
  so will often override what the `IntentlessPolicy` is doing.
- TED and the `IntentlessPolicy` are trying to solve similar problems, so your system
  is easier to reason about if you just use one or the other.

### Testing the Policy

As part of the beta, we're also releasing a beta version of
a new End-To-End testing framework. The `rasa test e2e` command allows you to
test your bot end-to-end, i.e. from the user's perspective. You can use it to
test your bot in a variety of ways, including testing the `IntentlessPolicy`.

To use the new testing framework, you need to define a set of test cases in
a test folder, e.g. `tests/e2e_test_stories.yml`. The test cases are defined
in a similar format as stories are, but contain the user's messages and the
bot's responses. Here's an example:

```yaml
test_cases:
  - test_case: transfer charge
    steps:
      - user: how can I send money without getting charged?
      - utter: utter_faq_0
      - user: not zelle. a normal transfer
      - utter: utter_faq_7
```

**Please ensure all your test stories have unique names!**
You can run the tests with `rasa test e2e`.

## Evaluating And Tuning the Intentless Policy

You can compare the performance of your bot with and without the intentless policy
by creating some end-to-end test cases.

First, split your NLU data into train and test sets:

```bash
rasa data split nlu -u data/nlu.yml --training-fraction 0.5
```

Then run the script to create test cases by combining your NLU test data with your bot's stories:

```bash
python scripts/create_test_cases.py -u train_test_split/test_data.yml -s 'data/core/*yml'
```

Replacing the `-s` argument with the path to your stories file or a glob to match multiple filenames.

Inspect the `generated_test_cases.yml` to check these test cases make sense.

Re-train your model- ensuring you only use the **training** data from your split.

Run your test cases:

```bash
rasa test e2e -f generated_test_cases.yml
```

You can then try different policies, parmeters, etc. in your `config.yml` to compare test performance.

## FAQ

### How is data handled?

The policy makes use of an intentless dialogue model which is implemented as a hosted service.

We log requests made to this server so that we can improve the model over time.

### How does the IntentlessPolicy work with other Rasa primitives

The `IntentlessPolicy` is designed to work with other Rasa primitives
like rules, stories, forms, etc. Here are some details about how it interacts with them:

- If there is a high-confidence NLU prediction and a matching story/rule,
  the `RulePolicy` or `MemoizationPolicy` will be used.

- If there is a high-confidence NLU prediction but no matching story/ rule,
  the `IntentlessPolicy` will kick in.

- If the NLU prediction has low confidence, the `IntentlessPolicy` will kick in.

- If the `IntentlessPolicy` prediction has low confidence,
  the `RulePolicy` will trigger fallback based on the `core_fallback_threshold`.

<img width="851" alt="image" src="./img/readme-intentless-policy-other-primitives.png">

## We want to hear from you

At Rasa we’re keen to improve our products and hear from users’ experience. We’d love to hear from you, especially:

- How many use cases did you implement?
- How many intents did you define?
- How many stories did you write?
- How was the success rate of your test stories impacted by the `IntentlessPolicy`?

## Disclaimer

This software release, including the Intentless Policy feature, is beta software.
It’s provided to you only for trial and evaluation, “as is”. You cannot use this beta software release
as part of any production environment. Beta software releases are not intended for processing sensitive
or personal data. There may be bugs or errors. We may never commercialize some beta software.
We disclaim all liabilities, warranties, representations, or covenants related to this beta release.

Your use of the Intentless Policy feature and any other software or material included in this release
is subject to the [Beta Software Terms](https://rasa.com/beta-terms/).

Please make sure you read these terms and conditions prior to using this beta release.
