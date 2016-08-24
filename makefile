# make deploy web m="<message explaining change>""
deploy web:
	git add .
	git commit -m "$(m)"
	git push
	make update

# Pushes the web/app folder to gh-pages to update the staging webpage.
update:
	rm -rf web/app
	cd web && \
	gulp preview
	git push origin `git subtree split --prefix web/app master`:gh-pages --force