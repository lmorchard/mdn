# Usage: ./tag_prod_release.sh 0.9.2
git checkout master
git pull origin master && \
git checkout prod && \
git reset --hard origin/master && \
git push --force origin HEAD && \
git tag -m "version ${1} as pushed to prod" ${1} HEAD && \
git push --tags
git tag
