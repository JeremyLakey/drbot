from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from datetime import date
import os
import collections

options = Options()
options.headless = True
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1200")

driver=webdriver.Chrome(options=options)

def parse_time(t):
    temp = t[2:]
    nums = []
    stamps = []
    curr = ""
    i = 0
    while i < len(temp):
        if temp[i].isnumeric():
            curr = curr + temp[i]
        else:
            nums.append(int(curr))
            stamps.append(temp[i])
            curr = ""
        i += 1
    f = ""

    for i in range(len(nums)):
        if stamps[i] == 'M':
            if nums[i] == 0:
                return f
            elif nums[i] == 1:
                f += str(nums[i]) + ' Minute '
            else:
                if nums[i] > 90:
                    f += parse_time("PT" + str(nums[i] // 60) + "H" + str(nums[i] % 60) + "M")
                else:
                    f += str(nums[i]) + ' Minutes '
        elif stamps[i] == 'H':
            if nums[i] == 1:
                f += str(nums[i]) + ' Hour '
            else:
                f += str(nums[i]) + ' Hours '
        else:
            f += str(nums[i]) + ' '

    return f

def update_table_of_contents(cat, file, img = None):
    f = open("./recipes/" + cat + "/" + cat + ".md", 'a')
    temp = file.replace(" ", "%20")
    if img is not None:
        f.write("\n\n## [<img src=\"" + img + "\" width=\"100\" height=\"100\" style=\"vertical-align:middle; border:5px solid\"/>&nbsp;&nbsp;" + file + "](" + "./" + temp + ")")
    else:
        f.write("\n\n## [ " + file + "](" + "./" + temp + ")")
    f.close()
def parse_recipe_json(meta, url, cat):
    try:
        file_name = meta["name"] + ".md"
        file_path = "./recipes/" + file_name
        file = open(file_path, mode='w', encoding='utf-8')
        file.write("### [back](./" + cat + ".md)\n")
        file.write("# " + meta["name"])
        file.write("\n")

        if "description" in meta:
            file.write("##### " + meta["description"])
            file.write("\n")

        if "image" in meta:
            img_data = meta["image"]
            if type(img_data) is list:
                if type(img_data[0]) is str:
                    update_table_of_contents(cat, meta["name"], img_data[0])
                    file.write("![main](" + img_data[0] + ")")
                else:
                    update_table_of_contents(cat, meta["name"], img_data[0]['url'])
                    file.write("![main](" + img_data[0]['url'] + ")")
            elif type(img_data) is dict:
                update_table_of_contents(cat, meta["name"], img_data['url'])
                file.write("![main](" + img_data['url'] + ")")
        else:
            update_table_of_contents(cat, meta["name"])


        file.write("\n### Details:")
        if "totalTime" in meta:
            file.write("\n")
            file.write("Total time: " + parse_time(meta["totalTime"]))
            file.write("\n")

        if "recipeYield" in meta:
            file.write("\n")
            file.write("Servings: " + str(meta["recipeYield"]))
            file.write("\n")

        file.write("\n# Ingredients:\n")
        for ing in meta["recipeIngredient"]:
            file.write(ing)
            file.write("\n\n")

        file.write("\n# Steps:\n")
        for step in meta["recipeInstructions"]:
            if 'text' in step:
                file.write("- " + step['text'])
                file.write("\n\n")
            elif 'name' in step:
                file.write("#### " + step['name'] + ":")
                file.write("\n\n")
                for stepp in step["itemListElement"]:
                    file.write("- " + stepp['text'])
                    file.write("\n\n")

        file.write("\n\n\n\n # About\n")
        if "author" in meta:
            if "@id" in meta["author"]:
                file.write("By: " + meta["author"]["@id"])
            else:
                if type(meta["author"]) is list:
                    file.write("By: " + meta["author"][0]["name"])
                else:
                    file.write("By: " + meta["author"]["name"])
            file.write("\n")
        file.write("#### Source: " + url)
        file.write("\n\n#### Date: " + str(date.today()))
        file.close()
        return file_name
    except:
        return None

def scrap_recipe(url, cat):
    driver.get(url)

    eles = driver.find_elements(By.TAG_NAME, 'script')
    for e in eles:
        tex = e.get_attribute('innerText')

        if "\"recipeIngredient\"" in tex:
            meta = json.loads(tex)
            if type(meta) is dict:
                if "@type" in meta and meta["@type"] == "Recipe":
                    return parse_recipe_json(meta, url, cat)
                for key in meta["@graph"]:
                    if key["@type"] == 'Recipe':
                        return parse_recipe_json(key, url, cat)
            else:
                return parse_recipe_json(meta[0], url, cat)
    return None

if __name__ == "__main__":
    print(scrap_recipe("https://www.thechunkychef.com/family-favorite-baked-mac-and-cheese/"))

# failed urls
# https://sugarspunrun.com/vanilla-cake-recipe/