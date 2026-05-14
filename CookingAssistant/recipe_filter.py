import json
import os

RECIPE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cooking_data_merged.json')

def load_recipes():
    with open(RECIPE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


class RecipeFilter:
    def __init__(self):
        self.recipes = load_recipes()

    def filter(self, **criteria):
        results = self.recipes

        if criteria.get('category'):
            results = [r for r in results if criteria['category'] in r.get('category', '')]

        if criteria.get('difficulties'):
            difficulties = criteria['difficulties']
            if isinstance(difficulties, str):
                difficulties = [difficulties]
            results = [r for r in results if r.get('difficulty') in difficulties]

        if criteria.get('property_type'):
            results = [r for r in results if criteria['property_type'] in r.get('property', '')]

        if criteria.get('taste'):
            taste = criteria['taste']
            if isinstance(taste, str):
                taste = [taste]
            results = [r for r in results if any(t in r.get('taste', '') for t in taste)]

        if criteria.get('max_time'):
            max_minutes = int(criteria['max_time'])
            results = [r for r in results if self._time_within(r.get('time', ''), max_minutes)]

        if criteria.get('ingredients'):
            ingredients = criteria['ingredients']
            if isinstance(ingredients, str):
                ingredients = [i.strip() for i in ingredients.split(',')]
            ingredients = [i for i in ingredients if i]
            if ingredients:
                results = [r for r in results if self._has_ingredients(r, ingredients)]

        if criteria.get('seasonings'):
            seasonings = criteria['seasonings']
            if isinstance(seasonings, str):
                seasonings = [s.strip() for s in seasonings.split(',')]
            seasonings = [s for s in seasonings if s]
            if seasonings:
                results = [r for r in results if self._has_seasonings(r, seasonings)]

        if criteria.get('utensils'):
            utensils = criteria['utensils']
            if isinstance(utensils, str):
                utensils = [utensils]
            if utensils:
                results = [r for r in results if self._has_utensils(r, utensils)]

        if criteria.get('keyword'):
            keyword = criteria['keyword']
            results = [r for r in results if
                       keyword in r.get('title', '') or
                       keyword in r.get('category', '') or
                       keyword in str(r.get('ingredients', []))]

        return results[:criteria.get('limit', 20)]

    def _time_within(self, time_str, max_minutes):
        if not time_str:
            return True
        try:
            if '小时' in time_str:
                hours = int(time_str.replace('小时', '').strip())
                return hours * 60 <= max_minutes
            elif '分钟' in time_str:
                minutes = int(time_str.replace('分钟', '').strip())
                return minutes <= max_minutes
        except:
            pass
        return True

    def _has_ingredients(self, recipe, ingredients):
        recipe_ingredients = [str(i).lower() for i in recipe.get('ingredients', [])]
        return any(ing.lower() in recipe_ingredients for ing in ingredients)

    def _has_seasonings(self, recipe, seasonings):
        recipe_seasonings = [str(s).lower() for s in recipe.get('seasonings', [])]
        return any(seasoning.lower() in recipe_seasonings for seasoning in seasonings)

    def _has_utensils(self, recipe, utensils):
        steps_text = ' '.join(recipe.get('steps', [])).lower()
        return any(utensil.lower() in steps_text for utensil in utensils)

    def get_categories(self):
        return sorted(list(set(r.get('category', '') for r in self.recipes)))

    def get_tastes(self):
        return sorted(list(set(r.get('taste', '') for r in self.recipes)))

    def get_difficulties(self):
        return ['简单', '中等', '困难']

    def get_properties(self):
        return sorted(list(set(r.get('property', '') for r in self.recipes)))

    def get_stats(self):
        return {
            'total': len(self.recipes),
            'categories': self.get_categories(),
            'tastes': self.get_tastes(),
            'difficulties': self.get_difficulties(),
            'properties': self.get_properties()
        }


recipe_filter = RecipeFilter()


def filter_recipes(
    category=None,
    difficulty=None,
    property_type=None,
    taste=None,
    max_time=None,
    ingredients=None,
    seasonings=None,
    utensils=None,
    difficulties=None,
    keyword=None,
    limit=20
):
    return recipe_filter.filter(
        category=category,
        difficulties=difficulties,
        property_type=property_type,
        taste=taste,
        max_time=max_time,
        ingredients=ingredients,
        seasonings=seasonings,
        utensils=utensils,
        keyword=keyword,
        limit=limit
    )


def get_filter_options():
    stats = recipe_filter.get_stats()
    return {
        'categories': stats['categories'],
        'tastes': stats['tastes'],
        'difficulties': stats['difficulties'],
        'properties': stats['properties'],
        'total_recipes': stats['total']
    }
