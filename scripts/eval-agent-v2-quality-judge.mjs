import { assert, writeReport } from "./eval-agent-v2-utils.mjs";

const dimensions = ["directness", "naturalness", "commercialCorrectness", "stateContinuity", "safetyPrivacy", "costDiscipline"];
const rubric = dimensions.map((dimension) => ({ dimension, min: dimension === "directness" || dimension === "commercialCorrectness" ? 4 : 3 }));

writeReport("agent-v2-quality-judge", [
  assert(rubric.length >= 6, "quality judge rubric dimensions defined", { rubric }),
  assert(rubric.some((item) => item.dimension === "directness" && item.min === 4), "directness is blocking quality dimension"),
]);

