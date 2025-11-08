import requests
from bs4 import BeautifulSoup

def get_page_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding Title

        if soup.find('title'):
            page_title = soup.find('title').text
        else:
            'There is no title for this page'

        # Finding meta description

        meta_description = soup.find('meta', attrs = {'name': 'description'})

        meta_desc = ""

        if meta_description and 'content' in meta_description.attrs:
            meta_desc = meta_description['content']
        
        # Finding Headers and its texts

        header_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        headings_data = []
        for tag in header_tags:
            headings_data.append({
                "type": tag.name,
                "text": tag.text
            })

        # Finding broken Images

        image_tags = soup.find_all('img')
        image_src = [img.get('src') for img in image_tags if img.get('src')]

        broken_images = []

        for src in image_src:
            try:
                response = requests.head(src, allow_redirects = True, timeout = 5)
                if response.status_code != 200:
                    broken_images.append((src, response.status_code))
            except:
                pass
        # Missing Image alt texts

        missing_alt_image_text = []

        for img in image_tags:
            alt_text = img.get('alt')
            if alt_text is None or alt_text.strip() == "":
                missing_alt_image_text.append(img.get('src', 'Image with no src attribute'))

        return page_title, headings_data, broken_images, missing_alt_image_text, meta_desc

    except requests.exceptions.RequestException as e:
        print(f"Error during URL access: {e}")
        return None, None


url = input("Enter the URL: ")

[page_title, headings_data, broken_images, missing_alt_image_text, meta_desc] = get_page_details(url)

print("# ---------------Page title -------------------------")
if page_title:
    print("The page title is", page_title)

print("\n")

print("-----------------Meta Description---------------------")
if not meta_desc:
    print("The meta description is empty")
else:
    print("The meta description is --->", meta_desc)

print("\n")

print("------------------Broken Images ------------------------")
if len(broken_images) == 0:
    print("There are no broken image for this page")
else:
    print("There are", len(broken_images), "number of broken images")

print("\n")

print("------------------Missing Image ALt Text-------------------")

if len(missing_alt_image_text) == 0:
    print("There are no missing alt image text on this web page")
else:
    for missing_alt in missing_alt_image_text:
        print("The alt text is missing for this image --->", missing_alt)

print("\n")

print("--------------------Heading Types and Text-------------------")

print("H1 and page title is the same!")
if headings_data:

    for heading in headings_data:
        print('heading val is --->', heading['type'], "associted text is --->", heading['text'])
else:
    print("No heading found")



