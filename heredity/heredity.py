import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Maps every person to their gene count.
    people_details = map_people_to_genes(people, one_gene, two_genes)

    joint_probability_calculation = 1

    probability_sum = 1

    mutation = PROBS["mutation"]
    # Maps every gene count to the probability to be passed on.
    gene_passing_probabilities = {
        2: 1.0 - mutation,
        1: 0.5,
        0: 0.0 + mutation
    }

    for person in people:
        gene_count = people_details[person]["gene"]
        trait = True if person in have_trait else False
        # Maps every person to their trait probability.
        people_details[person]["trait_probability"] = PROBS["trait"][gene_count][trait]
        # Finds the parents.
        mother = people[person]["mother"]
        father = people[person]["father"]

        if mother is None and father is None:
            # Sets the person"s gene probability to the unconditional probability in case of no parents.
            people_details[person]["gene_probability"] = PROBS["gene"][gene_count]
        else:
            # Finds the parent"s genes.
            mother_gene = people_details[mother]["gene"]
            father_gene = people_details[father]["gene"]
            # Fetches passing probability from gene_passing_probabilities and calculates the probability of NOT passing it.
            mother_passing_prob = gene_passing_probabilities[mother_gene]
            father_passing_prob = gene_passing_probabilities[father_gene]
            mother_not_passing_prob = probability_sum - mother_passing_prob
            father_not_passing_prob = probability_sum - father_passing_prob

            gene = people_details[person]["gene"]
            match gene:
                case 1:
                    # If the person"s gene is 1 than the gene probability is the probability that the mother does not pass it,
                    # multiplied by the father probability of passing it, added to the product of the probability that the mother
                    # passes it and the father probability of NOT passing it.
                    people_details[person]["gene_probability"] = (
                        (mother_not_passing_prob * father_passing_prob) +
                        (mother_passing_prob * father_not_passing_prob)
                    )
                case 2:
                    # If the person"s gene is 2 than the gene probability is calculated multiplying
                    # mother"s and father"s probabilities of passing it.
                    people_details[person]["gene_probability"] = mother_passing_prob * father_passing_prob
                case 0:
                    # If the person"s gene is 0 than the gene probability is calculated multiplying
                    # mother"s and father"s probabilities of NOT passing it.
                    people_details[person]["gene_probability"] = mother_not_passing_prob * father_not_passing_prob

        gene_probability = people_details[person]["gene_probability"]
        trait_probability = people_details[person]["trait_probability"]
        # Calculates every person"s joint probability of gene and trait together.
        people_details[person]["joint_probability"] = gene_probability * trait_probability
        # Calculates the overall joint probability.
        joint_probability_calculation *= people_details[person]["joint_probability"]

    return joint_probability_calculation


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Maps every person to their gene count.
    people = map_people_to_genes(probabilities, one_gene, two_genes)

    for person in probabilities:
        # Adds the gene probability given the gene count.
        gene = people[person]["gene"]
        probabilities[person]["gene"][gene] += p
        # Adds the trait probability given the person having or not the trait.
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    sum_genes = dict()
    sum_traits = dict()

    for person in probabilities:
        gene_probabilities = probabilities[person]["gene"]
        trait_probabilities = probabilities[person]["trait"]
        # Sums all the genes probabilities for a given person.
        sum_genes[person] = sum(gene_probabilities.values())
        # Sums all the traits probabilities for a given person.
        sum_traits[person] = sum(trait_probabilities.values())
        # Normalizes (rescales) each gene probability to be between
        # 0 and 1, dividing by the sum of all genes probabilities for that person
        # (and re-assigning it to the gene probability itself).
        for gene in gene_probabilities:
            probabilities[person]["gene"][gene] /= sum_genes[person]
        # Normalizes (rescales) each trait probability to be between
        # 0 and 1, dividing by the sum of all traits probabilities for that person
        # (and re-assigning it to the trait probability itself).
        for trait in trait_probabilities:
            probabilities[person]["trait"][trait] /= sum_traits[person]


def map_people_to_genes(dictionary, one_gene, two_genes):
    # Find people with zero genes.
    zero_genes = set(dictionary) - (one_gene.union(two_genes))
    # Maps every person to their gene count.
    zero_genes_people = {person: {"gene": 0} for person in zero_genes}
    one_genes_people = {person: {"gene": 1} for person in one_gene}
    two_genes_people = {person: {"gene": 2} for person in two_genes}

    people = zero_genes_people | one_genes_people | two_genes_people

    return people


if __name__ == "__main__":
    main()
