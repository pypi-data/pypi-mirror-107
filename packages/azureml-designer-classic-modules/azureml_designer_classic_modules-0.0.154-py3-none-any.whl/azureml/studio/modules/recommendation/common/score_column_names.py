from enum import Enum


class PortScheme(Enum):
    """Define Evaluate Recommender module inputs scheme, or score recommender modules output scheme.

    Evaluate Recommender module supports two kinds of inputs scheme:
    1. One Port scheme, only need Scored Dataset port input. This scheme is useful for anonymized dataset, where
    there are not explicit user/item columns, such as Criteo dataset.
    2. Two Port scheme, need both Scored Dataset and Test Dataset port inputs, this scheme cannot support anonymized
    dataset mentioned before, because the module cannot combine Scored Dataset and Test Dataset according to
    their user and item columns.
    Under other situations except for the anonymized cases, the two kinds of port schemes are both available. The
    Evaluate Recommender will deduce the port scheme, according to the scored dataset generated by upstream score
    recommender modules.
    """
    OnePort = "OnePort"
    TwoPort = "TwoPort"


# common constant defined for three kinds of tasks
USER_COLUMN = "User"
ITEM_COLUMN = "Item"

# types defined for score column names attr in DataFrameSchema
RECOMMENDATION_USER_COLUMN_TYPE = "Recommendation User Column"
RECOMMENDATION_ITEM_COLUMN_TYPE = "Recommendation Item Column"

# part for regression
SCORED_RATING = "Scored Rating"
TRUE_RATING = "Rating"
# constants for backward compatible regression
BACKWARD_COMPATIBLE_SCORED_RATING = "Rating"

# types defined for score column names attr in DataFrameSchema
RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE = "Recommendation Regression Scored Rating"


def build_regression_column_names(port_scheme: PortScheme):
    if port_scheme == PortScheme.OnePort:
        return [TRUE_RATING, SCORED_RATING]
    elif port_scheme == PortScheme.TwoPort:
        return [USER_COLUMN, ITEM_COLUMN, SCORED_RATING]


def build_backward_compatibility_regression_column_names():
    # older legacy evaluate recommender module only supports two port scheme
    return [USER_COLUMN, ITEM_COLUMN, BACKWARD_COMPATIBLE_SCORED_RATING]


# for DataFrameSchema score column name attr support
def build_regression_column_name_keys(port_scheme: PortScheme):
    if port_scheme == PortScheme.OnePort:
        return [RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE]
    else:
        return [RECOMMENDATION_USER_COLUMN_TYPE, RECOMMENDATION_ITEM_COLUMN_TYPE,
                RECOMMENDATION_REGRESSION_SCORED_RATING_TYPE]


# part for ranking
# constants defined for recommending items from rated items
RATED_ITEM = "Rated Item"
RECOMMENDED_ITEM_RATING = "True Rating"
TRUE_TOP_RATING = "True Top Rating"
# constants for backward compatible rated items recommendation
BACKWARD_COMPATIBLE_RATED_ITEM = "Item"

# types defined for score column names attr in DataFrameSchema
RECOMMENDATION_RATED_RANKING_RATED_ITEM_TYPE = "Recommendation Rated Ranking Rated Item"
RECOMMENDATION_RATED_RANKING_TRUE_RATING_TYPE = "Recommendation Rated Ranking True Rating"
RECOMMENDATION_RATED_RANKING_TRUE_TOP_RATING_TYPE = "Recommendation Rated Ranking True Top Rating"


def build_rated_ranking_column_names(port_scheme: PortScheme, top_k: int):
    column_names = [USER_COLUMN]
    if port_scheme == PortScheme.OnePort:
        column_names += [None] * 2 * top_k
        column_names[1::2] = [f"{RATED_ITEM} {i}" for i in range(1, top_k + 1)]
        column_names[2::2] = [f"{RECOMMENDED_ITEM_RATING} {i}" for i in range(1, top_k + 1)]
        column_names += [f"{TRUE_TOP_RATING} {i}" for i in range(1, top_k + 1)]
    elif port_scheme == PortScheme.TwoPort:
        column_names += [f"{RATED_ITEM} {i}" for i in range(1, top_k + 1)]
    return column_names


def build_backward_compatible_rated_ranking_column_names(top_k: int):
    # older legacy evaluate recommender module only supports two port scheme
    column_names = [USER_COLUMN]
    column_names += [f"{BACKWARD_COMPATIBLE_RATED_ITEM} {i}" for i in range(1, top_k + 1)]

    return column_names


