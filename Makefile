# Sync the testing branch
sync-testing:
	git checkout testing
	git pull origin testing
	git checkout main
	git pull origin main
	git merge testing

# Sync the main branch
sync-main:
	git checkout main
	git pull origin main

# Publish changes to the main branch
publish:
	git push origin main

# Default target
all: publish 