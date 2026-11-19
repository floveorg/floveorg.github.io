'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { _internal } = require('../src/docsify-edit.js');

const { headingTexts, splitBlocks, normBlock, wrapPlain, normalizeListMarkers } = _internal;

test('splitBlocks keeps fenced code whole', () => {
  const blocks = splitBlocks('before\n\n```js\na\n\nb\n```\n\nafter');
  assert.equal(blocks.length, 3);
  assert.match(blocks[1], /```js[\s\S]*\n\nb\n```/);
});

test('splitBlocks separates paragraphs', () => {
  assert.deepEqual(splitBlocks('one\n\ntwo'), ['one', 'two']);
});

test('splitBlocks keeps a loose list together', () => {
  const blocks = splitBlocks('- one\n\n- two\n\nparagraph');
  assert.equal(blocks.length, 2);
  assert.match(blocks[0], /- one\n\n- two/);
});

test('normBlock ignores emphasis, code ticks and line wrapping', () => {
  assert.equal(normBlock('A **bold** word'), normBlock('A __bold__\nword'));
  assert.equal(normBlock('`code` here'), normBlock('code here'));
  assert.equal(normBlock('> quoted\n> text'), normBlock('> quoted text'));
});

test('normBlock normalises link depth and table padding', () => {
  assert.equal(normBlock('[a](../../../apps/x.md)'), normBlock('[a](../apps/x.md)'));
  assert.equal(normBlock('| a | b |\n|---|---|\n| 1 | 2 |'),
               normBlock('| a | b |\n| --- | --- |\n| 1 | 2 |'));
});

test('wrapPlain wraps only plain paragraphs', () => {
  const long = 'word '.repeat(40).trim();
  const wrapped = wrapPlain(long);
  for (const line of wrapped.split('\n')) assert.ok(line.length <= 80, line);
  assert.equal(wrapPlain('- a long list item '.repeat(10)), '- a long list item '.repeat(10));
  assert.match(wrapPlain('hard  \nbreak'), /  \n/);
});

test('normalizeListMarkers matches the house style', () => {
  assert.equal(normalizeListMarkers('-   [x]  done'), '- [x] done');
  assert.equal(normalizeListMarkers('1.  one\n2.  two'), '1. one\n2. two');
});

test('headingTexts ignores headings inside fenced code', () => {
  const md = '# One\n\n```\n# not a heading\n```\n\n## Two';
  assert.deepEqual(headingTexts(md), ['One', 'Two']);
});
