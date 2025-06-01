import hashlib
from ..models.spam_email_hash import SpamEmailHash
from .redis_bloom_filter import RedisBloomFilter


def spam_email_hash(email_msg: dict) -> str:
    subject = email_msg.get('payload', {}).get('headers', {}).get('Subject', '')
    body = email_msg.get('snippet', '')  # Or full text if available
    from_email = next(
        (h['value'] for h in email_msg.get('payload', {}).get('headers', []) if h['name'].lower() == 'from'),
        ''
    )
    combined = f"{subject.strip()}|{body.strip()}|{from_email.strip()}"
    return hashlib.sha256(combined.encode()).hexdigest()


def preload_bloom_from_db(session, bloom: RedisBloomFilter):
    existing_hashes = session.query(SpamEmailHash.hash).all()
    for (h,) in existing_hashes:
        if h not in bloom:
            bloom.add(h)

def add_spam_email_to_db(email_msg: dict, bloom: RedisBloomFilter, session):
    h = spam_email_hash(email_msg)
    bloom.add(h)

    subject = email_msg.get('payload', {}).get('headers', {}).get('Subject', '')
    from_email = next(
        (h['value'] for h in email_msg.get('payload', {}).get('headers', []) if h['name'].lower() == 'from'),
        ''
    )

    spam_entry = SpamEmailHash(hash=h, subject=subject, sender=from_email)
    session.add(spam_entry)
    session.commit()
