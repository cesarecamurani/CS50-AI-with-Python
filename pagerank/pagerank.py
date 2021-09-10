import os
import sys
import random
from random import choices
import re
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000
PROBABILITIES_SUM = 1


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)

    print(f"PageRank Results from Iteration")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # `1 - damping_factor`.
    one_minus_df = PROBABILITIES_SUM - damping_factor
    # Probability for page with no links.
    no_links_probability = PROBABILITIES_SUM / len(corpus)
    probabilities = {pg: no_links_probability for pg in corpus if not corpus[page]}

    if corpus[page]:
        # Calculates `damping_factor` probability.
        df_probability = damping_factor / len(corpus[page])
        # Calculates `1 - damping_factor` probability.
        one_minus_df_probability = one_minus_df / len(corpus)

        for pg in corpus:
            # Calculates the probability based on a page being a link in the passed page or not.
            if pg in corpus[page]:
                probabilities[pg] = df_probability + one_minus_df_probability
            else:
                probabilities[pg] = one_minus_df_probability

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = list()
    # Chooses a page at random to start and applies the transition model.
    sample = random.choice(list(corpus.keys()))
    sample_model = transition_model(corpus, sample, damping_factor)
    # For the number of samples given it generates the next sample from
    # the previous sample based on the previous sample’s transition model and
    # populates the samples list.
    for i in range(n):
        sample = choices(list(sample_model.keys()), list(sample_model.values()))[0]
        sample_model = transition_model(corpus, sample, damping_factor)

        samples.append(sample)
    # Calculates the probability for each page dividing the total page count
    # by the number of samples generated.
    pages_count = dict(Counter(samples))
    page_ranks = {page: pages_count[page] / n for page in corpus}

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    threshold = 0.001
    # We assign an initial rank of 1 / corpus length to each page.
    initial_rank = PROBABILITIES_SUM / N
    page_ranks = {page: initial_rank for page in corpus}

    while True:
        # For each page in corpus we apply the PR(p) formula (please see below).
        current_page_ranks = {page: calculate_page_rank(corpus, page, damping_factor, page_ranks) for page in corpus}
        # For each page in corpus we check the difference between the previous and the current page rank.
        margin = 0
        for page in corpus:
            margin = max(margin, abs(current_page_ranks[page] - page_ranks[page]))
        # If we reach the threshold we interrupt the iteration and return the pages ranks.
        if margin < threshold:
            break
        # Otherwise we keep re-assigning the page ranks to the current (temporary) page ranks.
        page_ranks = current_page_ranks.copy()

    return page_ranks


def calculate_page_rank(corpus, page, damping_factor, page_ranks):
    N = len(corpus)
    linked_pages_sum = 0
    # `1 - damping_factor` probability.
    one_minus_df_probability = (PROBABILITIES_SUM - damping_factor) / N

    for i in corpus:
        num_links = len(corpus[i])
        # If a page `i` doesn't have links to other pages, we'll divide the
        # page `i` probability equally by all the pages in the corpus.
        if not corpus[i]:
            linked_pages_sum += page_ranks[i] / N
        # If the given page `page` is a link in page `i`, we'll divide the
        # page `i` probability by the number of links in that page.
        if page in corpus[i]:
            linked_pages_sum += page_ranks[i] / num_links
    # Calculates the page rank adding the `1 - damping_factor` probability to
    # the product of the damping factor multiplied by the sum of probabilities
    # for the pages that link to that page.
    page_rank = one_minus_df_probability + damping_factor * linked_pages_sum

    return page_rank


if __name__ == "__main__":
    main()
