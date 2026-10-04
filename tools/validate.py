"""Offline public-file and package checks; no third-party dependencies or network."""
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = {
    'carry-my-context': ['technical-continuity.md'],
    'challenge-my-plan': ['decision-tests.md'],
    'check-my-work': ['documents-and-numbers.md', 'software-checks.md'],
    'shape-my-idea': ['domain-prompts.md'],
}
UPSTREAMS = {'Pablo-aps/prove-it', 'bmad-code-org/BMAD-METHOD', 'jumpifequal/handoff-skill',
             'msitarzewski/agency-agents', 'obra/superpowers', 'phuryn/pm-skills', 'uchimata2/handoff-skill'}
RELEASE_FILES = {
    'plugin.json', '.agents/plugins/marketplace.json', 'provenance.json',
    '.claude-plugin/plugin.json', '.claude-plugin/marketplace.json',
    'LICENSE', 'SOURCE_NOTICES.txt', 'INSTALL.txt', 'QUICK_START.txt',
    'README.md', 'README.zh-TW.md', 'CHANGELOG.md', 'CONTRIBUTING.md',
    'SECURITY.md', 'PRIVACY.md', 'CODE_OF_CONDUCT.md', 'docs/EXAMPLES.md',
    'docs/assets/social-preview.svg', 'docs/assets/social-preview.png',
    'docs/assets/plugin-icon.svg',
}
for role, refs in REFERENCES.items():
    RELEASE_FILES.update({f'skills/{role}/SKILL.md', f'skills/{role}/agents/openai.yaml'})
    RELEASE_FILES.update(f'skills/{role}/references/{ref}' for ref in refs)
RELEASE_FILES.update('licenses/' + repo.replace('/', '__') + '.txt' for repo in UPSTREAMS)
REPO_FILES = RELEASE_FILES | {
    '.gitignore', '.gitattributes', '.github/workflows/validate.yml',
    '.github/ISSUE_TEMPLATE/bug_report.yml', '.github/ISSUE_TEMPLATE/feature_request.yml',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/pull_request_template.md',
    'tools/validate.py', 'tools/build_release.py', 'tests/test_validation.py',
}
SKIP_DIRS = {'.git', '__pycache__', 'dist', '.venv', 'venv'}
# Only this reviewed PNG may bypass text decoding. Pin replacement bytes after review.
BINARY_SHA256 = {
    'docs/assets/social-preview.png': 'ef1a9c6889ad740f5d7c8f770c0e73aff70a54418b9507409d13d4a83e9a61f4',
}
REVIEWED_TEXT_ASSETS = {
    'docs/assets/plugin-icon.svg': '6851fb87fd3f657ca5b666669c7dcbe1b82731e9e991afffa6d94bdae41f84c2',
}
SIGNATURES = {
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----',
    'github_token': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})',
    'openai_token': r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}',
    'aws_key': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'service_token': r'\b(?:xox[baprs]-[A-Za-z0-9-]{20,}|AIza[A-Za-z0-9_-]{30,})',
    'credential_url': r'(?i)https?://[^\s/:@]+:[^\s/@]+@',
    'secret_assignment': r'(?im)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*[\x22\x27]?[A-Za-z0-9_+./=-]{16,}',
    'private_home_path': r'(?i)(?:[A-Z]:[/\\]Users[/\\][^\s/\\]+|/(?:Users|home)/[^\s/]+)',
    'private_workspace_path': r'(?i)D:[/\\](?:Codex|claude)\b',
    'invisible_unicode': '[\u202a-\u202e\u2066-\u2069\u200b\u200c\u200d\u2060\ufeff]',
}


class ValidationError(ValueError):
    pass


def require(condition, category):
    if not condition:
        raise ValidationError(category)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse_json(text):
    def unique_pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate_json_key')
            result[key] = value
        return result
    try:
        return json.loads(text, object_pairs_hook=unique_pairs)
    except json.JSONDecodeError as error:
        raise ValidationError('invalid_json') from error


def inventory(root):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for name in dirs + files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            require(not path.is_symlink() and not getattr(path.lstat(), 'st_file_attributes', 0) & 0x400, 'reparse_path:' + rel)
            if path.is_file():
                require(path.stat().st_size <= 1_000_000, 'oversize_file:' + rel)
                result[rel] = path.read_bytes()
    return result


