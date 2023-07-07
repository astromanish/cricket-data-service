import errno
import os
import os.path
import re
import shutil
import sys
from datetime import date, timedelta
from stat import S_ISDIR, S_ISREG
import pysftp

from common.utils.helper import getEnvVariables
from DataIngestion.utils.helper import readJsFile


def create_directory(path):
    try:
        os.makedirs(path)
        os.chmod(path, 0o777)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

def download_squad_file(sftp, remotedir, localdir, squad_prefix, preserve_mtime=False):
    for entry in sftp.listdir(remotedir):
        remotepath = remotedir + "/" + entry
        localpath = os.path.join(localdir, entry)
        mode = sftp.stat(remotepath).st_mode
        if S_ISDIR(mode):
            download_squad_file(sftp, remotepath, localdir, squad_prefix, preserve_mtime)
        elif S_ISREG(mode) and entry.split('-')[0] == squad_prefix:
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

def download_match_file(sftp, remotedir, localdir, ipl_2023, preserve_mtime=False):
    squad_processed = False
    for entry in sftp.listdir(remotedir):
        if entry == "competition.js":
            continue
        if not squad_processed:
            download_squad_file(
                sftp,
                ipl_2023 + '/' + "IPL2023SQUAD",
                localdir,
                entry.split('-')[0],
                preserve_mtime=False
            )
            squad_processed = True
        remotepath = remotedir + "/" + entry
        localpath = os.path.join(localdir, entry)
        mode = sftp.stat(remotepath).st_mode
        if S_ISDIR(mode):
            try:
                os.mkdir(localpath)
            except OSError:
                pass
            download_match_file(sftp, remotepath, localpath, preserve_mtime)
        elif S_ISREG(mode):
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

def download_files(path, destination):
    create_directory(destination + "/IPL/IPL 2023")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(
        host=getEnvVariables("FTP_HOST"),
        username=getEnvVariables("FTP_USERNAME"),
        password=getEnvVariables("FTP_PASSWORD"),
        cnopts=cnopts,
        port=getEnvVariables("FTP_PORT")
    )
    local_directory = destination + path
    try:
        os.chdir(destination)
        create_directory(local_directory)
    except OSError:
        pass

    ipl_2023 = getEnvVariables("FTP_REMOTE_PATH") + "/IPL2023"
    yesterday = (date.today() - timedelta(days=1)).strftime("%d%m%Y")
    filelist = [file for file in sftp.listdir(ipl_2023) if yesterday == get_numbers_from_filename(file)]
    for file in filelist:
        create_directory(local_directory + "/" + file)
        download_match_file(sftp, ipl_2023 + '/' + file, local_directory + "/" + file, ipl_2023, preserve_mtime=False)

def move_files(basePath, dst_path, squad_path):
    logger.info("Moving Files")
    try:
        for basefold in os.listdir(basePath):
            if basefold != ".DS_Store":
                for filename in os.listdir(basePath + '/' + basefold):
                    if filename not in [".DS_Store", "competition.js"]:
                        logger.info(f"filename --> {filename}")
                        file_type = filename.split('-')[1].split('.')[0]
                        if file_type in ['matchsummary', 'Innings2', 'Innings1']:
                            shutil.move(basePath + '/' + basefold + '/' + filename, os.path.join(dst_path, filename))
                            logger.info(f"File Moved: {os.path.join(dst_path, filename)}")
                        elif file_type in ['squad']:
                            if os.path.exists(squad_path + basefold):
                                shutil.rmtree(squad_path + basefold)
                            squad_match_dir = squad_path + basefold
                            create_directory(squad_match_dir)
                            shutil.move(basePath + '/' + basefold + '/' + filename, os.path.join(squad_match_dir, filename))
                            logger.info(f"File Moved: {os.path.join(squad_match_dir, filename)}")
                        elif file_type in ['matchSchedule']:
                            if os.path.exists(os.path.join(dst_path, filename)):
                                src_file_len = len(readJsFile(os.path.join(dst_path, filename))['Result'])
                                current_file_len = len(readJsFile(os.path.join(basePath + '/' + basefold, filename))['Result'])
                                if current_file_len > src_file_len:
                                    shutil.move(basePath + '/' + basefold + '/' + filename, os.path.join(dst_path, filename))
                                    logger.info(f"File Moved: {os.path.join(dst_path, filename)}")
                                else:
                                    pass
                            else:
                                shutil.move(basePath + '/' + basefold + '/' + filename, os.path.join(dst_path, filename))
    except Exception as err:
        logger.error(err)
