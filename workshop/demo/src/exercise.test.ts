import assert from 'node:assert/strict';
import { test } from 'node:test';

if (process.env.SCORING_SOLUTION !== undefined && process.env.SCORING_SOLUTION !== '1') {
  throw new Error('SCORING_SOLUTION must be absent (learner stub) or 1 (facilitator solution).');
}
const { scoreAnswer } = await import(
  process.env.SCORING_SOLUTION === '1' ? './exercise.solution.ts' : './exercise.ts'
);
test('a correct answer without a hint earns 100 points', () => {
  assert.equal(scoreAnswer(true, false), 100);
});
test('a correct answer after a hint earns 75 points', () => {
  assert.equal(scoreAnswer(true, true), 75);
});
test('wrong answers never earn points, with or without a hint', () => {
  assert.equal(scoreAnswer(false, false), 0);
  assert.equal(scoreAnswer(false, true), 0);
});
