# Constraints
MIN_VALUE_FOR_COOKING_TIME = 1
MIN_VALUE_FOR_AMOUNT = 1

RECIPE_CONSTRAINT_NAME = 'unique_recipe'
INGREDIENT_CONSTRAINT_NAME = 'unique_ingredient'

# Errors message
COOKING_TIME_ERROR = 'Cooking time can not be less than 1'
AMOUNT_ERROR = 'Amount can not be less than 1'
SUBSCRIBE_ON_YOURSELF_ERROR = 'You can not subscribe on yourself'

# Regexs
REGEX_COLOR_FIELD = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'