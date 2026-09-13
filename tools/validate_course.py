"""Validate the course wiring without implementing any emulator method bodies."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'course/lessons.json').read_text(encoding='utf-8'))
assert [x['id'] for x in catalog] == [f'{n:02}' for n in range(1, 41)]
expected = sum(x['count'] for x in catalog)
for item in catalog:
    folder = root / item['folder']
    assert (folder / 'README.md').exists() and (folder / 'learn.cmd').exists()
    text = (folder / 'README.md').read_text(encoding='utf-8')
    for heading in ['## The GBA behavior', '## C# you need now', '## Write it', '## Check it']:
        assert heading in text, (item['id'], heading)
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in target:
            assert (folder / target.split('#')[0]).exists(), (item['id'], target)
    for template in item['templates']:
        content = (root / template['source']).read_text(encoding='utf-8')
        assert content.strip()
        if template['target'].startswith('tests/'):
            assert content.count('[Fact]') == item['count'], item['id']

# An isolated copy compiles ALL future starter/check templates. Nothing is staged
# in the learner's real src/tests and no emulator bodies are completed here.
scratch = root / '.work/course-validation'
scratch.mkdir(parents=True, exist_ok=True)
for name in ['GbaEmulator.sln', 'global.json', 'src/Gba.Core/Gba.Core.csproj',
             'src/Gba.Desktop/Gba.Desktop.csproj', 'src/Gba.Desktop/Program.cs',
             'tests/Gba.Core.Tests/Gba.Core.Tests.csproj',
             'src/Gba.Core/Memory/Ewram.cs', 'tests/Gba.Core.Tests/EwramTests.cs']:
    target = scratch / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / name, target)
for item in catalog:
    for template in item['templates']:
        target = scratch / template['target']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / template['source'], target)
dotnet = root / '.work/dotnet10/dotnet.exe'
if not dotnet.exists(): dotnet = Path(shutil.which('dotnet'))
def run(args, cwd=scratch):
    result = subprocess.run([str(dotnet), *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result
result = run(['build', 'GbaEmulator.sln', '--nologo'])
assert result.returncode == 0, result.stdout + result.stderr
result = run(['test', 'tests/Gba.Core.Tests/Gba.Core.Tests.csproj', '--no-build', '--logger', 'trx;LogFileName=all.trx', '--results-directory', 'reports'])
report = ET.parse(scratch / 'reports/all.trx')
results = report.findall('.//{*}UnitTestResult')
assert len(results) == expected, (len(results), expected, result.stdout)
# These are deliberately unfinished starters. A failing result is expected;
# the audit checks discovery/compilation rather than claiming hardware correctness.
print(f'{len(catalog)} lesson pages/links audited; all starter files compile; {len(results)} supplied checks discovered.')
print(f'Unfinished starters: {sum(r.get("outcome") == "Failed" for r in results)} expected failures. No emulator solutions written.')

# Exercise navigation/guardrails with toy TEST fixtures, not emulator solutions.
smoke = root / '.work/course-runner-validation'
smoke.mkdir(parents=True, exist_ok=True)
for name in ['GbaEmulator.sln', 'global.json', 'src/Gba.Core/Gba.Core.csproj',
             'src/Gba.Desktop/Gba.Desktop.csproj', 'src/Gba.Desktop/Program.cs',
             'tests/Gba.Core.Tests/Gba.Core.Tests.csproj', 'tools/course.ps1']:
    target = smoke / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / name, target)
first = smoke / 'tests/Gba.Core.Tests/FirstTests.cs'
first.write_text('[Trait("Lesson","01")] public class FirstTests { [Fact] public void Plumbing_check() { Assert.True(true); } }', encoding='utf-8')
toy = []
for n in range(1, 4):
    ident = f'{n:02}'
    folder = smoke / f'course/{ident}'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'README.md').write_text('Toy runner validation only.', encoding='utf-8')
    templates = []
    if n == 2:
        (folder / 'checks.cs.txt').write_text('[Trait("Lesson","02")] public class Course02Tests { [Fact] public void Second_plumbing_check() { Assert.True(true); } }', encoding='utf-8')
        templates.append(dict(source='course/02/checks.cs.txt', target='tests/Gba.Core.Tests/Course02Tests.cs'))
    toy.append(dict(id=ident,title='Runner fixture '+ident,folder=f'course/{ident}',file='src/Gba.Core/Keep.cs',mode='observed' if n==3 else 'automatic',count=0 if n==3 else 1,checks=['Observe a toy result.'],templates=templates))
(smoke / 'course/lessons.json').write_text(json.dumps(toy), encoding='utf-8')
sentinel = smoke / 'src/Gba.Core/Keep.cs'
sentinel.write_text('// Existing learner file must survive navigation.\n', encoding='utf-8')
# Explicitly make a conflicting template: the runner must preserve the target.
(smoke / 'course/02/starter.cs.txt').write_text('// Template must NOT replace the existing file.\n', encoding='utf-8')
toy[1]['templates'].append(dict(source='course/02/starter.cs.txt',target='src/Gba.Core/Keep.cs'))
(smoke / 'course/lessons.json').write_text(json.dumps(toy), encoding='utf-8')
env = __import__('os').environ.copy()
env['PATH'] = str(dotnet.parent) + __import__('os').pathsep + env['PATH']
def runner(*args):
    result = subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(smoke/'tools/course.ps1'),*args], cwd=smoke, env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    return result
def state():
    return json.loads((smoke/'.work/course-progress.json').read_text(encoding='utf-8-sig'))
for args, code in [(('-Lesson','01','-Once'),0), (('-Next',),0), (('-Once',),0)]:
    result=runner(*args)
    assert result.returncode == code, (args, result.stdout, result.stderr)
assert state()['current']=='02'
assert sentinel.read_text(encoding='utf-8').startswith('// Existing learner')
second = smoke / 'tests/Gba.Core.Tests/Course02Tests.cs'
valid = second.read_text(encoding='utf-8')
second.write_text(valid.replace('Assert.True(true)', 'Assert.True(false)'), encoding='utf-8')
result = runner('-Next')
assert result.returncode == 1 and state()['current']=='02', result.stdout
second.write_text(valid.replace('"Lesson","02"', '"Lesson","99"'), encoding='utf-8')
result = runner('-Once')
assert result.returncode == 1 and 'discovered 1' in result.stdout, result.stdout
second.write_text(valid + '\nTHIS IS NOT CSHARP', encoding='utf-8')
result=runner('-Once')
assert result.returncode == 1 and 'could not be checked' in result.stdout, result.stdout
second.write_text(valid, encoding='utf-8')
result=runner('-Lesson','03','-Next')
assert result.returncode == 2 and state()['current']=='03', result.stdout
assert not any(r['id']=='03' for r in state()['reviewed'])
toy[0]['retireChecks'] = [dict(fromLesson=2,name='FirstTests.Plumbing_check')]
(smoke / 'course/lessons.json').write_text(json.dumps(toy), encoding='utf-8')
first.write_text(first.read_text(encoding='utf-8').replace('Assert.True(true)','Assert.True(false)'), encoding='utf-8')
result=runner('-Lesson','02','-Once')
assert result.returncode == 0 and '1/1 checks passed' in result.stdout, result.stdout
print('Runner verified: success, next/resume, failed/missing checks, compiler errors, no overwrite, retirement of temporary restrictions, and no automatic completion of observed work.')
