"""Registered primary-source policy for the overflow dashboard.

A bare HTTPS link is not evidence.  Only exact URLs in the source register with
an explicitly supported kind and expected host are accepted as primary row
references.  Project repository links are primary *for project facts*, never
independent corroboration of an owner report or a customer review.
"""
from __future__ import annotations
from urllib.parse import urlsplit

OFFICIAL_HOSTS = {
    'official-government': {
        'www.cslb.ca.gov', 'leginfo.legislature.ca.gov', 'www.sf.gov',
        'media.api.sf.gov', 'www.epa.gov',
    },
    'official-code-publisher': {'codelibrary.amlegal.com'},
    'official-manufacturer': {'www.watcomfg.com'},
    'official-company': {
        'www.rapidflowbayarea.com', 'www.aceplumbingandrooter.com',
        'www.heisesplumbing.com', 'www.eplumbingsolutions.com',
        'www.bayareaplumbingsf.com', 'www.fastresponseplumbingsf.com',
        'www.wedoconstructions.com', 'www.ayoobpeery.com',
        'www.bernalhilldrywall.com', 'sfbuildinggroup.com',
        'inandoutplumbing.com', 'www.atlasplumbingandrooter.com',
        'discoverplumbingandrooter.com',
    },
    'official-tool': {'github.com'},
}
OTHER_KINDS = {'owner-record', 'repository-primary', 'review-platform',
               'website-unresolved', 'unavailable-code-reference'}
LABELS = {
    'official-government': 'Official government',
    'official-code-publisher': 'Official code publisher',
    'official-manufacturer': 'Manufacturer',
    'official-company': 'Company, self-published',
    'official-tool': 'Official tool documentation',
    'repository-primary': 'Project record',
    'owner-record': 'Owner report',
    'review-platform': 'Review / third party',
    'website-unresolved': 'Unresolved website',
    'unavailable-code-reference': 'Unavailable code reference',
}


def https_parts(url: str):
    """Return safe HTTPS parts or None; never accept credentials or a port."""
    try:
        parts = urlsplit(url)
        if (parts.scheme != 'https' or not parts.hostname or parts.username
                or parts.password or parts.port is not None):
            return None
        return parts
    except (ValueError, TypeError):
        return None


def is_primary(source: dict) -> bool:
    """Whether this *registered, explicitly classified* source is a row reference."""
    kind = source.get('kind')
    parts = https_parts(source.get('url', ''))
    if not parts:
        return False
    if kind == 'repository-primary':
        # Restrict project-primary evidence to this project, not any GitHub URL.
        if source.get('official') is not False:
            return False
        if parts.hostname == 'github.com':
            return parts.path == '/karagemop466-tech/Korea8' or parts.path.startswith('/karagemop466-tech/Korea8/')
        if parts.hostname == 'api.github.com':
            return parts.path.startswith('/repos/karagemop466-tech/Korea8/')
        return False
    if kind not in OFFICIAL_HOSTS or source.get('official') is not True:
        return False
    if parts.hostname not in OFFICIAL_HOSTS[kind]:
        return False
    if kind == 'official-tool':
        return parts.path == '/actions/upload-pages-artifact' or parts.path.startswith('/actions/upload-pages-artifact/')
    return True


def validate_registry(sources: list[dict]) -> list[str]:
    """Check classifications, allowed hosts, IDs and URLs, without network access."""
    errors, ids, urls = [], set(), set()
    for source in sources:
        sid, url, kind = source.get('id'), source.get('url'), source.get('kind')
        if not sid or sid in ids:
            errors.append(f'duplicate/missing source id: {sid}')
        ids.add(sid)
        if not url or url in urls or not https_parts(url):
            errors.append(f'duplicate/unsafe source URL: {sid}')
        urls.add(url)
        if kind not in LABELS:
            errors.append(f'unknown source kind: {sid}: {kind}')
        elif kind in OFFICIAL_HOSTS or kind == 'repository-primary':
            if not is_primary(source):
                errors.append(f'untrusted primary classification/host: {sid}')
        elif source.get('official') is not False:
            errors.append(f'non-primary must not be official: {sid}')
        for field in ('title', 'publisher', 'checked', 'retrieval', 'supports', 'limitations'):
            if not source.get(field):
                errors.append(f'missing {field}: {sid}')
    return errors
