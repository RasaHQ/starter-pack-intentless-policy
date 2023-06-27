.PHONY:help install train actions run test-e2e

-include .env

help: ## Display this help message.
	@echo 'Recipes:'
	@echo
	@grep ': ##' Makefile | grep -v grep | column -t -s '##'
	@echo

.EXPORT_ALL_VARIABLES:

install: ## Install package dependencies
	poetry install

train: ## Train a new model
	poetry run rasa train

actions: .EXPORT_ALL_VARIABLES ## Run the action server for carbon bot
	poetry run rasa run actions

run: .EXPORT_ALL_VARIABLES ## Run the bot
	poetry run rasa run --enable-api --debug

test-e2e: .EXPORT_ALL_VARIABLES ## run end-to-end story tests
	poetry run rasa test e2e