def validate_tree(root=ROOT):
    root = Path(root).resolve()
    # Ignore local caches on disk, but never ignore files actually staged/tracked by Git.
    if (root / '.git').exists():
        try:
            tracked = subprocess.run(['git', '--no-optional-locks', '-C', str(root), 'ls-files', '-z'], capture_output=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError) as error:
            raise ValidationError('git_index_unavailable') from error
        names = set(tracked.decode('utf-8').rstrip('\0').split('\0')) - {''}
        require(names <= REPO_FILES, 'tracked_private_or_extra_file')
    files = inventory(root)
    require(set(files) == REPO_FILES, 'public_file_set')
    texts = {}
    for rel, data in files.items():
        if rel in BINARY_SHA256:
            require(sha(data) == BINARY_SHA256[rel], 'binary_asset_hash:' + rel)
            continue
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError as error:
            raise ValidationError('non_utf8:' + rel) from error
        texts[rel] = text
        if rel in REVIEWED_TEXT_ASSETS:
            require(sha(data) == REVIEWED_TEXT_ASSETS[rel], 'text_asset_hash:' + rel)
        for category, expression in SIGNATURES.items():
            hit = re.search(expression, text)
            if hit:
                line = text.count('\n', 0, hit.start()) + 1
                raise ValidationError(f'{category}:{rel}:{line}')
        require(not any(byte < 32 and byte not in (9, 10, 13) for byte in data), 'control_byte:' + rel)
        if rel.endswith('.json'):
            parse_json(text)
        if rel.endswith('.md'):
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                local = target.split('#', 1)[0]
                resolved = ((root / rel).parent / local).resolve()
                require(resolved.is_relative_to(root) and resolved.exists(), 'missing_or_unsafe_reference:' + rel)

    manifest = parse_json(texts['plugin.json'])
    require(manifest.get('$schema') == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'manifest_schema')
    require(manifest.get('name') == 'practical-work-kit', 'manifest_identity')
    require(isinstance(manifest.get('version'), str) and re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'manifest_version')
    require(manifest.get('license') == 'Apache-2.0', 'manifest_license')
    require(set(manifest) <= {'$schema', 'name', 'version', 'description', 'license', 'keywords', 'extensions', 'author', 'homepage', 'repository'}, 'runtime_manifest_field')
    require(set(manifest.get('extensions', {})) == {'com.openai'}, 'runtime_extension')
    require(set(manifest['extensions']['com.openai']) == {'interface'}, 'runtime_extension_field')
    interface = manifest['extensions']['com.openai']['interface']
    require(set(interface) <= {'displayName', 'shortDescription', 'longDescription', 'category', 'defaultPrompt', 'developerName', 'websiteURL', 'supportURL', 'privacyPolicyURL', 'brandColor', 'logo', 'composerIcon'}, 'runtime_interface_field')
    for key, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)]:
        require(isinstance(interface.get(key), str) and 0 < len(interface[key]) <= limit, 'interface_' + key)
    require(isinstance(manifest.get('author'), dict) and bool(manifest['author'].get('name')), 'author_missing')
    for key in ('logo', 'composerIcon'):
        require(interface.get(key) == './docs/assets/plugin-icon.svg', 'interface_' + key)
    require(interface.get('websiteURL') == 'https://github.com/Yingye107/practical-work-kit', 'interface_websiteURL')
    require(interface.get('supportURL') == 'https://github.com/Yingye107/practical-work-kit/issues', 'interface_supportURL')
    require(interface.get('privacyPolicyURL') == 'https://raw.githubusercontent.com/Yingye107/practical-work-kit/main/PRIVACY.md', 'interface_privacyPolicyURL')
    require(interface.get('brandColor') == '#176b54', 'interface_brandColor')
    require(isinstance(interface.get('defaultPrompt'), list) and 1 <= len(interface['defaultPrompt']) <= 3 and all(isinstance(prompt, str) and 0 < len(prompt) <= 128 for prompt in interface['defaultPrompt']), 'starter_prompts')
    catalog = parse_json(texts['.agents/plugins/marketplace.json'])
    require(catalog.get('name') == 'practical-work-kit' and len(catalog.get('plugins', [])) == 1, 'marketplace_identity')
    entry = catalog['plugins'][0]
    require(entry.get('name') == manifest['name'] and entry.get('source') == {'source': 'local', 'path': './'}, 'marketplace_source')

    for role in REFERENCES:
        text = texts[f'skills/{role}/SKILL.md']
        front = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        require(front is not None and re.search(r'^name:\s*' + re.escape(role) + r'\s*$', front.group(1), re.M), 'skill_identity:' + role)
        require(re.search(r'^description:\s*\S', front.group(1), re.M), 'skill_description:' + role)
        ui = texts[f'skills/{role}/agents/openai.yaml']
        require('$' + role in ui and not re.search(r'^(?:dependencies|hooks|scripts|policy):', ui, re.M), 'skill_ui_or_runtime:' + role)

    # Both hosts discover the same default skills/ directory. No runtime components.
    claude = parse_json(texts['.claude-plugin/plugin.json'])
    require(set(claude) == {'name', 'version', 'description', 'author', 'homepage',
                           'repository', 'license', 'keywords'}, 'claude_runtime_manifest_field')
    for key in ('name', 'version', 'license', 'author', 'homepage', 'repository', 'keywords'):
        require(claude.get(key) == manifest.get(key), 'claude_manifest_' + key)
    require(isinstance(claude.get('description'), str) and bool(claude['description']),
            'claude_manifest_description')
    claude_market = parse_json(texts['.claude-plugin/marketplace.json'])
    require(set(claude_market) == {'name', 'description', 'owner', 'plugins'} and
            claude_market['name'] == claude['name'] and
            claude_market['description'] == claude['description'] and
            claude_market['owner'] == {'name': claude['author']['name']}, 'claude_marketplace_identity')
    require(isinstance(claude_market['plugins'], list) and len(claude_market['plugins']) == 1,
            'claude_marketplace_entries')
    entry = claude_market['plugins'][0]
    require(isinstance(entry, dict) and set(entry) == {'name', 'source', 'description'},
            'claude_marketplace_fields')
    require(entry['name'] == claude['name'] and entry['description'] == claude['description'],
            'claude_marketplace_entry')
    require(entry['source'] == './', 'claude_marketplace_source')

    provenance = parse_json(texts['provenance.json'])
    sources = provenance.get('sources', [])
    require(len(sources) == len(UPSTREAMS) and {item.get('repo') for item in sources} == UPSTREAMS, 'source_set')
    for source in sources:
        repo, commit = source['repo'], source.get('commit', '')
        require(re.fullmatch(r'[a-f0-9]{40}', commit), 'source_unpinned')
        license_items = [item for item in source.get('files', []) if item.get('path') == 'LICENSE']
        require(len(license_items) == 1, 'license_source_missing')
        item = license_items[0]
        rel = 'licenses/' + repo.replace('/', '__') + '.txt'
        require(sha(files[rel]) == item.get('sha256'), 'license_hash:' + rel)
        for item in source['files']:
            require(item.get('url') == f'https://raw.githubusercontent.com/{repo}/{commit}/' + item.get('path', ''), 'source_url')
            require(isinstance(item.get('sha256'), str) and re.fullmatch(r'[a-f0-9]{64}', item['sha256']), 'source_hash')
        require(rel in texts['SOURCE_NOTICES.txt'], 'license_notice_missing')
    return {'status': 'PASS', 'repository_files': len(files), 'release_files': len(RELEASE_FILES),
            'version': manifest['version'], 'file_sha256': {rel: sha(data) for rel, data in sorted(files.items())},
            'limits': 'Bounded signatures and package checks; not complete secret, legal, or host security assurance.'}


def validate_archive(path, root=ROOT):
    root = Path(root).resolve()
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        require(len(names) == len(set(names)), 'archive_duplicate')
        require(sum(item.file_size for item in infos) <= 3_000_000, 'archive_size')
        for item in infos:
            name, pure = item.filename, PurePosixPath(item.filename)
            require(name and not pure.is_absolute() and '..' not in pure.parts and '\\' not in name and ':' not in name and name == pure.as_posix(), 'archive_path')
            require(not stat.S_ISLNK(item.external_attr >> 16), 'archive_symlink')
            require(not item.flag_bits & 1 and item.file_size <= 1_000_000, 'archive_entry')
        require(set(names) == RELEASE_FILES, 'archive_file_set')
        require(all(archive.read(rel) == (root / rel).read_bytes() for rel in RELEASE_FILES), 'archive_content')
    return {'status': 'PASS', 'entries': len(names), 'sha256': sha(Path(path).read_bytes())}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = validate_tree(args.root)
    except (ValidationError, KeyError, TypeError, AttributeError) as error:
        print(json.dumps({'status': 'FAIL', 'reason': str(error)}))
        raise SystemExit(1)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'repository_files', 'release_files', 'version')}))
