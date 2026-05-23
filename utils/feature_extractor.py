import re
import urllib.parse
import math
from collections import Counter


def extract_features_from_url(url: str) -> dict:
    features = {}
    parsed = _safe_parse(url)
    netloc = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''
    full = url.lower()

    # Strip www
    domain = re.sub(r'^www\.', '', netloc.lower())

    # ── UsingIP ──────────────────────────────────────────────
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features['UsingIP'] = -1 if re.search(ip_pattern, netloc) else 1

    # ── LongURL ───────────────────────────────────────────────
    length = len(url)
    if length < 54:
        features['LongURL'] = 1
    elif length <= 75:
        features['LongURL'] = 0
    else:
        features['LongURL'] = -1

    # ── ShortURL ──────────────────────────────────────────────
    shorteners = r'(bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|short\.io|is\.gd|buff\.ly|adf\.ly)'
    features['ShortURL'] = -1 if re.search(shorteners, full) else 1

    # ── Symbol@ ───────────────────────────────────────────────
    features['Symbol@'] = -1 if '@' in url else 1

    # ── Redirecting// ─────────────────────────────────────────
    stripped = re.sub(r'^https?://', '', url)
    features['Redirecting//'] = -1 if '//' in stripped else 1

    # ── PrefixSuffix- ─────────────────────────────────────────
    features['PrefixSuffix-'] = -1 if '-' in netloc else 1

    # ── SubDomains ────────────────────────────────────────────
    domain_parts = netloc.split('.')
    num_dots = len(domain_parts) - 1
    if num_dots == 1:
        features['SubDomains'] = 1
    elif num_dots == 2:
        features['SubDomains'] = 0
    else:
        features['SubDomains'] = -1

    # ── HTTPS ─────────────────────────────────────────────────
    features['HTTPS'] = 1 if url.startswith('https') else -1

    # ── DomainRegLen ──────────────────────────────────────────
    domain_len = len(netloc)
    features['DomainRegLen'] = 1 if domain_len < 20 else -1

    # ── Favicon (heuristic: HTTPS + known TLD = likely has favicon) ──
    safe_tlds = ['.com', '.org', '.edu', '.gov', '.net']
    has_safe_tld = any(netloc.endswith(t) for t in safe_tlds)
    features['Favicon'] = 1 if (url.startswith('https') and has_safe_tld) else -1

    # ── NonStdPort ────────────────────────────────────────────
    port = parsed.port
    features['NonStdPort'] = -1 if (port and port not in [80, 443]) else 1

    # ── HTTPSDomainURL ────────────────────────────────────────
    features['HTTPSDomainURL'] = -1 if 'https' in netloc else 1

    # ── RequestURL ────────────────────────────────────────────
    features['RequestURL'] = 1 if len(path.split('/')) < 6 else -1

    # ── AnchorURL (heuristic: deep path = likely has bad anchors) ────
    features['AnchorURL'] = -1 if len(path.split('/')) > 4 else 1

    # ── LinksInScriptTags (heuristic: query string complexity) ───────
    features['LinksInScriptTags'] = -1 if len(query) > 50 else 1

    # ── ServerFormHandler (heuristic: login/form keywords in path) ───
    form_keywords = ['login', 'signin', 'form', 'submit', 'account', 'update', 'verify']
    features['ServerFormHandler'] = -1 if any(k in path.lower() for k in form_keywords) else 1

    # ── InfoEmail ─────────────────────────────────────────────
    features['InfoEmail'] = -1 if 'mailto:' in full else 1

    # ── AbnormalURL ───────────────────────────────────────────
    features['AbnormalURL'] = -1 if netloc and netloc not in url else 1

    # ── WebsiteForwarding ─────────────────────────────────────
    redirect_count = full.count('http')
    features['WebsiteForwarding'] = -1 if redirect_count > 2 else 1

    # ── StatusBarCust (heuristic: obfuscated URL chars) ───────
    suspicious_chars = len(re.findall(r'%[0-9a-fA-F]{2}', url))
    features['StatusBarCust'] = -1 if suspicious_chars > 3 else 1

    # ── DisableRightClick (heuristic: very long query string) ─
    features['DisableRightClick'] = -1 if len(query) > 100 else 1

    # ── UsingPopupWindow (heuristic: suspicious keywords in URL) ─────
    popup_keywords = ['bonus', 'prize', 'winner', 'claim', 'reward', 'free', 'lucky']
    features['UsingPopupWindow'] = -1 if any(k in full for k in popup_keywords) else 1

    # ── IframeRedirection (heuristic: multiple subdomains) ────
    features['IframeRedirection'] = -1 if num_dots >= 3 else 1

    # ── AgeofDomain (heuristic: risky TLD = likely new domain) ───────
    risky_tlds = ['.cn', '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
    features['AgeofDomain'] = -1 if any(netloc.endswith(t) for t in risky_tlds) else 1

    # ── DNSRecording (heuristic: domain entropy = random generated) ──
    entropy = _entropy(domain.split('.')[0])
    features['DNSRecording'] = -1 if entropy > 3.5 else 1

    # ── WebsiteTraffic (heuristic: known legit domain) ────────
    known_legit = ['google', 'youtube', 'facebook', 'amazon', 'microsoft',
                   'apple', 'github', 'twitter', 'instagram', 'linkedin']
    features['WebsiteTraffic'] = 1 if any(k in netloc for k in known_legit) else -1

    # ── PageRank (heuristic: safe TLD + no risky signals) ─────
    risky_signals = (
        features['UsingIP'] == -1 or
        features['PrefixSuffix-'] == -1 or
        features['AgeofDomain'] == -1
    )
    features['PageRank'] = -1 if risky_signals else (1 if has_safe_tld else 0)

    # ── GoogleIndex (heuristic: https + safe TLD + no IP) ─────
    features['GoogleIndex'] = (
        1 if (url.startswith('https') and has_safe_tld and features['UsingIP'] == 1)
        else -1
    )

    # ── LinksPointingToPage (heuristic: phishing keyword density) ────
    phish_keywords = ['crypto', 'wallet', 'recover', 'claim', 'bonus', 'verify',
                      'secure', 'login', 'update', 'confirm', 'bank', 'paypal',
                      'netflix', 'amazon', 'apple', 'microsoft']
    keyword_hits = sum(1 for k in phish_keywords if k in full)
    if keyword_hits == 0:
        features['LinksPointingToPage'] = 1
    elif keyword_hits == 1:
        features['LinksPointingToPage'] = 0
    else:
        features['LinksPointingToPage'] = -1

    # ── StatsReport (heuristic: overall risk score) ────────────
    negative_count = sum(1 for v in features.values() if v == -1)
    if negative_count <= 2:
        features['StatsReport'] = 1
    elif negative_count <= 5:
        features['StatsReport'] = 0
    else:
        features['StatsReport'] = -1

    return features


def _entropy(s: str) -> float:
    """Shannon entropy of a string."""
    if not s:
        return 0
    counts = Counter(s)
    total = len(s)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def features_to_vector(features: dict, feature_names: list) -> list:
    return [features.get(col, 0) for col in feature_names]


def _safe_parse(url: str):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return urllib.parse.urlparse(url)
    except Exception:
        return urllib.parse.urlparse('')