#!/bin/bash
set -e
function docker-run {
   docker-compose -f docker/docker-compose.local.yml run --rm web $@
} 

echo -e "\n>>> Resetting database"
docker-run ./manage.py reset_db --close-sessions --noinput

echo -e "\n>>> Running migrations"
docker-run ./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
docker-run ./manage.py createsuperuser \
   --username admin \
   --email admin@example.com \
   --noinput

echo -e "\n>>> Setting superuser 'admin' password to '12345'"
SHELL_CMD="\
u=User.objects.get(username='admin');\
u.set_password('12345');\
u.first_name='Admin';\
u.last_name='McGee';\
u.save();\
"
docker-run ./manage.py shell_plus -c "$SHELL_CMD"


echo -e "\n>>> Downloading CLIP model"
docker-run ./manage.py download_clip

echo -e "\n>>> Downloading and encoding 128 test images"
docker-run ./manage.py setup_images 128

echo -e "\n>>> Setup finished."
