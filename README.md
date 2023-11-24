# prediction-triple-classifier

Classify the precedence triple predictions into either true or false from previous prediction, using semi-supervised learning.
Before this, we run the triple prediction 100 times and selected top 25% of the predictions.
We use `score`, `triple_incidence`, `head_rate`, and `tail_rate` as features.
 * `score`: average score from triple prediction stage
 * `triple_incidence`: the incidence of the triple among the 100 predictions
 * `head_rate`: the rate of this head appearing in all triples
 * `tail_rate`: the rate of this tail appearing in all triples
