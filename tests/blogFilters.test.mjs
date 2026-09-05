import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import ts from 'typescript';

// Compile the pure selector with the project's existing TypeScript dependency (Node 20 compatible).
const source = readFileSync(new URL('../src/lib/blogFilters.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext } });
const { notesForLocale, isPublicNote } = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
const post = (slug, locale, translationGroup) => ({ slug, data: { locale, translationGroup } });

test('translation groups select the requested locale regardless of input order', () => {
  const versions = ['ja', 'en', 'zh'].map(locale => post(locale, locale, 'rotterdam'));
  for (const locale of ['en', 'ja', 'zh']) {
    for (const input of [versions, [...versions].reverse()]) {
      assert.deepEqual(notesForLocale(input, locale).map(p => p.slug), [locale]);
    }
  }
});

test('ungrouped legacy and single-language entries stay visible without mutating input', () => {
  const input = [post('legacy'), post('single-ja', 'ja'), post('grouped-ja', 'ja', 'solo')];
  const before = structuredClone(input);
  for (const locale of ['en', 'ja', 'zh']) assert.deepEqual(notesForLocale(input, locale), input);
  assert.deepEqual(input, before);
  assert.equal(input.filter(isPublicNote).length, input.length);
});

test('missing translations fall back to English, then the first available version', () => {
  const ja = post('ja', 'ja', 'group');
  const en = post('en', 'en', 'group');
  assert.deepEqual(notesForLocale([ja, en], 'zh'), [en]);
  assert.deepEqual(notesForLocale([ja], 'zh'), [ja]);
  assert.deepEqual(notesForLocale([], 'zh'), []);
});
