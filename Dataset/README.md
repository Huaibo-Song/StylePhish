
# Dataset Description

We evaluate model performance from multiple perspectives, including false positive (FP) rate on benign webpages, phishing detection performance on two datasets, and robustness against attacks.

## False Positive Dataset
We use the benign test dataset from VisualPhishNet paper as the FP evaluation dataset.

## Benchmark Dataset
We conduct experiments on two datasets:

1. Phishpedia Dataset - The publicly available Phishpedia dataset with duplicate samples removed.
2. StylePhish Dataset - We crawl real-world phishing webpages from OpenPhish and perform deduplication

## Logo Attack Datasets
we construct two categories of logo attack datasets based on the dataset originally introduced by Ji et al. to evaluate the robustness of our method against visual deception attacks:

1. Perceptible Logo Modification Attacks
2. Imperceptible Logo Adversarial Attacks

## Webpage-Level Attack Dataset
We construct three types of webpage-level evasion attacks to evaluate the robustness of our method:

1. Layout Attacks
2. Color Attacks
3. Typography Attacks
