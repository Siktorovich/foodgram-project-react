# Constraints
MIN_VALUE_FOR_COOKING_TIME = 1
MIN_VALUE_FOR_AMOUNT = 1

RECIPE_CONSTRAINT_NAME = 'unique_recipe'
INGREDIENT_CONSTRAINT_NAME = 'unique_ingredient'
TAG_RECIPE_CONSTRAINT_NAME = 'unique_tag_for_recipe'
INGREDIENT_RECIPE_CONSTRAINT_NAME = 'unique_ingredient_in_recipe'
FAVORITE_CONSTRAINT_NAME = 'unique_favorite'
CART_CONSTRAINT_NAME = 'unique_cart'

# Errors message
# Subscribe model
SUBSCRIBE_ON_YOURSELF_ERROR = 'You can not subscribe on yourself'

# Recipe model
COOKING_TIME_ERROR = 'Cooking time can not be less than 1'
DUBLICATED_RECIPE_INGREDIENTS = 'There is dublicated ingredients in recipe'
DUBLICATED_RECIPE_TAGS = 'There is dublicated tags in recipe'
EMPTY_LIST_INGREDIENTS = 'The recipe should have ingredients'
EMPTY_LIST_TAGS = 'The recipe should have tags'
UNIQUE_NAME_RECIPE = 'There is already recipe with name - '

# Ingredient model
AMOUNT_ERROR = 'Amount can not be less than 1'

# Regexs
REGEX_COLOR_FIELD = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

# Pagination
PAGE_SIZE = 6
MAX_PAGE_SIZE = 50
