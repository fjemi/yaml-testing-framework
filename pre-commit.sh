#!/bin/bash

# https://stackoverflow.com/questions/75725831/pre-commit-missing-required-key-name-will-local-hook
# https://www.andrewcbancroft.com/blog/musings/make-bash-script-executable/
# https://stackoverflow.com/questions/45495155/how-to-exit-a-git-hook-script-if-a-git-command-fails
# https://askubuntu.com/questions/674333/how-to-pass-an-array-as-function-argument

hook_entrypoints=(
	# Formatting and linting
	"trunk check"
	"trunk fmt"
	"pipenv run pytest --project-directory=${PWD} --cov=${PWD} --cov-report=html"
)

function execute_hook_entrypoints() {
	local entrypoints=("$@")
	for i in "${entrypoints[@]}"; do
		if ! eval $"${entrypoint} ${i}"; then
			exit 1
		fi
	done
}

execute_hook_entrypoints "${hook_entrypoints[@]}"
