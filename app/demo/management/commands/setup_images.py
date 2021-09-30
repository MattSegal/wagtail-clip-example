import os
import hashlib
import concurrent.futures
from io import BytesIO

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.images import ImageFile
from wagtail.images import get_image_model

WagtailImage = get_image_model()


class Command(BaseCommand):
    help = "Download images for the website"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **kwargs):
        assert settings.DEBUG, "NEVER RUN THIS IN PROD!"
        num_images = kwargs["count"]
        WagtailImage.objects.all().delete()
        img_dir = os.path.join(settings.MEDIA_ROOT, "original_images")
        if os.path.exists(img_dir):
            images_fnames = os.listdir(img_dir)
            img_paths = [os.path.join(img_dir, i) for i in images_fnames]
            img_paths = img_paths[:num_images]
        else:
            img_paths = []

        for idx, img_path in enumerate(img_paths):
            count = idx + 1
            recreate_wagtail_image(img_path, count, num_images)

        num_existing = WagtailImage.objects.count()
        num_remaining = num_images - num_existing
        if num_remaining > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                for idx in range(num_remaining):
                    count = num_existing + idx + 1
                    executor.submit(download_wagtail_image, count, num_images)


def recreate_wagtail_image(img_path, count, total):
    print(f"Recreating image from {img_path} {count} / {total}...")
    with open(img_path) as f:
        img_bytes = f.read()
        filename = "{}.jpg".format(hashlib.sha256(img_bytes).hexdigest())
        django_image = ImageFile(BytesIO(img_bytes), name=filename)
        if not WagtailImage.objects.filter(title=filename).exists():
            return WagtailImage.objects.create(title=filename, file=django_image)


def download_wagtail_image(count, total):
    print(f"Downloading image {count} / {total}...")
    while True:
        url = f"https://source.unsplash.com/random/?sig={count}"
        r = requests.get(url, stream=True)
        r.raise_for_status()
        img_bytes = r.content
        filename = "{}.jpg".format(hashlib.sha256(img_bytes).hexdigest())
        django_image = ImageFile(BytesIO(img_bytes), name=filename)
        if not WagtailImage.objects.filter(title=filename).exists():
            return WagtailImage.objects.create(title=filename, file=django_image)
