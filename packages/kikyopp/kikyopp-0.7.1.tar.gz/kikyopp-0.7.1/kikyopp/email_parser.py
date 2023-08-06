import email
import logging
import re
from typing import Optional

from flanker import mime
from flanker.addresslib import address
from flanker.mime.message.headers.wrappers import WithParams, ContentType
from flanker.mime.message.part import MimePart

from kikyopp.selector import Selector

log = logging.getLogger(__name__)


class BaseEmailParser:
    def parse_email(self, file_content: bytes) -> dict:
        data = {}
        msg = mime.from_string(email.message_from_bytes(file_content).as_string())
        try:
            self._parse_headers(msg, data)
            self._parse_content(msg, data)
        except Exception as e:
            log.error('Parse email error: %s', e)
        return data

    def _parse_headers(self, msg: MimePart, data: dict):
        data['subject'] = msg.headers.get('Subject')
        data['mail_from'] = msg.headers.get('From')
        data['mail_to'] = msg.headers.get('To')
        data['mail_cc'] = msg.headers.get('Cc')

        data['mail_from'] = str(address.parse(data['mail_from']))
        to_address_list = [str(i) for i in address.parse_list(data['mail_to'])]
        if len(to_address_list) == 0:
            data['mail_to'] = None
        elif len(to_address_list) == 1:
            data['mail_to'] = to_address_list[0]
        else:
            data['mail_to'] = to_address_list

        cc_address_list = [str(i) for i in address.parse_list(data['mail_cc'])]
        if len(cc_address_list) == 0:
            data['mail_cc'] = None
        elif len(cc_address_list) == 1:
            data['mail_cc'] = cc_address_list[0]
        else:
            data['mail_cc'] = cc_address_list

    def _parse_content(self, msg: MimePart, data: dict):
        content_type: ContentType = msg.content_type
        if 'content' not in data:
            data['content'] = ''
        if 'attachments' not in data:
            data['attachments'] = []
        if content_type.is_singlepart():
            if msg.body:
                data['content'] += _read_index_content(content_type, msg.body)
        elif content_type.is_multipart():
            for part in msg.parts:
                part_content_type: ContentType = part.content_type
                cd = part.headers.get('Content-Disposition')
                if cd and isinstance(cd, WithParams) and cd.value == 'attachment':
                    # 附件
                    filename = cd.params.get('filename')
                    if not filename:
                        filename = 'no_name'
                    if part.body:
                        filepath = self._save_attachment(filename, part_content_type, part.body)
                        data['attachments'].append({
                            'filename': filename,
                            'filepath': filepath,
                            'content_type': str(part_content_type)
                        })
                else:
                    if part_content_type.format_type == 'text':
                        data['content'] += _read_index_content(part_content_type, part.body)
                if isinstance(part, MimePart):
                    if len(part.parts) > 0:
                        for p in part.parts:
                            self._parse_content(p, data)

    def _save_attachment(self, filename: str, content_type: ContentType, content: bytes) -> Optional[str]:
        pass


blank_reg = re.compile(r'\s+')

CONTENT_LIMIT = 5000


def _read_index_content(content_type: ContentType, body) -> str:
    content = ''
    if content_type.format_type == 'text':
        if content_type.subtype == 'html':
            content = _get_text_from_html(body)
            if content:
                content = blank_reg.sub(' ', content)
                if len(content) > CONTENT_LIMIT:
                    content = content[:CONTENT_LIMIT]
        elif content_type.subtype == 'plain':
            content = body
            content = blank_reg.sub(' ', content)
            if len(content) > CONTENT_LIMIT:
                content = ''
    return content


def _get_text_from_html(html):
    try:
        selector = Selector(html)
        return selector.css('body').text[0]
    except Exception:
        return ''