# for DataFrameSchema score column name attr support
def build_rated_ranking_column_name_keys(port_scheme: PortScheme, top_k: int):
    column_name_keys = [RECOMMENDATION_USER_COLUMN_TYPE]
    if port_scheme == PortScheme.OnePort:
        column_name_keys += [None] * 2 * top_k
        column_name_keys[1::2] = [f"{RECOMMENDATION_RATED_RANKING_RATED_ITEM_TYPE} {i}" for i in range(1, top_k + 1)]
        column_name_keys[2::2] = [f"{RECOMMENDATION_RATED_RANKING_TRUE_RATING_TYPE} {i}" for i in range(1, top_k + 1)]
        column_name_keys += [f"{RECOMMENDATION_RATED_RANKING_TRUE_TOP_RATING_TYPE} {i}" for i in range(1, top_k + 1)]
    elif port_scheme == PortScheme.TwoPort:
        column_name_keys += [f"{RECOMMENDATION_RATED_RANKING_RATED_ITEM_TYPE} {i}" for i in range(1, top_k + 1)]
    return column_name_keys


# constant defined for recommending items from all items/from unrated items
RECOMMENDED_ITEM = "Recommended Item"
RECOMMENDED_ITEM_HIT = "Hit"
ACTUAL_COUNT = "Actual Count"

# types defined for score column names attr in DataFrameSchema
RECOMMENDATION_RECOMMENDED_ITEM_TYPE = "Recommendation Recommended Item"
RECOMMENDATION_RECOMMENDED_ITEM_HIT_TYPE = "Recommendation Recommended Item Hit"
RECOMMENDATION_RECOMMENDED_ACTUAL_COUNT_TYPE = "Recommendation Recommended Actual Count"


def build_ranking_column_names(port_scheme: PortScheme, top_k: int):
    column_names = [USER_COLUMN]
    if port_scheme == PortScheme.OnePort:
        column_names += [None] * 2 * top_k
        column_names[1::2] = [f"{RECOMMENDED_ITEM} {i}" for i in range(1, top_k + 1)]
        column_names[2::2] = [f"{RECOMMENDED_ITEM_HIT} {i}" for i in range(1, top_k + 1)]
        column_names += [ACTUAL_COUNT]
    elif port_scheme == PortScheme.TwoPort:
        column_names += [f"{RECOMMENDED_ITEM} {i}" for i in range(1, top_k + 1)]
    return column_names


# for DataFrameSchema score column name attr support
def build_ranking_column_name_keys(port_scheme: PortScheme, top_k: int):
    column_name_keys = [RECOMMENDATION_USER_COLUMN_TYPE]
    if port_scheme == PortScheme.OnePort:
        column_name_keys += [None] * 2 * top_k
        column_name_keys[1::2] = [f"{RECOMMENDATION_RECOMMENDED_ITEM_TYPE} {i}" for i in range(1, top_k + 1)]
        column_name_keys[2::2] = [f"{RECOMMENDATION_RECOMMENDED_ITEM_HIT_TYPE} {i}" for i in range(1, top_k + 1)]
        column_name_keys += [RECOMMENDATION_RECOMMENDED_ACTUAL_COUNT_TYPE]
    elif port_scheme == PortScheme.TwoPort:
        column_name_keys += [f"{RECOMMENDATION_RECOMMENDED_ITEM_TYPE} {i}" for i in range(1, top_k + 1)]
    return column_name_keys


# part for classification
SCORED_LABEL = "Scored Label"
SCORED_PROB = "Scored Probability"
TRUE_LABEL = "Label"

# types defined for score column names attr in DataFrameSchema
RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE = "Recommendation Classification Scored Label"
RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE = "Recommendation Classification Scored Prob"


def build_classification_column_names(port_scheme: PortScheme):
    if port_scheme == PortScheme.OnePort:
        return [TRUE_LABEL, SCORED_LABEL, SCORED_PROB]
    elif port_scheme == PortScheme.TwoPort:
        return [USER_COLUMN, ITEM_COLUMN, SCORED_LABEL, SCORED_PROB]


# for DataFrameSchema score column name attr support
def build_classification_column_name_keys(port_scheme: PortScheme):
    if port_scheme == PortScheme.OnePort:
        return [RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE, RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE]
    else:
        return [RECOMMENDATION_USER_COLUMN_TYPE, RECOMMENDATION_ITEM_COLUMN_TYPE,
                RECOMMENDATION_CLASSIFICATION_SCORED_LABEL_TYPE, RECOMMENDATION_CLASSIFICATION_SCORED_PROB_TYPE]
