# cheesefactory-sftp/put.py

import logging
from typing import List
from .transfer import CfSftpTransfer

logger = logging.getLogger(__name__)


class CfSftpPut(CfSftpTransfer):
    """GET-related attributes and methods.

    Notes:
        CfSftp --> CfSftpGet ----> CfSftpTransfer --> CfSftpUtilities --> CfSftpConnection
               |-> CfSftpPut ->|
    """
    def __init__(self):
        super().__init__()

    #
    # PUBLIC METHODS
    #

    def put(self, append_local: str = None, append_remote: str = None, local_path: str = None,
            log_checksum: bool = False, preserve_mtime: bool = True, remote_path: str = None,
            remove_source: bool = False) -> str:
        """Upload a single, remote file from the local host to the SFTP server.

        Args:
            append_local: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If no
                          extension exists, then string is appended to end of filename.
            append_remote: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If
                           no extension exists, then string is appended to end of filename.
            local_path: Local/destination path and filename.
            log_checksum: Calculate file SHA256 checksum and log resulting value.
            preserve_mtime: Keep modification time of source file.
            remote_path: Remote/source path and filename.
            remove_source: Remove the remote source file.

        Returns:
            Final destination file path (after any name changes).
        """
        file = self._transfer(
            action='PUT', append_local=append_local, append_remote=append_remote, local_path=local_path,
            log_checksum=log_checksum, preserve_mtime=preserve_mtime, remote_path=remote_path,
            remove_source=remove_source
        )
        return file

    def put_by_glob(self, append_local: str = None, append_remote: str = None, flat_dir: bool = False,
                    glob_filter: str = '*', local_base_dir: str = '.', log_checksum: bool = False,
                    preserve_mtime: bool = True, recursive_search: bool = False, remote_dir: str = '.',
                    remove_source: bool = False) -> List[str]:
        """Create a list of remote files to upload based on glob, then upload.

        Creates a recursive list of files and directories in remote_dir and filters by glob_filter.

        Args:
            append_local: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If no
                          extension exists, then string is appended to end of filename.
            append_remote: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If
                           no extension exists, then string is appended to end of filename.
            flat_dir: Do not recreate directory structure in local_base_dir.
            glob_filter:
            log_checksum: Calculate file SHA256 checksum and log resulting value.
            local_base_dir: Local base directory for downloaded files. See flat_dir.
            preserve_mtime: Keep modification time of source file.
            recursive_search:
            remote_dir:
            remove_source: Remove the remote source file.

        Returns:
            List of final destination file paths (after any name changes).
        """
        files = self._transfer_by_glob(
            action='PUT', append_local=append_local, append_remote=append_remote, base_dir=local_base_dir,
            flat_dir=flat_dir, glob_filter=glob_filter, log_checksum=log_checksum, preserve_mtime=preserve_mtime,
            recursive_search=recursive_search, remove_source=remove_source, source_dir=remote_dir,
        )
        return files

    def put_by_list(self, append_local: str = None, append_remote: str = None, flat_dir: bool = False,
                    log_checksum: bool = False, preserve_mtime: bool = True, local_files: List[str] = None,
                    remote_base_dir: str = '.', remove_source: bool = False) -> List[str]:
        """Upload a list of files from the local host to the SFTP server.

        Args:
            append_local: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If no
                          extension exists, then string is appended to end of filename.
            append_remote: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If
                           no extension exists, then string is appended to end of filename.
            flat_dir: Do not recreate directory structure in local_base_dir.
            log_checksum: Calculate file SHA256 checksum and log resulting value.
            local_files: Local/source path and filename.
            preserve_mtime: Keep modification time of source file.
            remote_base_dir: Local base directory for downloaded files. See flat_dir.
            remove_source: Remove the remote source file.

        Returns:
            List of final destination file paths (after any name changes).
        """
        files = self._transfer_by_list(
            action='PUT', append_local=append_local, append_remote=append_remote, base_dir=remote_base_dir,
            file_list=local_files, flat_dir=flat_dir, log_checksum=log_checksum, preserve_mtime=preserve_mtime,
            remove_source=remove_source
        )
        return files

    def put_by_regex(self, append_local: str = None, append_remote: str = None, flat_dir: bool = False,
                     local_base_dir: str = '.', log_checksum: bool = False, preserve_mtime: bool = True,
                     regex_filter: str = r'^', remote_dir: str = '.', remove_source: bool = False) -> List[str]:
        """Create a list of remote files to upload based on a regex, then upload.

        Creates a recursive list of files and directories in remote_dir and filters using re.search().

        Args:
            append_local: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If no
                          extension exists, then string is appended to end of filename.
            append_remote: String to replace extension (Path.suffix) with. Use '%' to represent original extension. If
                           no extension exists, then string is appended to end of filename.
            flat_dir: Do not recreate directory structure in local_base_dir.
            local_base_dir:
            log_checksum: Calculate file SHA256 checksum and log resulting value.
            preserve_mtime: Keep modification time of source file.
            regex_filter:
            remote_dir: Remote/source path and filename.
            remove_source:

        Returns:
            List of final destination file paths (after any name changes).
        """
        files = self._transfer_by_regex(
            action='PUT', append_local=append_local, append_remote=append_remote, base_dir=local_base_dir,
            flat_dir=flat_dir, log_checksum=log_checksum, preserve_mtime=preserve_mtime, regex_filter=regex_filter,
            source_dir=remote_dir, remove_source=remove_source
        )
        return files
