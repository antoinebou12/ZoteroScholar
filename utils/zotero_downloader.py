import logging
import os
import re

from pyzotero import zotero

logger = logging.getLogger(__name__)

class ZoteroDownloader:
    def __init__(
        self,
        user_id: str,
        api_key: str,
        base_path: str = "data/zotero_papers",
    ):
        self.user_id = user_id
        self.api_key = api_key
        self.zot = zotero.Zotero(self.user_id, 'user', self.api_key)
        self.base_path = base_path

    def download_pdfs(self, group_limit: int = None):
        if group_limit is None:
            # Download from personal library
            self._download_attachments(self.zot, self.base_path)
        else:
            # Download from groups, respecting the group_limit
            groups = self.zot.groups()
            for group in groups[:group_limit]:
                group_id = group['id']
                group_name = self._sanitize_filename(group['data']['name'])
                group_path = os.path.join(
                    self.base_path,
                    f"user_{self.user_id}",
                    f"group_{group_id}_{group_name}",
                )
                zot_group = zotero.Zotero(group_id, 'group', self.api_key)
                self._download_attachments(zot_group, group_path)

    def _download_attachments(self, zot_instance, path: str):
        # Ensure the download directory exists
        os.makedirs(path, exist_ok=True)
        # Fetch all PDF attachments
        attachments = zot_instance.everything(
            zot_instance.items(itemType='attachment', linkMode='imported_file')
        )
        for attachment in attachments:
            # Check if the attachment is a PDF
            if 'application/pdf' in attachment['data'].get('contentType', ''):
                filename = attachment['data'].get('filename', 'unnamed.pdf')
                filename = self._sanitize_filename(filename)
                pdf_path = os.path.join(path, filename)
                # Skip download if file already exists
                if not os.path.exists(pdf_path):
                    try:
                        # Download the PDF file content
                        pdf_content = zot_instance.file(attachment['key'])
                        # Save the PDF file to the specified path
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_content)
                        logger.info(f"Successfully downloaded: {filename}")
                    except Exception as e:
                        logger.error(f"Error downloading {filename}: {e}")
                        continue
                else:
                    logger.info(f"File already exists. Skipping: {filename}")

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing whitespace
        filename = filename.strip()
        return filename
