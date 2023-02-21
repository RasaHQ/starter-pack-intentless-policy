.PHONY:help install train actions run test-e2e

help: ## Display this help message.
	@echo 'Recipes:'
	@echo
	@grep ': ##' Makefile | grep -v grep | column -t -s '##'
	@echo

install: ## Install package dependencies
	poetry install

train:  ## Train a new model
	poetry run rasa train

actions: ## Run the action server for carbon bot
	poetry run rasa run actions

run: ## Run the bot
	poetry run rasa run --enable-api --debug

test-e2e: ## run end-to-end story tests
	poetry run rasa test e2e
