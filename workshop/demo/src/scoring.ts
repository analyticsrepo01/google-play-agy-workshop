export function scoreAnswer(correct: boolean, usedHint: boolean): number {
  return correct ? (usedHint ? 75 : 100) : 0;
}
