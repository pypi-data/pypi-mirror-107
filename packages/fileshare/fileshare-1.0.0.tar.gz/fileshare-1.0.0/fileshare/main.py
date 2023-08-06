import os
import uuid
import volapi
import pathlib
import zipfile
import argparse
import requests
import collections

from tqdm import tqdm

def uuid4(): return str(uuid.uuid4())


def upload() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='The file (or files) to upload')
    parser.add_argument('-z', '--zip', help='Zip files before uploading', action='store_true')
    parser.add_argument('-r', '--room', help='Existing room name to add files to; automatically generated if not provided')

    args = parser.parse_args()

    if args.zip:
        zipfile_name = f'{uuid4()}.zip'

        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except ImportError:
            compression = zipfile.ZIP_STORED

        zfile = zipfile.ZipFile(zipfile_name, 'w', compression=compression)

        for file in args.files:
            zfile.write(file)

        zfile.close()

        print(f'Compressed {len(args.files)} files')

        args.files = [zipfile_name]

    try:
        with volapi.Room(args.room, subscribe=False) as room:
            for file in tqdm(args.files):
                room.upload_file(file)
                tqdm.write(f'✅  {file}')

            print(f'Uploaded {len(args.files)} {"files" if len(args.files) > 1 else "file"} to https://volafile.org/r/{room.name}')
    except RuntimeError as e:
        print(e)

    if args.zip:
        os.remove(zipfile_name)


def download() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('room', help='Room to download files from')
    parser.add_argument('-d', '--destination', help='Destination directory for files; will be created if it does not exist', default='./')

    args = parser.parse_args()

    out_directory = args.destination + '/' if args.destination[-1] != '/' else args.destination

    pathlib.Path(out_directory).mkdir(parents=True, exist_ok=True)

    try:
        with volapi.Room(args.room, subscribe=False) as room:
            file_urls = collections.OrderedDict((x.name, x.url) for x in room.files).items()

            for f_name, f_url in tqdm(file_urls):
                with open(f'{out_directory}{f_name}', 'wb') as outf:
                    outf.write(requests.get(f_url).content)
                    tqdm.write(f'✅  {f_name}')

            if len(file_urls) > 0:
                print(f'Downloaded {len(file_urls)} {"files" if len(file_urls) > 1 else "file"} to {out_directory}')
    except RuntimeError as e:
        print(e)
