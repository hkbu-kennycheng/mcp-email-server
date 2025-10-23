from datetime import datetime
from typing import Any

from pydantic import BaseModel



def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class EmailMetadata(BaseModel):
    """Email metadata"""

    email_id: str
    subject: str
    sender: str
    recipients: list[str]  # Recipient list
    date: datetime
    attachments: list[str]

    @classmethod
    def from_email(cls, email: dict[str, Any]):
        return cls(
            email_id=email["email_id"],
            subject=email["subject"],
            sender=email["from"],
            recipients=email.get("to", []),
            date=email["date"],
            attachments=email["attachments"],
        )

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


class EmailMetadataPageResponse(BaseModel):
    """Paged email metadata response"""

    page: int
    page_size: int
    before: datetime | None
    since: datetime | None
    subject: str | None
    emails: list[EmailMetadata]
    total: int


class EmailBodyResponse(BaseModel):
    """Single email body response"""

    email_id: str  # IMAP UID of this email
    subject: str
    sender: str
    recipients: list[str]
    date: datetime
    body: str
    attachments: list[str]


class EmailContentBatchResponse(BaseModel):
    """Batch email content response for multiple emails"""

    emails: list[EmailBodyResponse]
    requested_count: int
    retrieved_count: int
    failed_ids: list[str]
