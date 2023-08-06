import os
import sys
import logging

from . import config
from .helpers import runSubprocess

class S3:
    def __init__(self):
        self.bucket = os.path.join(config.s3_bucket, '')
        if not runSubprocess(['s3cmd', 'ls', self.bucket], failOnError=False) and not config.dry_run:
            logging.error('s3cmd is not installed or configured properly')
            sys.exit(1)
        logging.info('Using S3 bucket: %s' % self.bucket)

    def pull_rpms(self):
        command = ['s3cmd', 'sync', os.path.join(self.bucket, ''), os.path.join(config.target_rpm_dir, '')]
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)

    def push_rpms(self):
        command = ['s3cmd', 'sync', os.path.join(config.target_rpm_dir, ''), self.bucket]
        if config.dry_run:
            print(*command)
        else:
            runSubprocess(command)
